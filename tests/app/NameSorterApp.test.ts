import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { NameSorterApp } from '../../src/app/NameSorterApp.ts';
import { Name } from '../../src/domain/Name.ts';
import { byLastNameThenGivenNames } from '../../src/domain/NameOrdering.ts';
import { NameSorter } from '../../src/domain/NameSorter.ts';
import type { NameSource } from '../../src/io/NameSource.ts';
import { InMemoryNameSink } from '../helpers/InMemoryNameSink.ts';

const sourceOf = (lines: string[]): NameSource => ({
  readNames: async () => lines.map((line) => Name.parse(line)),
});

describe('NameSorterApp', () => {
  it('reads from the source, sorts, and writes the result to the sink', async () => {
    const sink = new InMemoryNameSink();
    const app = new NameSorterApp(
      sourceOf(['Janet Parsons', 'Marin Alvarez', 'Leo Gardner']),
      new NameSorter(byLastNameThenGivenNames),
      sink,
    );

    await app.run();

    assert.deepEqual(sink.lastWritten, ['Marin Alvarez', 'Leo Gardner', 'Janet Parsons']);
  });

  it('writes nothing to the sink if the source fails', async () => {
    const sink = new InMemoryNameSink();
    const brokenSource: NameSource = {
      readNames: async () => {
        throw new Error('disk on fire');
      },
    };
    const app = new NameSorterApp(brokenSource, new NameSorter(byLastNameThenGivenNames), sink);

    await assert.rejects(app.run(), { message: 'disk on fire' });
    assert.equal(sink.writes.length, 0);
  });
});
