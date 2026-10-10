import type { Name } from '../domain/Name.ts';

/** Somewhere names can be read from, e.g. a file. */
export interface NameSource {
  readNames(): Promise<Name[]>;
}
