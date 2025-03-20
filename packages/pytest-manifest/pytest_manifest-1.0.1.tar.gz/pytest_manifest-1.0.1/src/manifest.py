import contextlib
import inspect
import os
from typing import Final, Union

import pytest
import yaml


class UndefinedType:
    """
    Represents an undefined value in tests.
    """

    def __repr__(self):
        return "Undefined"


Undefined: Final = UndefinedType()


class Manifest:
    """
    Context manager for asserting against a manifest file of results in tests.

    Usage:
    
    >>> def test(manifest):
    >>>     assert manifest == "actual"

    ...or:

    >>>     assert manifest["key"] == "actual"

    Running pytest with the --overwrite-manifest flag will copy the actual
    results to a manifest YAML file if the equality assertion fails. The 
    manifest filename is generated from the test module, class (if applicable),
    and function names. Manifest files are stored in a "manifests" directory in 
    the test directory.
    """

    actual: Union[list, dict, UndefinedType] = Undefined

    def __init__(
        self,
        test_class,
        test_function,
        test_input,
        overwrite=False,
        *,
        key=Undefined,
    ):
        filename = ".".join(
            [
                test_class.__module__,
                test_class.__name__,
                test_function.__name__,
                "yaml",
            ]
            if test_class
            else [test_function.__module__, test_function.__name__, "yaml"]
        )
        filename = filename.replace("tests.", "")
        filedir = os.path.join(
            os.path.dirname(os.path.realpath(inspect.getfile(test_function))),
            "manifests",
        )
        os.makedirs(filedir, exist_ok=True)
        self.filepath = os.path.join(filedir, filename)
        self._key = key
        self.overwrite = overwrite

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.actual is not Undefined and self.overwrite:
            try:
                with open(self.filepath, "r") as file:
                    manifest = yaml.load(file, Loader=yaml.FullLoader) or {}
            except FileNotFoundError:
                manifest = {}
            if self._key is Undefined:
                manifest = self.actual
            else:
                manifest[self._key] = self.actual
            if self.overwrite:
                with open(self.filepath, "w") as file:
                    try:
                        yaml.dump(
                            manifest,
                            file,
                            sort_keys=True,
                            indent=4,
                            encoding="utf-8",
                            allow_unicode=True,
                        )
                    except TypeError:
                        file.seek(0)
                        file.truncate()
                        yaml.dump({}, file)
                        raise

    def __eq__(self, actual):
        if not (eq := self.__manifest == actual):
            self.actual = actual
        return eq

    def __getitem__(self, key):
        self._key = key
        return self

    @property
    def __manifest(self):
        try:
            with open(self.filepath, "r") as file:
                if manifest := yaml.load(file, Loader=yaml.FullLoader):
                    if self._key is Undefined:
                        return manifest
                    else:
                        return manifest.get(self._key, Undefined)
                else:
                    return Undefined
        except FileNotFoundError:
            return Undefined

    @contextlib.contextmanager
    def key(self, key):
        default_key = self._key
        self._key = key
        yield
        self._key = default_key


@pytest.fixture
def manifest(request):
    """Fixture for handling manifest results in tests."""
    with Manifest(
        request.cls,
        request.function,
        request.node.funcargs,
        request.config.getoption("overwrite"),
    ) as manifest:
        yield manifest


def pytest_addoption(parser):
    """Adds custom command-line options to pytest."""
    parser.addoption(
        "-O",
        "--overwrite-manifest",
        action="store_true",
        dest="overwrite",
        help="Copy actual results to the manifest file",
    )


def folded_unicode_representer(dumper: yaml.Dumper, data):
    if data.count("\n") > 0:
        # Remove any trailing spaces, then put it back together again
        data = "\n".join([line.rstrip() for line in data.splitlines()])
        return dumper.represent_scalar(
            "tag:yaml.org,2002:str", data, style="|"
        )
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, folded_unicode_representer)
