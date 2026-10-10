import type { Name } from '../domain/Name.ts';
import type { NameSink } from './NameSink.ts';

/**
 * Fans a single write out to several sinks, in the order they were given.
 *
 * This lets the application write "to the screen and to a file" while
 * only ever talking to one `NameSink`.
 */
export class CompositeNameSink implements NameSink {
  readonly #sinks: readonly NameSink[];

  constructor(sinks: readonly NameSink[]) {
    this.#sinks = sinks;
  }

  async writeNames(names: readonly Name[]): Promise<void> {
    for (const sink of this.#sinks) {
      await sink.writeNames(names);
    }
  }
}
