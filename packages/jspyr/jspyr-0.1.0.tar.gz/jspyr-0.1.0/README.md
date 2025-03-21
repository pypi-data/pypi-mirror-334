# jspyr

JsPyr (pronounced Jasper) combines a Python and a JavaScript program into a single file.

## Installation

```bash
pip install jspyr
```

## Usage

```console
$ cat hello.py
print("Hello, World!")

$ cat hello.js
console.log("Hello, World!");

$ jspyr hello.py hello.js --out hello.jp
Created `hello.jp` from `hello.py` and `hello.js`!

$ python hello.jp
Hello, World!

$ node hello.jp
Hello, World!
```

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests

## Type Checking

Run `mypy .`

## Create and upload a package to PyPI

Make sure to bump the version in `setup.cfg`.

Then run the following commands:

```bash
python -m build
```

Then upload it to PyPI using [twine](https://twine.readthedocs.io/en/latest/#installation):

```bash
twine upload dist/*
```
