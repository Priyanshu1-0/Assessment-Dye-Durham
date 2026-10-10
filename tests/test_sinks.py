import io
import tempfile
import unittest
from collections.abc import Sequence
from pathlib import Path

from name_sorter.name import Name
from name_sorter.sinks import CompositeNameSink, ConsoleNameSink, FileNameSink
from tests.helpers import InMemoryNameSink, parse_all

NAMES = parse_all(["Marin Alvarez", "Adonis Julius Archer"])


class ConsoleNameSinkTests(unittest.TestCase):
    def test_prints_each_name_on_its_own_line(self) -> None:
        output = io.StringIO()

        ConsoleNameSink(output).write_names(NAMES)

        self.assertEqual(output.getvalue(), "Marin Alvarez\nAdonis Julius Archer\n")

    def test_prints_nothing_for_an_empty_list(self) -> None:
        output = io.StringIO()

        ConsoleNameSink(output).write_names([])

        self.assertEqual(output.getvalue(), "")


class FileNameSinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "out.txt"

    def test_writes_one_name_per_line_with_a_trailing_newline(self) -> None:
        FileNameSink(self.file).write_names(NAMES)

        self.assertEqual(self.file.read_text(), "Marin Alvarez\nAdonis Julius Archer\n")

    def test_overwrites_an_existing_file_rather_than_appending(self) -> None:
        self.file.write_text("stale content that should disappear\n")

        FileNameSink(self.file).write_names(NAMES)

        self.assertEqual(self.file.read_text(), "Marin Alvarez\nAdonis Julius Archer\n")

    def test_writes_an_empty_file_for_an_empty_list(self) -> None:
        FileNameSink(self.file).write_names([])

        self.assertEqual(self.file.read_text(), "")


class CompositeNameSinkTests(unittest.TestCase):
    def test_writes_the_same_names_to_every_sink(self) -> None:
        first, second = InMemoryNameSink(), InMemoryNameSink()

        CompositeNameSink([first, second]).write_names(NAMES)

        self.assertEqual(first.last_written, ["Marin Alvarez", "Adonis Julius Archer"])
        self.assertEqual(second.last_written, ["Marin Alvarez", "Adonis Julius Archer"])

    def test_writes_to_sinks_in_the_order_they_were_given(self) -> None:
        order: list[str] = []

        class RecordingSink:
            def __init__(self, label: str) -> None:
                self.label = label

            def write_names(self, names: Sequence[Name]) -> None:
                order.append(self.label)

        CompositeNameSink([RecordingSink("screen"), RecordingSink("file")]).write_names([])

        self.assertEqual(order, ["screen", "file"])

    def test_does_nothing_when_it_has_no_sinks(self) -> None:
        CompositeNameSink([]).write_names([Name.parse("Marin Alvarez")])  # must not raise
