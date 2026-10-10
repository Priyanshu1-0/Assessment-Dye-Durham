import tempfile
import unittest
from pathlib import Path

from name_sorter.sources import FileNameSource, NameFileError
from tests.helpers import as_strings


class FileNameSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "names.txt"

    def test_reads_one_name_per_line(self) -> None:
        self.file.write_text("Janet Parsons\nAdonis Julius Archer\n")

        names = FileNameSource(self.file).read_names()

        self.assertEqual(as_strings(names), ["Janet Parsons", "Adonis Julius Archer"])

    def test_copes_with_windows_line_endings(self) -> None:
        self.file.write_bytes(b"Janet Parsons\r\nLeo Gardner\r\n")

        names = FileNameSource(self.file).read_names()

        self.assertEqual(as_strings(names), ["Janet Parsons", "Leo Gardner"])

    def test_skips_blank_lines(self) -> None:
        self.file.write_text("\nJanet Parsons\n   \n\nLeo Gardner")

        names = FileNameSource(self.file).read_names()

        self.assertEqual(as_strings(names), ["Janet Parsons", "Leo Gardner"])

    def test_returns_an_empty_list_for_an_empty_file(self) -> None:
        self.file.write_text("")

        self.assertEqual(FileNameSource(self.file).read_names(), [])

    def test_accepts_a_path_as_a_string(self) -> None:
        self.file.write_text("Leo Gardner\n")

        self.assertEqual(as_strings(FileNameSource(str(self.file)).read_names()), ["Leo Gardner"])

    def test_fails_with_path_and_line_number_when_a_line_is_not_a_valid_name(self) -> None:
        self.file.write_text("Janet Parsons\n\nCher\nLeo Gardner\n")

        with self.assertRaises(NameFileError) as raised:
            FileNameSource(self.file).read_names()

        self.assertTrue(str(raised.exception).startswith(f'{self.file}:3: Invalid name "Cher"'))

    def test_fails_when_the_file_does_not_exist(self) -> None:
        with self.assertRaises(FileNotFoundError):
            FileNameSource(Path(self.tmp.name) / "missing.txt").read_names()
