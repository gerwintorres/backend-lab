from collections.abc import Iterator
from pathlib import Path


def read_lines(file_path: str | Path) -> Iterator[str]:
    """
    Open a text file and yield its lines one by one.
    The file is automatically closed when the context is exited.

    Args:
        file_path (str | Path): The path to the text file.
    """

    with open(file_path, encoding="utf-8") as file:
        yield from file
