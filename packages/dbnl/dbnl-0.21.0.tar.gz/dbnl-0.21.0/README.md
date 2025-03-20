![Distributional](./assets/logo.svg)

## Documentation

See the dbnl [documentation](https://docs.dbnl.com/).

# Distributional SDK Installation Instructions

## 1. Latest Stable Release

To install the latest stable release of the `dbnl` package:

```bash
pip install dbnl
```

## 2. Specific Release

To install a specific version (e.g., version `0.19.1`):

```bash
pip install "dbnl==0.19.1"
```

## 3. Installing with the `eval` Extra

The `dbnl.eval` extra includes additional features and requires an external spaCy model.

### 3.1. Install the Required spaCy Model

To install the required `en_core_web_sm` pre-trained English-language NLP model for SpaCy that matches your spaCy version:

```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

### 3.2. Install `dbnl` with the `eval` Extra

To install `dbnl` with evaluation extras:

```bash
pip install "dbnl[eval]"
```

If you need a specific version with evaluation extras (e.g., version `0.19.1`):

```bash
pip install "dbnl[eval]==0.19.1"
```

## License

[Apache License](./LICENSE)
