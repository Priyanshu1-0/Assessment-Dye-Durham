"""The ``Name`` value object: one person's name, split into its parts."""

from __future__ import annotations

from dataclasses import dataclass


class InvalidNameError(ValueError):
    """Raised when a piece of text cannot be understood as a valid name."""

    def __init__(self, text: str, reason: str) -> None:
        super().__init__(f'Invalid name "{text.strip()}": {reason}')
        self.text = text
        self.reason = reason


@dataclass(frozen=True)
class Name:
    """A person's name: one to three given names followed by a last name.

    A ``Name`` is immutable and always valid; constructing one with the wrong
    number of given names raises ``InvalidNameError``. Most callers will use
    ``Name.parse`` to build one from a line of text.
    """

    MIN_GIVEN_NAMES = 1
    MAX_GIVEN_NAMES = 3

    given_names: tuple[str, ...]
    last_name: str

    def __post_init__(self) -> None:
        count = len(self.given_names)
        if not Name.MIN_GIVEN_NAMES <= count <= Name.MAX_GIVEN_NAMES:
            raise InvalidNameError(
                str(self),
                f"a name must have between {Name.MIN_GIVEN_NAMES} and "
                f"{Name.MAX_GIVEN_NAMES} given names followed by a last name, "
                f"but found {count} given name(s)",
            )

    @classmethod
    def parse(cls, text: str) -> Name:
        """Build a ``Name`` from text such as ``"Hunter Uriah Mathew Clarke"``.

        The final word is the last name and every word before it is a given
        name. Surrounding whitespace is ignored and runs of whitespace between
        words are treated as a single separator.

        Raises ``InvalidNameError`` if the text is blank or has the wrong
        number of given names.
        """
        words = text.split()
        if not words:
            raise InvalidNameError(text, "a name cannot be blank")

        *given_names, last_name = words
        return cls(tuple(given_names), last_name)

    def __str__(self) -> str:
        """The full name with single spaces, e.g. ``"Adonis Julius Archer"``."""
        return " ".join((*self.given_names, self.last_name))
