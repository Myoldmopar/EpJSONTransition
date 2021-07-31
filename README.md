# EpJSON Transition

[![Documentation Status](https://readthedocs.org/projects/epjson-transition/badge/?version=latest&style=for-the-badge)](https://epjson-transition.readthedocs.io/en/latest/?badge=latest)
[![Unit Tests](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/Test?label=Unit%20Tests&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3A%22Test%22)
[![Coverage Status](https://img.shields.io/coveralls/github/Myoldmopar/EpJSONTransition?label=Coverage&style=for-the-badge)](https://coveralls.io/github/Myoldmopar/EpJSONTransition?branch=main)
[![PEP8 Enforcement](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/Flake8?label=Flake8&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3AFlake8)

Prototype tool for doing EpJSON transition

## Testing

The project is tested using standard Python unit testing practices.
Each commit is automatically tested with Github Actions on Windows, Mac, Ubuntu 18.04 and Ubuntu 20.04.
The code coverage across platforms is collected on Coveralls.
When a tag is created in the GitHub Repo, Github Actions builds downloadable packages.

## Development

To run the unit test suite, make sure to have nose and coverage installed via: `pip install nose coverage`.
Then execute `setup.py nosetests`.
Unit test results will appear in the console, and coverage results will be in a `htmlcov` directory.