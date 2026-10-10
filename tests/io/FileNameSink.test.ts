import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { describe, it } from 'node:test';
import { Name } from '../../src/domain/Name.ts';
import { FileNameSink } from '../../src/io/FileNameSink.ts';
import { useTempDir } from '../helpers/tempDir.ts';

const names = ['Marin Alvarez', 'Adonis Julius Archer'].map((line) => Name.parse(line));

describe('FileNameSink', () => {
  it('writes one name per line with a trailing newline', async (t) => {
    const file = join(await useTempDir(t), 'out.txt');

    await new FileNameSink(file).writeNames(names);

    assert.equal(await readFile(file, 'utf8'), 'Marin Alvarez\nAdonis Julius Archer\n');
  });

  it('overwrites an existing file rather than appending to it', async (t) => {
    const file = join(await useTempDir(t), 'out.txt');
    await writeFile(file, 'stale content that should disappear\n');

    await new FileNameSink(file).writeNames(names);

    assert.equal(await readFile(file, 'utf8'), 'Marin Alvarez\nAdonis Julius Archer\n');
  });

  it('writes an empty file for an empty list', async (t) => {
    const file = join(await useTempDir(t), 'out.txt');

    await new FileNameSink(file).writeNames([]);

    assert.equal(await readFile(file, 'utf8'), '');
  });
});
