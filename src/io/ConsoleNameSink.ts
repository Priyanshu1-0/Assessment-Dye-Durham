import type { Name } from '../domain/Name.ts';
import type { NameSink } from './NameSink.ts';

/** The slice of a writable stream this sink needs; `process.stdout` satisfies it. */
export interface TextOutput {
  write(text: string): unknown;
}

/** Prints names to the screen, one per line. */
export class ConsoleNameSink implements NameSink {
  readonly #output: TextOutput;

  constructor(output: TextOutput = process.stdout) {
    this.#output = output;
  }

  async writeNames(names: readonly Name[]): Promise<void> {
    for (const name of names) {
      this.#output.write(`${name}\n`);
    }
  }
}
