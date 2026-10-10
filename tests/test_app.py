import unittest

from name_sorter.app import NameSorterApp
from name_sorter.name import Name
from name_sorter.ordering import by_last_name_then_given_names
from name_sorter.sorter import NameSorter
from tests.helpers import InMemoryNameSink, parse_all


class ListNameSource:
    """A ``NameSource`` backed by an in-memory list of lines."""

    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def read_names(self) -> list[Name]:
        return parse_all(self._lines)


class FailingNameSource:
    def read_names(self) -> list[Name]:
        raise OSError("disk on fire")


class NameSorterAppTests(unittest.TestCase):
    def test_reads_from_the_source_sorts_and_writes_to_the_sink(self) -> None:
        sink = InMemoryNameSink()
        app = NameSorterApp(
            source=ListNameSource(["Janet Parsons", "Marin Alvarez", "Leo Gardner"]),
            sorter=NameSorter(by_last_name_then_given_names),
            sink=sink,
        )

        app.run()

        self.assertEqual(sink.last_written, ["Marin Alvarez", "Leo Gardner", "Janet Parsons"])

    def test_writes_nothing_if_the_source_fails(self) -> None:
        sink = InMemoryNameSink()
        app = NameSorterApp(FailingNameSource(), NameSorter(by_last_name_then_given_names), sink)

        with self.assertRaises(OSError):
            app.run()

        self.assertEqual(sink.writes, [])
