import os
import pathlib
from functools import wraps

import pytest

from pytest_manifest import fixture, Manifest, Undefined


def full_manifest_test(): ...


def keyed_manifest_test(): ...


def missing_manifest_test(): ...


def function_test(): ...


class ClassTest:
    def method_test(self): ...


def prepare(wrapped):
    @wraps(wrapped)
    def wrapper(self, manifest, *args, **kwargs):
        current_dir = pathlib.Path(__file__).parent
        templates_dir = current_dir / "templates"
        manifests_dir = current_dir / "manifests"
        manifests_dir.mkdir(exist_ok=True)

        for template_file in templates_dir.glob("*.yaml"):
            destination_file = manifests_dir / template_file.name
            if not destination_file.exists():
                destination_file.write_text(template_file.read_text())
        try:
            result = wrapped(self, manifest, *args, **kwargs)
        finally:
            for file in manifests_dir.glob("*.yaml"):
                file.unlink()
            manifests_dir.rmdir()
        return result

    return wrapper


class TestManifest:
    @pytest.mark.parametrize(
        ("cls", "function", "expected"),
        (
            (
                None, 
                function_test,
                "manifests/test_pytest_manifest.function_test.yaml",
            ),
            (
                ClassTest, ClassTest.method_test, "manifests/test_pytest_manifest.ClassTest.method_test.yaml",
            ),
        ),
    )
    def test_filepath(self, cls, function, expected):
        manifest = next(fixture(cls, function, False))
        assert (
            os.path.relpath(manifest.filepath, pathlib.Path(__file__).parent)
            == expected
        )

    @pytest.mark.parametrize(
        ("manifest", "actual", "expected"),
        (
            (
                Manifest("tests/manifests/test_pytest_manifest.full_manifest_test.yaml"),
                "Hello world",
                True,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.full_manifest_test.yaml"),
                "Goodbye world",
                False,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml")["hello"],
                "Hello world",
                True,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml")["hello"],
                "Goodbye world",
                False,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml")["goodbye"],
                "Hello world",
                False,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.missing_manifest_test.yaml"),
                "Hello world",
                False,
            ),
        ),
    )
    @prepare
    def test_eq(self, manifest, actual, expected):
        assert bool(manifest == actual) == expected

    @pytest.mark.parametrize(
        ("manifest", "actual", "overwritten_manifest"),
        (
            (
                Manifest("tests/manifests/test_pytest_manifest.full_manifest_test.yaml", overwrite=True),
                "Hello world",
                None,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.full_manifest_test.yaml", overwrite=True),
                "Goodbye world",
                "Goodbye world",
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml", overwrite=True)[
                    "hello"
                ],
                "Hello world",
                None,
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml", overwrite=True)[
                    "hello"
                ],
                "Goodbye world",
                {"hello": "Goodbye world"},
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.keyed_manifest_test.yaml", overwrite=True)[
                    "goodbye"
                ],
                "Goodbye world",
                {"hello": "Hello world", "goodbye": "Goodbye world"},
            ),
            (
                Manifest("tests/manifests/test_pytest_manifest.missing_manifest_test.yaml", overwrite=True),
                "Hello world",
                "Hello world",
            ),
        ),
    )
    @prepare
    def test_overwrite(self, manifest, actual, overwritten_manifest):
        with manifest:
            result = manifest == actual
        if overwritten_manifest:
            assert not result
            assert manifest == actual
            manifest._key = Undefined
            assert manifest == overwritten_manifest
        else:
            assert result
