"""Small shared helpers for the test suite."""

from __future__ import annotations

import random
from collections.abc import Iterable, Sequence

from name_sorter.name import Name


def parse_all(lines: Iterable[str]) -> list[Name]:
    return [Name.parse(line) for line in lines]


def as_strings(names: Iterable[Name]) -> list[str]:
    return [str(name) for name in names]


class InMemoryNameSink:
    """A ``NameSink`` that simply remembers what it was asked to write."""

    def __init__(self) -> None:
        self.writes: list[Sequence[Name]] = []

    def write_names(self, names: Sequence[Name]) -> None:
        self.writes.append(names)

    @property
    def last_written(self) -> list[str]:
        """The names from the most recent write, as plain strings."""
        return as_strings(self.writes[-1]) if self.writes else []


# The example given in the assessment brief, and the order it should produce.
EXAMPLE_UNSORTED = [
    "Janet Parsons",
    "Vaughn Lewis",
    "Adonis Julius Archer",
    "Shelby Nathan Yoder",
    "Marin Alvarez",
    "London Lindsey",
    "Beau Tristan Bentley",
    "Leo Gardner",
    "Hunter Uriah Mathew Clarke",
    "Mikayla Lopez",
    "Frankie Conner Ritter",
]

EXAMPLE_SORTED = [
    "Marin Alvarez",
    "Adonis Julius Archer",
    "Beau Tristan Bentley",
    "Hunter Uriah Mathew Clarke",
    "Leo Gardner",
    "Vaughn Lewis",
    "London Lindsey",
    "Mikayla Lopez",
    "Janet Parsons",
    "Frankie Conner Ritter",
    "Shelby Nathan Yoder",
]


def generate_names(count: int, seed: int = 0) -> list[str]:
    """Deterministically generate ``count`` plausible, messy name lines.

    Mixes 1-3 given names, inconsistent letter case and awkward last names
    so that large-scale tests exercise the same edge cases the unit tests do.
    """
    rng = random.Random(seed)
    given = ["Adam", "Zoe", "Leo", "Marin", "Janet", "Hunter", "Uriah", "Beau",
             "Tristan", "London", "Mikayla", "Frankie", "Conner", "Shelby",
             "Nathan", "Adonis", "Julius", "Vaughn", "Casey", "Drew", "Ellis"]
    last = ["Parsons", "Lewis", "Archer", "Yoder", "Alvarez", "Lindsey", "Bentley",
            "Gardner", "Clarke", "Lopez", "Ritter", "Smith", "smith", "McDonald",
            "Macdonald", "Nguyen", "O'Brien", "Zhang", "Abbott", "Young"]

    lines = []
    for _ in range(count):
        given_count = rng.choice([1, 1, 2, 2, 3])
        lines.append(" ".join([*rng.sample(given, given_count), rng.choice(last)]))
    return lines
