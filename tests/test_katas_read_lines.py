import pytest

from katas.read_lines import read_lines


def test_read_lines_yields_all_lines_and_closes_the_file(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("first line\nsecond line\n", encoding="utf-8")

    lines = read_lines(file_path)

    assert list(lines) == ["first line\n", "second line\n"]
    assert lines.gi_frame is None


def test_read_lines_propagates_missing_file_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(read_lines(tmp_path / "missing.txt"))
