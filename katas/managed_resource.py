from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


@contextmanager
def managed_resource(resource: Any) -> Iterator[Any]:
    """
    Open a resource and ensure it is closed after use.

    Args:
        resource: A path accepted by open().
    """

    with open(resource) as resource_file:
        yield resource_file
