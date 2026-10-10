import type { Name } from './Name.ts';

/**
 * Decides the relative order of two names, following the usual comparator
 * contract: negative if `a` comes first, positive if `b` comes first, zero
 * if they are equivalent.
 *
 * `NameSorter` accepts any `NameComparer`, so a different ordering (say,
 * by first name) can be introduced without touching the sorter.
 */
export type NameComparer = (a: Name, b: Name) => number;

/**
 * A fixed locale keeps the ordering identical on every machine regardless
 * of the host's regional settings. "base" sensitivity makes the comparison
 * case- and accent-insensitive, so "mcdonald" and "McDonald" are neighbours.
 */
const collator = new Intl.Collator('en', { sensitivity: 'base' });

/**
 * The ordering required by the assessment: by last name first, then by
 * each given name in turn.
 *
 * When one name's given names are a prefix of another's (e.g. "Leo Gardner"
 * and "Leo Alan Gardner"), the shorter name comes first.
 */
export const byLastNameThenGivenNames: NameComparer = (a, b) => {
  const lastNameOrder = collator.compare(a.lastName, b.lastName);
  if (lastNameOrder !== 0) {
    return lastNameOrder;
  }
  return compareWordByWord(a.givenNames, b.givenNames);
};

function compareWordByWord(a: readonly string[], b: readonly string[]): number {
  const sharedLength = Math.min(a.length, b.length);

  for (let i = 0; i < sharedLength; i++) {
    const wordOrder = collator.compare(a[i]!, b[i]!);
    if (wordOrder !== 0) {
      return wordOrder;
    }
  }

  return a.length - b.length;
}
