"""``NameSorter``: sorts names using whichever ordering it is given."""

from __future__ import annotations

from collections.abc import Iterable

from name_sorter.name import Name
from name_sorter.ordering import NameSortKey


class NameSorter:
    """Sorts names according to an injected ``NameSortKey``.

    The sorter owns the mechanics of sorting (never mutating its input,
    keeping equivalent names in their original order) while the key it is
    given owns the business rule of what "sorted" means.
    """

    def __init__(self, key: NameSortKey) -> None:
        self._key = key

    def sort(self, names: Iterable[Name]) -> list[Name]:
        """Return a new, sorted list; the input is left untouched.

        ``sorted`` is stable, so names the key considers equivalent keep the
        order they were read in.
        """
        return sorted(names, key=self._key)
