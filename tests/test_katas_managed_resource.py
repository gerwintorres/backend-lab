import pytest

from katas.managed_resource import managed_resource


def test_managed_resource_yields_readable_file_and_closes_it(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("contents", encoding="utf-8")

    with managed_resource(file_path) as resource:
        assert resource.read() == "contents"
        assert not resource.closed

    assert resource.closed


def test_managed_resource_propagates_missing_file_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        with managed_resource(tmp_path / "missing.txt"):
            pass
