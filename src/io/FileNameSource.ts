import { readFile } from 'node:fs/promises';
import { InvalidNameError, Name } from '../domain/Name.ts';
import type { NameSource } from './NameSource.ts';

/**
 * Reads names from a plain-text file with one name per line.
 *
 * Blank lines are skipped. Any other line that is not a valid name stops
 * the read with an error that names the offending line, so a typo in a
 * thousand-name file is easy to find and fix.
 */
export class FileNameSource implements NameSource {
  readonly #filePath: string;

  constructor(filePath: string) {
    this.#filePath = filePath;
  }

  async readNames(): Promise<Name[]> {
    const contents = await readFile(this.#filePath, 'utf8');
    const lines = contents.split(/\r?\n/);
    const names: Name[] = [];

    lines.forEach((line, index) => {
      if (line.trim() === '') {
        return;
      }
      names.push(this.#parseLine(line, index + 1));
    });

    return names;
  }

  #parseLine(line: string, lineNumber: number): Name {
    try {
      return Name.parse(line);
    } catch (error) {
      if (error instanceof InvalidNameError) {
        throw new Error(`${this.#filePath}:${lineNumber}: ${error.message}`, { cause: error });
      }
      throw error;
    }
  }
}
