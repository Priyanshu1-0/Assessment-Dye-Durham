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

    def test_ignores_a_utf8_byte_order_mark_from_windows_editors(self) -> None:
        self.file.write_bytes(b"\xef\xbb\xbfJanet Parsons\nMarin Alvarez\n")

        names = FileNameSource(self.file).read_names()

        self.assertEqual(as_strings(names), ["Janet Parsons", "Marin Alvarez"])
        self.assertEqual(names[0].given_names, ("Janet",), "the mark must not be glued onto the first name")

    def test_fails_clearly_when_the_file_is_not_utf8(self) -> None:
        self.file.write_bytes("José García\n".encode("latin-1"))

        with self.assertRaises(NameFileError) as raised:
            FileNameSource(self.file).read_names()

        self.assertIn(str(self.file), str(raised.exception))
        self.assertIn("not valid utf-8-sig text", str(raised.exception))

    def test_fails_when_the_file_does_not_exist(self) -> None:
        with self.assertRaises(FileNotFoundError):
            FileNameSource(Path(self.tmp.name) / "missing.txt").read_names()
