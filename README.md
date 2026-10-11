# name-sorter

Sorts a list of names by **last name**, then by **given names**.

Given a file with one name per line:

```
Janet Parsons
Vaugh Lewis
Adonis Julius Archer
```

running `name-sorter ./unsorted-names-list.txt` prints the sorted names to the
screen and writes the same list to `./sorted-names-list.txt`
(overwriting it if it already exists):

```
Adonis Julius Archer
Vaugh Lewis
Janet Parsons
```

## Requirements

Python 3.9 or newer. Nothing else: the program and its tests use only the
standard library, so there is nothing to install.

## Usage

```sh
./name-sorter ./unsorted-names-list.txt
```

Equivalent alternatives:

```sh
python3 -m name_sorter ./unsorted-names-list.txt   # as a module
pip install . && name-sorter ./unsorted-names-list.txt   # as an installed command
```

A sample `unsorted-names-list.txt` is included in the repository.

## Running the tests

```sh
python3 -m unittest            # add -v for one line per test
```

The suite covers each module in isolation, a generated thousand-name list,
and an end-to-end run of the real `name-sorter` executable.

## The rules, precisely

- A name is one or more **given names** followed by a **last name**, separated
  by spaces. The last word on a line is always the last name.
- A name must have **1 to 3 given names**. Anything else (including a blank
  name) is rejected.
- Names are ordered by last name, then by first given name, then second, then
  third. Where one name's given names are a prefix of another's, the shorter
  name comes first (`Leo Gardner` before `Leo Alan Gardner`).
- Comparison is case-insensitive. Names that compare equal keep the order
  they appeared in the input.
- Blank lines in the input are ignored. Any other invalid line stops the
  program with an error naming the file and line number, and nothing is
  written. Fixing the data is better than silently dropping a person.

## How the code is organised

```
name-sorter               executable; just calls name_sorter.cli.main
name_sorter/
  cli.py                  composition root: parses args, wires everything together
  app.py                  NameSorterApp: read -> sort -> write, against the interfaces below
  name.py                 Name value object; parsing and validation of a single name
  ordering.py             the comparison rule (a sort key) described above
  sorter.py               NameSorter: sorts a list using whichever key it is given
  sources.py              NameSource interface + FileNameSource (one name per line)
  sinks.py                NameSink interface + Console, File and Composite sinks
tests/                    one test module per source module, plus test_cli.py end-to-end
```

Each class has a single job. `NameSorterApp` depends on the `NameSource`,
`NameSink` and `NameSortKey` abstractions rather than on files or the console,
so a new destination or ordering is a new class, not a change to an existing
one. The only place that knows about concrete types is `cli.py`.
