import type { Name } from './Name.ts';
import type { NameComparer } from './NameOrdering.ts';

/**
 * Sorts names using whichever ordering it is given.
 *
 * The sorter owns the mechanics of sorting (never mutating its input,
 * keeping equal names in their original order) while the injected
 * `NameComparer` owns the business rule of what "sorted" means.
 */
export class NameSorter {
  readonly #compare: NameComparer;

  constructor(compare: NameComparer) {
    this.#compare = compare;
  }

  /** Returns a new, sorted array; the original is left untouched. */
  sort(names: readonly Name[]): Name[] {
    // Array.prototype.sort is stable, so names the comparer considers
    // equivalent keep the order they were read in.
    return [...names].sort(this.#compare);
  }
}
