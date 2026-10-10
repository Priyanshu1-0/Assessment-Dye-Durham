/**
 * A person's name, split into the parts the sorter cares about.
 *
 * A name is parsed from a single line of text such as
 * "Hunter Uriah Mathew Clarke": the final word is the last name and every
 * word before it is a given name. The assessment requires at least one and
 * at most three given names, so "Clarke" alone or a name with four given
 * names is rejected.
 */
export class Name {
  static readonly MIN_GIVEN_NAMES = 1;
  static readonly MAX_GIVEN_NAMES = 3;

  readonly givenNames: readonly string[];
  readonly lastName: string;

  private constructor(givenNames: readonly string[], lastName: string) {
    this.givenNames = givenNames;
    this.lastName = lastName;
  }

  /**
   * Parses a line of text into a Name.
   *
   * Surrounding whitespace is ignored and any run of whitespace between
   * words is treated as a single separator.
   *
   * @throws {InvalidNameError} if the text is blank or has the wrong
   *   number of given names.
   */
  static parse(text: string): Name {
    const words = text.trim().split(/\s+/).filter((word) => word !== '');

    if (words.length === 0) {
      throw new InvalidNameError(text, 'a name cannot be blank');
    }

    const lastName = words[words.length - 1]!;
    const givenNames = words.slice(0, -1);

    if (givenNames.length < Name.MIN_GIVEN_NAMES || givenNames.length > Name.MAX_GIVEN_NAMES) {
      throw new InvalidNameError(
        text,
        `a name must have between ${Name.MIN_GIVEN_NAMES} and ${Name.MAX_GIVEN_NAMES} given names ` +
          `followed by a last name, but found ${givenNames.length} given name(s)`,
      );
    }

    return new Name(givenNames, lastName);
  }

  /** The full name with single spaces between words, e.g. "Adonis Julius Archer". */
  toString(): string {
    return [...this.givenNames, this.lastName].join(' ');
  }
}

/** Raised when a line of text cannot be understood as a valid name. */
export class InvalidNameError extends Error {
  readonly input: string;

  constructor(input: string, reason: string) {
    super(`Invalid name "${input.trim()}": ${reason}`);
    this.name = 'InvalidNameError';
    this.input = input;
  }
}
