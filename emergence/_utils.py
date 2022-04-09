from __future__ import annotations

import functools
from typing import Callable, Iterable, TypeVar

_T = TypeVar("_T")


def reduce(iterable: Iterable[_T], func: Callable[[_T, _T], _T]) -> _T:
    iterator = iter(iterable)
    try:
        init = next(iterator)
    except StopIteration:
        raise IndexError("empty iterable")  # pylint: disable=raise-missing-from
    return functools.reduce(func, iterator, init)
