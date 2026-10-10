import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { Name } from '../../src/domain/Name.ts';
import { CompositeNameSink } from '../../src/io/CompositeNameSink.ts';
import { InMemoryNameSink } from '../helpers/InMemoryNameSink.ts';

describe('CompositeNameSink', () => {
  it('writes the same names to every sink', async () => {
    const first = new InMemoryNameSink();
    const second = new InMemoryNameSink();
    const names = [Name.parse('Marin Alvarez')];

    await new CompositeNameSink([first, second]).writeNames(names);

    assert.deepEqual(first.lastWritten, ['Marin Alvarez']);
    assert.deepEqual(second.lastWritten, ['Marin Alvarez']);
  });

  it('writes to sinks in the order they were given', async () => {
    const order: string[] = [];
    const sinkNamed = (label: string) => ({
      writeNames: async () => {
        order.push(label);
      },
    });

    await new CompositeNameSink([sinkNamed('screen'), sinkNamed('file')]).writeNames([]);

    assert.deepEqual(order, ['screen', 'file']);
  });

  it('does nothing when it has no sinks', async () => {
    await assert.doesNotReject(new CompositeNameSink([]).writeNames([Name.parse('Marin Alvarez')]));
  });
});
