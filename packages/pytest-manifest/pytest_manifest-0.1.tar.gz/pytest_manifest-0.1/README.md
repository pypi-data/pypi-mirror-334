# pytest-manifest

`pytest-manifest` is a plugin for the `pytest` testing framework. Its purpose is to provide an easy way to capture and assert test outputs.

## Installation

To install `pytest-manifest`, use pip:

```sh
pip install pytest-manifest
```

## Usage

`pytest-manifest` exposes a `manifest` fixture that loads the expected test result from a YAML file and can be asserted against a test output:

```python
def test(manifest):
    assert manifest == "actual"
```

...or load a subset of the file using a key:

```python
    assert manifest["key"] == "actual"
```

The manifest file can optionally be overwritten with the actual test result on failed assertions by passing the `--overwrite-manifest`/`-O` flag to `pytest` when executing tests:

```sh
pytest --overwrite-manifest test.py
```

