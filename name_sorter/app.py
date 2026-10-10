"""``NameSorterApp``: the whole program in one sentence."""

from __future__ import annotations

from name_sorter.sinks import NameSink
from name_sorter.sorter import NameSorter
from name_sorter.sources import NameSource


class NameSorterApp:
    """Read names, sort them, write them out.

    The app knows nothing about files or the console. It is handed a source,
    a sorter and a sink, and the entry point (``cli.py``) decides what those
    are. That keeps this class trivial to test with in-memory stand-ins.
    """

    def __init__(self, source: NameSource, sorter: NameSorter, sink: NameSink) -> None:
        self._source = source
        self._sorter = sorter
        self._sink = sink

    def run(self) -> None:
        names = self._source.read_names()
        sorted_names = self._sorter.sort(names)
        self._sink.write_names(sorted_names)
