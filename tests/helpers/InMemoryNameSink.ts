import type { Name } from '../../src/domain/Name.ts';
import type { NameSink } from '../../src/io/NameSink.ts';

/** A `NameSink` that simply remembers what it was asked to write. */
export class InMemoryNameSink implements NameSink {
  readonly writes: (readonly Name[])[] = [];

  async writeNames(names: readonly Name[]): Promise<void> {
    this.writes.push(names);
  }

  /** The names from the most recent write, as plain strings. */
  get lastWritten(): string[] {
    const last = this.writes[this.writes.length - 1] ?? [];
    return last.map(String);
  }
}
