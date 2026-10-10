# name-sorter

Sorts a list of names by **last name**, then by **given names**.

Given a file with one name per line:

```
Janet Parsons
Vaughn Lewis
Adonis Julius Archer
```

running `name-sorter ./unsorted-names-list.txt` prints the sorted names to the
screen and writes the same list to `./sorted-names-list.txt`
(overwriting it if it already exists):

```
Adonis Julius Archer
Vaughn Lewis
Janet Parsons
```

## Requirements

- [Node.js](https://nodejs.org) 24 or newer. There is no build step: Node runs
  the TypeScript sources directly.

## Usage

```sh
npm install                                  # dev tooling only (TypeScript for type-checking)
./bin/name-sorter.js ./unsorted-names-list.txt
```

or, equivalently, `npm start -- ./unsorted-names-list.txt`.

A sample `unsorted-names-list.txt` is included in the repository.

## Running the tests

```sh
npm test            # unit tests + an end-to-end test of the executable
npm run typecheck   # tsc, strict mode
```

## The rules, precisely

- A name is one or more **given names** followed by a **last name**, separated
  by spaces. The last word on a line is always the last name.
- A name must have **1 to 3 given names**. Anything else (including a blank
  name) is rejected.
- Names are ordered by last name, then by first given name, then second, then
  third. Where one name's given names are a prefix of another's, the shorter
  name comes first (`Leo Gardner` before `Leo Alan Gardner`).
- Comparison is case-insensitive and uses a fixed English locale, so the
  output is the same on every machine. Names that compare equal keep the
  order they appeared in the input.
- Blank lines in the input are ignored. Any other invalid line stops the
  program with an error naming the file and line number, and nothing is
  written. Fixing the data is better than silently dropping a person.

## How the code is organised

```
bin/name-sorter.js      executable; just calls src/cli.ts
src/
  cli.ts                composition root: parses args, wires everything together
  app/NameSorterApp.ts  read -> sort -> write, against the interfaces below
  domain/
    Name.ts             value object; parsing and validation of a single name
    NameOrdering.ts     the comparison rule (NameComparer) described above
    NameSorter.ts       sorts a list using whichever NameComparer it is given
  io/
    NameSource.ts       interface: where names come from
    NameSink.ts         interface: where names go
    FileNameSource.ts   one name per line from a text file
    FileNameSink.ts     one name per line to a text file
    ConsoleNameSink.ts  one name per line to the screen
    CompositeNameSink.ts  writes to several sinks (screen + file)
tests/                  mirrors src/; tests/cli.test.ts runs the real executable
```

Each class has a single job, the application depends on the `NameSource` /
`NameSink` / `NameComparer` abstractions rather than on files or the console,
and new destinations or orderings can be added without changing existing
classes. The only place that knows about concrete types is `src/cli.ts`.
