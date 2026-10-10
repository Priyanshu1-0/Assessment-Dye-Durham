"""Where names go: the ``NameSink`` interface and its implementations."""

from __future__ import annotations

import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Optional, Protocol, TextIO, Union

from name_sorter.name import Name


class NameSink(Protocol):
    """Somewhere names can be written to, e.g. the screen or a file."""

    def write_names(self, names: Sequence[Name]) -> None: ...


class ConsoleNameSink:
    """Prints names to the screen, one per line.

    The output stream is injectable (defaulting to ``sys.stdout``) so tests
    can capture what would have been printed.
    """

    def __init__(self, output: Optional[TextIO] = None) -> None:
        self._output = output

    def write_names(self, names: Sequence[Name]) -> None:
        # Resolved at write time, not construction time, so that anything
        # which swaps sys.stdout (e.g. a test harness) is respected.
        output = self._output if self._output is not None else sys.stdout
        output.writelines(_as_lines(names))


class FileNameSink:
    """Writes names to a plain-text file, one per line.

    Whatever the file previously contained is replaced.
    """

    def __init__(self, path: Union[str, Path], encoding: str = "utf-8") -> None:
        self._path = Path(path)
        self._encoding = encoding

    def write_names(self, names: Sequence[Name]) -> None:
        self._path.write_text("".join(_as_lines(names)), encoding=self._encoding)


class CompositeNameSink:
    """Fans a single write out to several sinks, in the order they were given.

    This lets the application write "to the screen and to a file" while only
    ever talking to one ``NameSink``.
    """

    def __init__(self, sinks: Iterable[NameSink]) -> None:
        self._sinks = tuple(sinks)

    def write_names(self, names: Sequence[Name]) -> None:
        for sink in self._sinks:
            sink.write_names(names)


def _as_lines(names: Iterable[Name]) -> Iterable[str]:
    return (f"{name}\n" for name in names)
