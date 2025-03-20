import os
import pathlib
from functools import wraps

import pytest

from manifest import Manifest, Undefined


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
        ("manifest", "expected"),
        (
            (
                Manifest(None, function_test, None),
                "manifests/test_manifest.function_test.yaml",
            ),
            (
                Manifest(ClassTest, ClassTest.method_test, None),
                "manifests/test_manifest.ClassTest.method_test.yaml",
            ),
        ),
    )
    @prepare
    def test_filepath(self, manifest, expected):
        assert (
            os.path.relpath(manifest.filepath, pathlib.Path(__file__).parent)
            == expected
        )

    @pytest.mark.parametrize(
        ("manifest", "actual", "expected"),
        (
            (
                Manifest(None, full_manifest_test, None),
                "Hello world",
                True,
            ),
            (
                Manifest(None, full_manifest_test, None),
                "Goodbye world",
                False,
            ),
            (
                Manifest(None, keyed_manifest_test, None)["hello"],
                "Hello world",
                True,
            ),
            (
                Manifest(None, keyed_manifest_test, None)["hello"],
                "Goodbye world",
                False,
            ),
            (
                Manifest(None, keyed_manifest_test, None)["goodbye"],
                "Hello world",
                False,
            ),
            (
                Manifest(None, missing_manifest_test, None),
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
                Manifest(None, full_manifest_test, None, overwrite=True),
                "Hello world",
                None,
            ),
            (
                Manifest(None, full_manifest_test, None, overwrite=True),
                "Goodbye world",
                "Goodbye world",
            ),
            (
                Manifest(None, keyed_manifest_test, None, overwrite=True)[
                    "hello"
                ],
                "Hello world",
                None,
            ),
            (
                Manifest(None, keyed_manifest_test, None, overwrite=True)[
                    "hello"
                ],
                "Goodbye world",
                {"hello": "Goodbye world"},
            ),
            (
                Manifest(None, keyed_manifest_test, None, overwrite=True)[
                    "goodbye"
                ],
                "Goodbye world",
                {"hello": "Hello world", "goodbye": "Goodbye world"},
            ),
            (
                Manifest(None, missing_manifest_test, None, overwrite=True),
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
