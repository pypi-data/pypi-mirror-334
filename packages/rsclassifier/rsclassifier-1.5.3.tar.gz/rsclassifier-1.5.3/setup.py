from setuptools import setup

setup(name = 'rsclassifier',
      version = '1.5.3',
      author = 'Reijo Jaakkola',
      author_email = 'jaakkolareijo@hotmail.com',
      description = 'Package for training rule set classifiers for tabular data.',
      packages = [
          'rsclassifier',
          'discretization'
      ]
)