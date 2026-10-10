import { writeFile } from 'node:fs/promises';
import type { Name } from '../domain/Name.ts';
import type { NameSink } from './NameSink.ts';

/**
 * Writes names to a plain-text file, one per line, replacing whatever the
 * file previously contained.
 */
export class FileNameSink implements NameSink {
  readonly #filePath: string;

  constructor(filePath: string) {
    this.#filePath = filePath;
  }

  async writeNames(names: readonly Name[]): Promise<void> {
    const lines = names.map((name) => `${name}\n`).join('');
    await writeFile(this.#filePath, lines, 'utf8');
  }
}
