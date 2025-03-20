"""Commonly used protocols for type hinting."""

from typing import Protocol as _Protocol, runtime_checkable as _runtime_checkable


@_runtime_checkable
class Stringable(_Protocol):
    """An object that can be converted to a string,
    i.e., one that has a `__str__` method."""

    def __str__(self) -> str:
        ...
