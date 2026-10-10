"""The command-line entry point and composition root.

This is the one place that knows about concrete classes. It turns the
command-line arguments into a configured ``NameSorterApp``, runs it, and
translates the outcome into an exit code.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Optional, TextIO

from name_sorter.app import NameSorterApp
from name_sorter.ordering import by_last_name_then_given_names
from name_sorter.sinks import CompositeNameSink, ConsoleNameSink, FileNameSink
from name_sorter.sorter import NameSorter
from name_sorter.sources import FileNameSource, NameFileError

OUTPUT_FILE_NAME = "sorted-names-list.txt"
"""The sorted names are always written here, relative to the working directory."""

USAGE = f"""Usage: name-sorter <path-to-unsorted-names-list>

Sorts the names in the given file by last name, then by given names.
The result is printed to the screen and written to ./{OUTPUT_FILE_NAME}."""

EXIT_OK = 0
EXIT_FAILURE = 1


def main(
    argv: Optional[Sequence[str]] = None,
    stdout: Optional[TextIO] = None,
    stderr: Optional[TextIO] = None,
) -> int:
    """Run the program and return its exit code.

    ``argv`` is the list of arguments *excluding* the program name; it
    defaults to the real command line. The streams default to the real
    ``sys.stdout`` / ``sys.stderr`` and exist so tests can capture output.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    if len(args) != 1:
        print(USAGE, file=stderr)
        return EXIT_FAILURE

    input_file_path = args[0]
    app = NameSorterApp(
        source=FileNameSource(input_file_path),
        sorter=NameSorter(by_last_name_then_given_names),
        sink=CompositeNameSink([ConsoleNameSink(stdout), FileNameSink(OUTPUT_FILE_NAME)]),
    )

    try:
        app.run()
    except (OSError, NameFileError) as error:
        # These are the failures a user can do something about (missing or
        # unreadable file, a bad line). Anything else is a bug and is left
        # to surface with a full traceback.
        print(f"Error: {error}", file=stderr)
        return EXIT_FAILURE

    return EXIT_OK
