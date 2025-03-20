import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import Any, Tuple
from sklearn.model_selection import train_test_split
from discretization.entropy_based_discretization import find_pivots
from rsclassifier.feature_selection import feature_selection_using_decision_tree, feature_selection_using_brute_force
from rsclassifier.quine_mccluskey import minimize_dnf

class Error(Exception):
    pass

class RuleSetClassifier:
    def __init__(self):
        """
        Initialize the RuleSetClassifier with default values.
        """
        self.semantics = {}  # Maps propositional symbols to pairs [type, feature, value, feature index].
        self.rules = []  # List of rules. Each rule is a pair [output, terms].
        self.default_prediction = None  # Output if no rule matches.
        
        self.is_initialized = False
        self.is_fitted = False

        self.X = None  # The feature data.
        self.y = None  # The target labels.

        self.X_grow = None
        self.y_grow = None

        self.X_prune = None
        self.y_prune = None

    def _booleanize_categorical_features(self, X : pd.DataFrame, categorical_features : list) -> pd.DataFrame:
        """
        Convert categorical features into Boolean features.

        Args:
            X (pandas.DataFrame): The feature data.
            categorical_features (list): List of categorical features.

        Returns:
            pandas.DataFrame: Data with Booleanized categorical features.
        """
        local_X = X.copy()
        for feature in categorical_features:
            unique_values = local_X[feature].unique()
            new_columns = {}
            for value in unique_values:
                # Create a new column for each value (one-hot encoding style).
                new_columns[feature + ' = ' + str(value)] = (local_X[feature] == value)
                # Store semantics for future use.
                self.semantics[feature + ' = ' + str(value)] = ['categorical', feature, value]
            # Concatenate the new Boolean columns with the original data.
            local_X = pd.concat([local_X, pd.DataFrame(new_columns)], axis=1)
        # Drop original categorical columns.
        local_X.drop(columns=categorical_features, inplace=True)
        return local_X

    def _booleanize_numerical_features(self, X : pd.DataFrame, y : pd.Series, numerical_features : list, silent : bool = False) -> pd.DataFrame:
        """
        Discretize numerical features using pivots and convert them into Boolean features.

        Args:
            X (pandas.DataFrame): The feature data.
            y (pandas.Series): The target labels.
            numerical_features (list): List of numerical features.
            silent (bool): Whether to suppress output.

        Returns:
            pandas.DataFrame: Data with Booleanized numerical features.
        """
        local_X = X.copy()
        for feature in tqdm(numerical_features, total=len(numerical_features), desc='Discretizing numerical features...', disable = silent):
            # Find pivot points for discretization.
            pivots = find_pivots(local_X[feature], y)
            if len(pivots) == 0:
                # Skip features with no suitable pivots.
                continue
            new_columns = {}
            for pivot in pivots:
                # Create a Boolean column for values greater than the pivot.
                new_columns[f'{feature} > {pivot:.2f}'] = local_X[feature] > pivot
                # Store semantics for future use.
                self.semantics[f'{feature} > {pivot:.2f}'] = ['numerical', feature, pivot]
            # Concatenate new columns with the data.
            local_X = pd.concat([local_X, pd.DataFrame(new_columns)], axis=1)
        # Drop original numerical columns.
        local_X.drop(columns=numerical_features, inplace=True)
        return local_X

    # Loads and preprocesses data into the classifier.
    def load_data(
            self, X : pd.DataFrame,
            y : pd.Series,
            boolean : list = [],
            categorical : list = [],
            numerical : list = [],
            silent : bool = False
        ) -> None:
        """
        Load and preprocess the data into the classifier by converting features to Boolean features.

        Args:
            X (pandas.DataFrame): The feature data.
            y (pandas.Series): The target labels.
            boolean (list), default = []: List of Boolean features.
            categorical (list), default = []: List of categorical features.
            numerical (list), default = []: List of numerical features.
            silent (bool), default = False: Whether to suppress output.
        """
        bool_X = X.copy()
        if len(boolean) > 0:
            for feature in boolean:
                bool_X[feature] = X[feature].astype(bool)
                self.semantics[feature] = ['boolean', feature]
        if len(categorical) > 0:
            bool_X = self._booleanize_categorical_features(bool_X, categorical)
        if len(numerical) > 0:
            bool_X = self._booleanize_numerical_features(bool_X, y, numerical, silent)

        # Store indexes for features for numpy-operations.
        for key, value in self.semantics.items():
            updated_value = value + [X.columns.get_loc(value[1])]
            self.semantics[key] = updated_value

        self.X = bool_X
        self.y = y
        self.is_initialized = True
        if not silent:
            print(f'Total number of Boolean features: {len(self.X.columns)}')

    def _form_rule_set(self, features : list, default_prediction : Any, silent : bool) -> None:
        """
        Form a set of rules based on the data.

        Args:
            features (list): List of features to use.
            default_prediction (any): Default prediction if no rule matches.
            silent (bool): Whether to suppress output.
        """
        self.rules = []
    
        # Convert DataFrame to NumPy array
        local_X_np = self.X_grow[features].to_numpy()
        y_np = self.y_grow.to_numpy()
        
        # Track unique "types" (feature value combinations)
        unique_types, inverse_indices = np.unique(local_X_np, axis=0, return_inverse=True)
        
        # Count occurrences of each (type, y) pair
        unique_y = np.unique(y_np)
        type_scores = np.zeros((len(unique_types), len(unique_y)))

        for i in tqdm(range(len(y_np)), desc='Calculating probabilities...', disable=silent):
            type_scores[inverse_indices[i], np.where(unique_y == y_np[i])[0][0]] += 1

        # Determine default prediction if not given
        if default_prediction is None:
            self.default_prediction = self.y_grow.mode()[0]
        else:
            self.default_prediction = default_prediction

        # Generate rules
        rules = {y: [] for y in unique_y if y != self.default_prediction}

        for i in tqdm(range(len(unique_types)), desc='Forming the classifier...', disable=silent):
            best_y = unique_y[np.argmax(type_scores[i])]
            if best_y != self.default_prediction:
                rules[best_y].append(unique_types[i])

        # Remove empty rule lists
        self.rules = [(key, [list(zip(rule,features)) for rule in value]) for key, value in rules.items() if value]

    def _prune_terms_using_domain_knowledge(self, terms : list) -> list:
        """
        Prune terms using domain knowledge to simplify them.

        Args:
            terms (list of lists): The list of terms to simplify.

        Returns:
            list: Simplified terms.
        """
        simplified_terms = []
        for term in terms:
            simplified_term = []
            positive_categories = []
            upper_bounds = {}
            lower_bounds = {}
            for literal in term:
                meaning = self.semantics[literal[1]]
                if meaning[0] == 'categorical':
                    if literal[0] == 0:
                        simplified_term.append(literal)
                    if literal[0] == 1 and meaning[1] not in positive_categories:
                        positive_categories.append(meaning[1])
                        simplified_term.append(literal)
                elif meaning[0] == 'numerical':
                    if literal[0] == 0:
                        if meaning[1] not in upper_bounds or meaning[2] <= upper_bounds[meaning[1]]:
                            upper_bounds[meaning[1]] = meaning[2]
                    if literal[0] == 1:
                        if meaning[1] not in lower_bounds or meaning[2] > lower_bounds[meaning[1]]:
                            lower_bounds[meaning[1]] = meaning[2]
                else:
                    simplified_term.append(literal)
            for feature in upper_bounds.keys():
                simplified_term.append([0, f'{feature} > {upper_bounds[feature]:.2f}'])
            for feature in lower_bounds.keys():
                simplified_term.append([1, f'{feature} > {lower_bounds[feature]:.2f}'])
            simplified_terms.append(simplified_term)
        return simplified_terms
    
    def _evaluate_term_using_training_data(self, term : list, prediction : Any) -> float:
        """
        Evaluate the accuracy of a given term using training data.

        Args:
            term (list): A list of literals.
            prediction (Any): The predicted class label associated with the term.

        Returns:
            float: The accuracy of the term, calculated as the ratio of correct predictions made by 
                   the term to the total number of instances covered by the term. Returns 0.0 if the 
                   term covers no instances.
        """
        X_grow_np = self.X_grow.to_numpy()
        feature_names = self.X_grow.columns.to_list()

        term_mask = np.all([
            (X_grow_np[:, feature_names.index(literal[1])] == literal[0])
            for literal in term
        ], axis=0)

        covered_count = term_mask.sum()
        if covered_count == 0:
            return 0.0

        correct_count = np.sum(term_mask & (self.y_grow == prediction))
        return correct_count / covered_count
    
    def _prune_terms_useless_literals(self, terms : list, prediction : Any, silent : bool) -> list:
        """
        Prune a given term by removing unnecessary (based on training data) literals.

        Args:
            terms (list): A list of terms.
            prediction (Any): The predicted class label associated with the term.
            silent (bool): Whether to suppress output.

        Returns:
            list: The pruned terms.
        """
        pruned_terms = []
        for term in tqdm(terms, desc = f'Pruning terms for class {prediction}...', disable = silent):
            local_term = term.copy()
            while True:
                old_score = self._evaluate_term_using_training_data(local_term, prediction)
                best_term = local_term
                for i in range(len(local_term)):
                    reduced_term = local_term[:i] + local_term[i + 1:]  # Avoid deep copy
                    new_score = self._evaluate_term_using_training_data(reduced_term, prediction)
                    if old_score == new_score:
                        best_term = reduced_term
                if best_term == local_term:
                    break
                local_term = best_term
            pruned_terms.append(local_term)
        return pruned_terms
    
    def _evaluate_term_using_cross_validation(self, term : list, prediction : Any) -> float:
        """
        Evaluate the accuracy of a given term using cross-validation.

        Args:
            term (list): A list of literals.
            prediction (Any): The predicted class label associated with the term.

        Returns:
            float: The accuracy of the term, calculated as the ratio of correct predictions made by 
                   the term to the total number of instances covered by the term. Returns 0.0 if the 
                   term covers no instances.
        """
        term_mask = np.ones(len(self.X_prune), dtype = bool)
        for literal in term:
            term_mask &= (self.X_prune[literal[1]] == literal[0])
        sum = (term_mask).sum()
        if sum == 0:
            return 0.0
        else:
            return (term_mask & (self.y_prune == prediction)).sum() / sum
    
    def _prune_term_cross_validation(self, terms : list, prediction : Any, silent : bool) -> list:
        """
        Prune a given term by removing unnecessary (based on cross validation) literals.

        Args:
            terms (list): A list of terms.
            prediction (Any): The predicted class label associated with the term.
            silent (bool): Whether to suppress output.

        Returns:
            list: The pruned terms.
        """
        pruned_terms = []
        for term in tqdm(terms, desc = f'Pruning terms for class {prediction}...', disable = silent):
            local_term = term.copy()
            while True:
                highest_score = self._evaluate_term_using_cross_validation(local_term, prediction)
                best_term = local_term
                for i in range(len(local_term)):
                    reduced_term = local_term[:i] + local_term[i + 1:]  # Avoid deep copy
                    score = self._evaluate_term_using_cross_validation(reduced_term, prediction)
                    if score > highest_score:
                        highest_score = score
                        best_term = reduced_term
                if best_term == local_term:
                    break
                local_term = best_term
            pruned_terms.append(local_term)
        return pruned_terms

    def _entails(self, term1 : list, term2 : list) -> bool:
        """
        Check whether term1 entails term2, meaning every condition in term2 is satisfied by term1.

        Args:
            term1 (list): The first term.
            term2 (list): The second term.

        Returns:
            bool: True if term1 entails term2, False otherwise.
        """
        for l2 in term2:
            # We need to check that term1 contains a literal l1 which entails l2.
            entailed = False
            for l1 in term1:
                if l1[0] == l2[0]:
                    meaning1 = self.semantics[l1[1]]
                    meaning2 = self.semantics[l2[1]]
                    if meaning1[1] == meaning2[1]:
                        if meaning1[0] == 'boolean':
                            entailed = True
                            break
                        elif meaning1[0] == 'categorical' and meaning1[2] == meaning2[2]:
                            entailed = True
                            break
                        elif meaning1[0] == 'numerical':
                            if l1[0] == 0 and meaning2[2] >= meaning1[2]:
                                entailed = True
                                break
                            elif meaning2[2] <= meaning1[2]:
                                entailed = True
                                break
            if not entailed:
                return False
        return True
    
    def _simplify(self, silent = False) -> None:
        """
        Simplify the classifier's rule set by pruning and removing redundant terms.

        The simplification process involves three main steps:
        1. Boolean optimization using the Quine-McCluskey algorithm.
        2. Domain knowledge-based pruning.
        3. Removing literals that do not contribute to accuracy.
        4. Further pruning based on cross validation.
        5. Removing redundant terms by checking if any term entails another.

        Args:
            silent (bool): Whether to suppress output.
        """
        simplified_rules = []
        for rule in self.rules:
            prediction = rule[0]
            terms = rule[1]
            
            # Step 1. Boolean optimization.
            simplified_terms = minimize_dnf(terms)

            # Step 2. Domain knowledge.
            simplified_terms = self._prune_terms_using_domain_knowledge(simplified_terms)

            # Step 3. Remove literals that do not contribute to accuracy.
            simplified_terms = self._prune_terms_useless_literals(simplified_terms, prediction, silent)

            # Step 4. Pruning based on cross validation.
            if self.X_prune is not None:
                # TODO: This pruning can also lead to conflicts between rules. Is this a problem?
                simplified_terms = self._prune_term_cross_validation(simplified_terms, prediction, silent)
            
            # Step 5. Pruning can cause some of the rules to become redundant. Remove them.
            necessary_terms = []
            for i in range(len(simplified_terms)):
                necessary = True
                for j in range(i + 1, len(simplified_terms)):
                    if self._entails(simplified_terms[i], simplified_terms[j]):
                        necessary = False
                        break
                if necessary:
                    necessary_terms.append(simplified_terms[i])
        
            simplified_rules.append([prediction, necessary_terms])

        self.rules = simplified_rules

    def fit(self,
            num_prop : int,
            fs_algorithm : str = 'dt',
            growth_size : float = 1.0,
            random_state : int = 42,
            default_prediction : Any = None,
            silent : bool = False
        ) -> None:
        """
        Train the RuleSetClassifier by selecting features, forming rules and simplifying the rules.

        Args:
            num_prop (int): The number of features (properties) to use.
            fs_algorithm ({'dt', 'brute'}), default = 'dt': Algorithm used to select which Boolean features to use.
            growth_size (float), default = 1.0: Should be in the range (0,1] and represent the proportion of the dataset to include in the growth split. If equal to 1.0 (the default value), no pruning will be done.
            random_state (int), default = 42: Controls the shuffling applied to the data before applying the split.
            default_prediction (any), dfault = None: The default prediction if no rule matches.
            silent (bool), default = False: If True, suppress output during training.
        """
        if not self.is_initialized:
            raise Error('Data has not been loaded.')
        
        if growth_size <= 0.0 or growth_size > 1.0:
            raise Error('growth_size needs to be in the range (0,1].')
        
        if num_prop > len(self.X.columns):
            if not silent:
                print('WARNING: num_prop more than the number of features. All of the features will be used.')
                num_prop = len(self.X.columns)
        
        if fs_algorithm == 'dt':
            used_props = feature_selection_using_decision_tree(self.X, self.y, num_prop)
        elif fs_algorithm == 'brute':
            used_props = feature_selection_using_brute_force(self.X, self.y, num_prop, silent)
        else:
            raise Error('Invalid fs_algorithm.')
        
        if growth_size == 1.0:
            self.X_grow = self.X
            self.X_prune = None
            self.y_grow = self.y
            self.y_prune = None
        else:
            X_grow, X_prune, y_grow, y_prune = train_test_split(self.X, self.y, test_size = growth_size, random_state = random_state)
            self.X_grow = X_grow
            self.X_prune = X_prune
            self.y_grow = y_grow
            self.y_prune = y_prune

        self._form_rule_set(used_props, default_prediction, silent)
        self._simplify(silent)
        self.is_fitted = True

    def _evaluate_batch(self, X: np.ndarray) -> np.ndarray:
        """
        Evaluate a batch of input assignments by checking which rule they satisfy.

        Args:
            X (np.ndarray): A 2D NumPy array where each row represents an instance.

        Returns:
            np.ndarray: An array of predicted output classes.
        """
        num_samples = X.shape[0]
        predictions = np.full(num_samples, self.default_prediction)  # Default predictions

        for rule in self.rules:
            output = rule[0]
            terms = rule[1]
            
            # Create a mask for samples satisfying at least one term
            term_satisfied = np.zeros(num_samples, dtype=bool)
            
            for term in terms:
                term_mask = np.ones(num_samples, dtype=bool)  # Start assuming all rows satisfy the term
                
                for literal in term:
                    interpretation = self.semantics[literal[1]]
                    
                    if interpretation[0] == 'boolean':
                        term_mask &= (X[:, interpretation[2]] == literal[0])
                    
                    elif interpretation[0] == 'numerical':
                        term_mask &= (X[:, interpretation[3]] > interpretation[2]) == literal[0]
                    
                    else:  # Categorical or other types
                        term_mask &= (X[:, interpretation[3]] == interpretation[2]) == literal[0]
                    
                    if not term_mask.any():  # Early exit if no sample satisfies
                        break

                term_satisfied |= term_mask  # If any term is satisfied, the rule applies
            
            # Assign predictions for samples satisfying the rule
            predictions[term_satisfied] = output

        return predictions

    def predict(self, X : pd.DataFrame) -> pd.Series:
        """
        Predict the class labels for a dataset.

        Args:
            X (pandas.DataFrame): The feature data for which predictions are made.

        Returns:
            pandas.Series: The predicted class labels.
        """
        if not self.is_fitted:
            raise Error("Model has not been fitted.")
        return pd.Series(self._evaluate_batch(X.to_numpy()))
    
    def _term_support_and_confidence(self, term : list, prediction : Any) -> Tuple[int, float]:
        """
        Calculate the support and confidence for a given term and prediction.

        Support: The number of data points that satisfy the rule.
        Confidence: The probability that a data point satisfying the rule is correctly classified.

        Args:
            term (list): A list of literals.
            prediction (any): The predicted value associated with the term.

        Returns:
            tuple: (t, p)
                - t (int): support
                - p (float): confidence
        """
        # Identify rows where the prediction is correct
        correct_prediction_mask = (self.y == prediction)

        # Check whether each row satisfies the term
        term_mask = np.ones(len(self.X), dtype = bool)
        for literal in term:
            term_mask &= (self.X[literal[1]] == literal[0])

        # Number of rows where term is true (t) and correct prediction (p)
        t = term_mask.sum()
        p = (term_mask & correct_prediction_mask).sum()

        return t, p/t

    def __str__(self) -> str:
        """
        Return a string representation of the rule set.

        Each rule is displayed with its corresponding terms, support, and confidence.

        Returns:
            str: A human-readable string representation of the rule set.
        """
        output = str()
        for i in range(len(self.rules)):
            rule = self.rules[i]
            if i > 0:
                output += 'ELSE IF\n'
            else:
                output += 'IF\n'
            prediction = rule[0]
            terms = rule[1]
            for i in range(len(terms)):
                if i > 0:
                    output += 'OR '
                output += '('
                term = terms[i]
                for j in range(len(term)):
                    if j > 0:
                        output += ' AND '
                    if term[j][0] == 0:
                        meaning = self.semantics[term[j][1]]
                        if meaning[0] == 'numerical':
                            output += f'{meaning[1]} <= {meaning[2]}'
                        else:
                            output += f'NOT {term[j][1]}'
                    else:
                        output += term[j][1]
                support, confidence = self._term_support_and_confidence(term, prediction)
                output += f') {{support: {support}, confidence: {confidence:.2f}}}\n'
            output += f'THEN {rule[0]}\n'
        output += f'ELSE {self.default_prediction}\n'
        return output