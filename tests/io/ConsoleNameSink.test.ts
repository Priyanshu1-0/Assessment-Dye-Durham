import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { Name } from '../../src/domain/Name.ts';
import { ConsoleNameSink } from '../../src/io/ConsoleNameSink.ts';

describe('ConsoleNameSink', () => {
  it('prints each name on its own line', async () => {
    let printed = '';
    const sink = new ConsoleNameSink({ write: (text) => (printed += text) });

    await sink.writeNames([Name.parse('Marin Alvarez'), Name.parse('Adonis Julius Archer')]);

    assert.equal(printed, 'Marin Alvarez\nAdonis Julius Archer\n');
  });

  it('prints nothing for an empty list', async () => {
    let printed = '';
    const sink = new ConsoleNameSink({ write: (text) => (printed += text) });

    await sink.writeNames([]);

    assert.equal(printed, '');
  });
});
