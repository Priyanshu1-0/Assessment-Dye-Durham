"""Where names come from: the ``NameSource`` interface and its implementations."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, Union

from name_sorter.name import InvalidNameError, Name


class NameSource(Protocol):
    """Somewhere names can be read from, e.g. a file."""

    def read_names(self) -> list[Name]: ...


class NameFileError(Exception):
    """Raised when a names file cannot be understood: either a line is not a
    valid name, or the file is not text in the expected encoding.

    The message always names the file (and the line, where there is one) so
    that one bad line in a thousand-name file is quick to find.
    """


class FileNameSource:
    """Reads names from a plain-text file with one name per line.

    Blank lines are skipped. Any other line that is not a valid name stops the
    read with a ``NameFileError``. Failing loudly was a deliberate choice:
    silently dropping a person from the list would be worse than asking the
    user to fix the data.

    The default encoding, ``utf-8-sig``, is plain UTF-8 that also tolerates
    the byte-order mark Windows Notepad and Excel put at the start of a file.
    Without it, the mark would be glued onto the first name as an invisible
    character and that name would sort in the wrong place.
    """

    def __init__(self, path: Union[str, Path], encoding: str = "utf-8-sig") -> None:
        self._path = Path(path)
        self._encoding = encoding

    def read_names(self) -> list[Name]:
        text = self._read_text()
        names: list[Name] = []

        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            names.append(self._parse_line(line, line_number))

        return names

    def _read_text(self) -> str:
        try:
            return self._path.read_text(encoding=self._encoding)
        except UnicodeDecodeError as error:
            raise NameFileError(
                f"{self._path}: file is not valid {self._encoding} text "
                f"(bad byte at position {error.start}). Save it as UTF-8 and try again."
            ) from error

    def _parse_line(self, line: str, line_number: int) -> Name:
        try:
            return Name.parse(line)
        except InvalidNameError as error:
            raise NameFileError(f"{self._path}:{line_number}: {error}") from error
