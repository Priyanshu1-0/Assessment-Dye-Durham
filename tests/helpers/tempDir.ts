import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import type { TestContext } from 'node:test';

/**
 * Creates a throwaway directory for a test to read and write files in,
 * and removes it once the test finishes.
 */
export async function useTempDir(t: TestContext): Promise<string> {
  const dir = await mkdtemp(join(tmpdir(), 'name-sorter-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
