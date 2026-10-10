"""End-to-end tests.

These run the real ``name-sorter`` executable in a scratch working directory,
exactly as the assessors will, and check the screen output, the written file
and the exit code.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from name_sorter.cli import OUTPUT_FILE_NAME, USAGE
from tests.helpers import EXAMPLE_SORTED, EXAMPLE_UNSORTED, generate_names

REPO_ROOT = Path(__file__).resolve().parent.parent
EXECUTABLE = REPO_ROOT / "name-sorter"


class NameSorterCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cwd = Path(self.tmp.name)
        self.input_file = self.cwd / "unsorted-names-list.txt"
        self.output_file = self.cwd / OUTPUT_FILE_NAME

    def run_name_sorter(self, *args: str) -> "subprocess.CompletedProcess[str]":
        # Invoke via the current interpreter so the test runs on whichever
        # Python is under test, rather than whatever "#!/usr/bin/env python3" finds.
        return subprocess.run(
            [sys.executable, str(EXECUTABLE), *args],
            cwd=self.cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_prints_the_sorted_names_and_writes_them_to_sorted_names_list_txt(self) -> None:
        self.input_file.write_text("\n".join(EXAMPLE_UNSORTED) + "\n")

        result = self.run_name_sorter("./unsorted-names-list.txt")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "\n".join(EXAMPLE_SORTED) + "\n")
        self.assertEqual(self.output_file.read_text(), "\n".join(EXAMPLE_SORTED) + "\n")

    def test_handles_a_thousand_names(self) -> None:
        lines = generate_names(1000, seed=7)
        self.input_file.write_text("\n".join(lines) + "\n")

        result = self.run_name_sorter("./unsorted-names-list.txt")

        self.assertEqual(result.returncode, 0, result.stderr)
        output_lines = result.stdout.splitlines()
        self.assertEqual(len(output_lines), 1000)
        self.assertEqual(sorted(output_lines), sorted(lines), "output must contain exactly the input names")
        self.assertEqual(self.output_file.read_text(), result.stdout, "file and screen must match")

    def test_overwrites_a_previous_sorted_names_list_txt(self) -> None:
        self.input_file.write_text("Leo Gardner\n")
        self.output_file.write_text("left over from last time\n")

        self.run_name_sorter("./unsorted-names-list.txt")

        self.assertEqual(self.output_file.read_text(), "Leo Gardner\n")

    def test_shows_usage_and_fails_when_no_file_is_given(self) -> None:
        result = self.run_name_sorter()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.strip(), USAGE)

    def test_shows_usage_and_fails_when_given_too_many_arguments(self) -> None:
        result = self.run_name_sorter("a.txt", "b.txt")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.strip(), USAGE)

    def test_reports_a_readable_error_when_the_input_file_is_missing(self) -> None:
        result = self.run_name_sorter("./does-not-exist.txt")

        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stderr, r"^Error: .*does-not-exist\.txt")
        self.assertEqual(result.stdout, "")
        self.assertFalse(self.output_file.exists())

    def test_reports_the_line_number_when_the_input_contains_an_invalid_name(self) -> None:
        self.input_file.write_text("Leo Gardner\nMadonna\n")

        result = self.run_name_sorter("./unsorted-names-list.txt")

        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stderr, r'unsorted-names-list\.txt:2: Invalid name "Madonna"')
        self.assertFalse(self.output_file.exists(), "nothing should be written when input is bad")

    def test_can_also_be_run_as_a_module(self) -> None:
        self.input_file.write_text("Janet Parsons\nMarin Alvarez\n")

        result = subprocess.run(
            [sys.executable, "-m", "name_sorter", "./unsorted-names-list.txt"],
            cwd=self.cwd,
            env={"PYTHONPATH": str(REPO_ROOT)},
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Marin Alvarez\nJanet Parsons\n")
