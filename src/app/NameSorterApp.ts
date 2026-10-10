import type { NameSorter } from '../domain/NameSorter.ts';
import type { NameSink } from '../io/NameSink.ts';
import type { NameSource } from '../io/NameSource.ts';

/**
 * The whole program in one sentence: read names, sort them, write them out.
 *
 * The app knows nothing about files or the console; it is handed a source,
 * a sorter and a sink, and the entry point (`src/cli.ts`) decides what those
 * are. That keeps this class trivial to test with in-memory stand-ins.
 */
export class NameSorterApp {
  readonly #source: NameSource;
  readonly #sorter: NameSorter;
  readonly #sink: NameSink;

  constructor(source: NameSource, sorter: NameSorter, sink: NameSink) {
    this.#source = source;
    this.#sorter = sorter;
    this.#sink = sink;
  }

  async run(): Promise<void> {
    const names = await this.#source.readNames();
    const sortedNames = this.#sorter.sort(names);
    await this.#sink.writeNames(sortedNames);
  }
}
