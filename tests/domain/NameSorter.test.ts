import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { Name } from '../../src/domain/Name.ts';
import { byLastNameThenGivenNames, type NameComparer } from '../../src/domain/NameOrdering.ts';
import { NameSorter } from '../../src/domain/NameSorter.ts';

const parseAll = (lines: string[]) => lines.map((line) => Name.parse(line));
const asStrings = (names: Name[]) => names.map(String);

describe('NameSorter', () => {
  it('sorts the example from the assessment into the expected order', () => {
    const unsorted = parseAll([
      'Janet Parsons',
      'Vaughn Lewis',
      'Adonis Julius Archer',
      'Shelby Nathan Yoder',
      'Marin Alvarez',
      'London Lindsey',
      'Beau Tristan Bentley',
      'Leo Gardner',
      'Hunter Uriah Mathew Clarke',
      'Mikayla Lopez',
      'Frankie Conner Ritter',
    ]);

    const sorted = new NameSorter(byLastNameThenGivenNames).sort(unsorted);

    assert.deepEqual(asStrings(sorted), [
      'Marin Alvarez',
      'Adonis Julius Archer',
      'Beau Tristan Bentley',
      'Hunter Uriah Mathew Clarke',
      'Leo Gardner',
      'Vaughn Lewis',
      'London Lindsey',
      'Mikayla Lopez',
      'Janet Parsons',
      'Frankie Conner Ritter',
      'Shelby Nathan Yoder',
    ]);
  });

  it('leaves the input array untouched', () => {
    const unsorted = parseAll(['Zoe Young', 'Adam Abbott']);
    const snapshot = asStrings(unsorted);

    new NameSorter(byLastNameThenGivenNames).sort(unsorted);

    assert.deepEqual(asStrings(unsorted), snapshot);
  });

  it('returns an empty list for an empty list', () => {
    assert.deepEqual(new NameSorter(byLastNameThenGivenNames).sort([]), []);
  });

  it('keeps equivalent names in their original order', () => {
    const unsorted = parseAll(['adam smith', 'Adam Smith', 'ADAM SMITH']);

    const sorted = new NameSorter(byLastNameThenGivenNames).sort(unsorted);

    assert.deepEqual(asStrings(sorted), ['adam smith', 'Adam Smith', 'ADAM SMITH']);
  });

  it('defers entirely to the comparer it is given', () => {
    const byLastNameLengthDescending: NameComparer = (a, b) => b.lastName.length - a.lastName.length;
    const unsorted = parseAll(['A Li', 'B Anderson', 'C Smith']);

    const sorted = new NameSorter(byLastNameLengthDescending).sort(unsorted);

    assert.deepEqual(asStrings(sorted), ['B Anderson', 'C Smith', 'A Li']);
  });
});
