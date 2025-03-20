# gopyadapter

# Publishing

* Install [poetry](https://python-poetry.org/)
* Tell poetry what version of python you want to use `poetry env use python3.13`
* Create the venv and install dependencies `poetry install`
* Run `poetry env activate` to activate the environment
* Set your pypy token `poetry config pypi-token.pypi <token>`
* Publish `poetry publish --build`