"""Where names come from: the ``NameSource`` interface and its implementations."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, Union

from name_sorter.name import InvalidNameError, Name


class NameSource(Protocol):
    """Somewhere names can be read from, e.g. a file."""

    def read_names(self) -> list[Name]: ...


class NameFileError(Exception):
    """Raised when a names file contains a line that is not a valid name.

    The message includes the file path and line number so that one bad line
    in a thousand-name file is quick to find.
    """


class FileNameSource:
    """Reads names from a plain-text file with one name per line.

    Blank lines are skipped. Any other line that is not a valid name stops the
    read with a ``NameFileError``. Failing loudly was a deliberate choice:
    silently dropping a person from the list would be worse than asking the
    user to fix the data.
    """

    def __init__(self, path: Union[str, Path], encoding: str = "utf-8") -> None:
        self._path = Path(path)
        self._encoding = encoding

    def read_names(self) -> list[Name]:
        text = self._path.read_text(encoding=self._encoding)
        names: list[Name] = []

        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            names.append(self._parse_line(line, line_number))

        return names

    def _parse_line(self, line: str, line_number: int) -> Name:
        try:
            return Name.parse(line)
        except InvalidNameError as error:
            raise NameFileError(f"{self._path}:{line_number}: {error}") from error
