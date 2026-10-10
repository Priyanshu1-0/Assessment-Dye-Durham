import type { Name } from '../domain/Name.ts';

/** Somewhere names can be written to, e.g. the screen or a file. */
export interface NameSink {
  writeNames(names: readonly Name[]): Promise<void>;
}
