import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { describe, it } from 'node:test';
import { promisify } from 'node:util';
import { OUTPUT_FILE_NAME, USAGE } from '../src/cli.ts';
import { useTempDir } from './helpers/tempDir.ts';

/**
 * End-to-end: runs the real executable in a scratch working directory,
 * exactly as the assessors will, and checks the screen and file output.
 */

const executable = new URL('../bin/name-sorter.js', import.meta.url).pathname;

async function runNameSorter(cwd: string, ...args: string[]) {
  try {
    const { stdout, stderr } = await promisify(execFile)(process.execPath, [executable, ...args], { cwd });
    return { exitCode: 0, stdout, stderr };
  } catch (error) {
    const failed = error as { code: number; stdout: string; stderr: string };
    return { exitCode: failed.code, stdout: failed.stdout, stderr: failed.stderr };
  }
}

const unsorted = ['Janet Parsons', 'Adonis Julius Archer', 'Marin Alvarez'];
const sorted = ['Marin Alvarez', 'Adonis Julius Archer', 'Janet Parsons'];

describe('name-sorter CLI', () => {
  it('prints the sorted names and writes them to sorted-names-list.txt', async (t) => {
    const cwd = await useTempDir(t);
    await writeFile(join(cwd, 'unsorted-names-list.txt'), `${unsorted.join('\n')}\n`);

    const result = await runNameSorter(cwd, './unsorted-names-list.txt');

    assert.equal(result.exitCode, 0, result.stderr);
    assert.equal(result.stdout, `${sorted.join('\n')}\n`);
    assert.equal(await readFile(join(cwd, OUTPUT_FILE_NAME), 'utf8'), `${sorted.join('\n')}\n`);
  });

  it('overwrites a previous sorted-names-list.txt', async (t) => {
    const cwd = await useTempDir(t);
    await writeFile(join(cwd, 'unsorted-names-list.txt'), 'Leo Gardner\n');
    await writeFile(join(cwd, OUTPUT_FILE_NAME), 'left over from last time\n');

    await runNameSorter(cwd, './unsorted-names-list.txt');

    assert.equal(await readFile(join(cwd, OUTPUT_FILE_NAME), 'utf8'), 'Leo Gardner\n');
  });

  it('shows usage and fails when no file is given', async (t) => {
    const result = await runNameSorter(await useTempDir(t));

    assert.equal(result.exitCode, 1);
    assert.equal(result.stderr.trim(), USAGE);
  });

  it('shows usage and fails when given too many arguments', async (t) => {
    const result = await runNameSorter(await useTempDir(t), 'a.txt', 'b.txt');

    assert.equal(result.exitCode, 1);
    assert.equal(result.stderr.trim(), USAGE);
  });

  it('reports a readable error when the input file is missing', async (t) => {
    const result = await runNameSorter(await useTempDir(t), './does-not-exist.txt');

    assert.equal(result.exitCode, 1);
    assert.match(result.stderr, /^Error: .*does-not-exist\.txt/);
    assert.equal(result.stdout, '');
  });

  it('reports the line number when the input contains an invalid name', async (t) => {
    const cwd = await useTempDir(t);
    await writeFile(join(cwd, 'unsorted-names-list.txt'), 'Leo Gardner\nMadonna\n');

    const result = await runNameSorter(cwd, './unsorted-names-list.txt');

    assert.equal(result.exitCode, 1);
    assert.match(result.stderr, /unsorted-names-list\.txt:2: Invalid name "Madonna"/);
  });
});
