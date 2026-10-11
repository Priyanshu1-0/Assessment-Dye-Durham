"""How names are ordered.

Python sorts most naturally with a *key function* - something that turns each
item into a value that can be compared with ``<``. A ``NameSortKey`` is such a
function for names. ``NameSorter`` accepts any ``NameSortKey``, so a different
ordering (say, by first name) can be introduced without touching the sorter.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from name_sorter.name import Name


class Comparable(Protocol):
    """A type-checker hint: "this value can be compared with <".

    This class is never created or used when the program runs. It only tells
    tools like mypy that a sort key must return something Python can put in
    order - a string, a number, or a tuple of those. ``__lt__`` is the method
    behind the ``<`` operator. The ``...`` means we are not writing a real
    body; the hint is enough.
    """

    def __lt__(self, other: Any, /) -> bool: ...


# A function that takes a Name and returns something Comparable.
# NameSorter is given one of these; by_last_name_then_given_names is ours.
NameSortKey = Callable[[Name], Comparable]


def by_last_name_then_given_names(name: Name) -> tuple[str, tuple[str, ...]]:
    """The ordering required by the assessment.

    Names are compared by last name first, then by each given name in turn.
    Comparison is case-insensitive (``casefold`` handles more than ASCII).

    The key is a tuple, so Python's tuple comparison does the rest: when one
    name's given names are a prefix of another's (``Leo Gardner`` versus
    ``Leo Alan Gardner``), the shorter tuple - the shorter name - sorts first.
    """
    return (
        name.last_name.casefold(),
        tuple(given_name.casefold() for given_name in name.given_names),
    )
