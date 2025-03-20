# Development
## Development Install
```
git clone https://spacecruft.org/aviation/atc2txt
cd atc2txt/
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install -e .
pip install -e .[dev]
```

## Formatting
```
black src/atc2txt/main.py src/atc2txt/lib/*py
```

## Lint
```
ruff check src/
```

# Build for PyPI
```
pip install -e .[dev]
make all
pip install --upgrade build
python3 -m build
```

# Upload to PyPI
Log into test.pypi.org and pypi.org. Create an API token.
Save token to with formatting to `$HOME/.pypirc`, such as:
```[testpypi]
  username = __token__
  password = pypi-foooooooooooooooooooooooooooooooooooooo
```

Test repo:
```
python3 -m twine upload --repository testpypi dist/*
```

Main repo:
```
python3 -m twine upload dist/*
```

# Release
Move needed files to `dist/` then upload to server.

```
mv docs/_build/latex/en/atc2txt-prepress-en.pdf dist/atc2txt-`atc2txt --version`-en.pdf
```

Upload these files to https://spacecruft.org/aviation/atc2txt/releases
```
atc2txt-VERSION-py3-none-any.whl
atc2txt-VERSION.tar.gz
atc2txt-VERSION-en.pdf

