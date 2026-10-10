import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { describe, it } from 'node:test';
import { FileNameSource } from '../../src/io/FileNameSource.ts';
import { useTempDir } from '../helpers/tempDir.ts';

describe('FileNameSource', () => {
  it('reads one name per line', async (t) => {
    const file = join(await useTempDir(t), 'names.txt');
    await writeFile(file, 'Janet Parsons\nAdonis Julius Archer\n');

    const names = await new FileNameSource(file).readNames();

    assert.deepEqual(names.map(String), ['Janet Parsons', 'Adonis Julius Archer']);
  });

  it('copes with Windows line endings', async (t) => {
    const file = join(await useTempDir(t), 'names.txt');
    await writeFile(file, 'Janet Parsons\r\nLeo Gardner\r\n');

    const names = await new FileNameSource(file).readNames();

    assert.deepEqual(names.map(String), ['Janet Parsons', 'Leo Gardner']);
  });

  it('skips blank lines', async (t) => {
    const file = join(await useTempDir(t), 'names.txt');
    await writeFile(file, '\nJanet Parsons\n   \n\nLeo Gardner');

    const names = await new FileNameSource(file).readNames();

    assert.deepEqual(names.map(String), ['Janet Parsons', 'Leo Gardner']);
  });

  it('returns an empty list for an empty file', async (t) => {
    const file = join(await useTempDir(t), 'names.txt');
    await writeFile(file, '');

    assert.deepEqual(await new FileNameSource(file).readNames(), []);
  });

  it('fails with the file path and line number when a line is not a valid name', async (t) => {
    const file = join(await useTempDir(t), 'names.txt');
    await writeFile(file, 'Janet Parsons\n\nCher\nLeo Gardner\n');

    await assert.rejects(
      new FileNameSource(file).readNames(),
      (error: Error) => error.message.startsWith(`${file}:3: Invalid name "Cher"`),
    );
  });

  it('fails when the file does not exist', async (t) => {
    const missing = join(await useTempDir(t), 'nope.txt');

    await assert.rejects(new FileNameSource(missing).readNames(), { code: 'ENOENT' });
  });
});
