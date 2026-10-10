import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { InvalidNameError, Name } from '../../src/domain/Name.ts';

describe('Name.parse', () => {
  it('treats the last word as the last name and the rest as given names', () => {
    const name = Name.parse('Hunter Uriah Mathew Clarke');

    assert.deepEqual(name.givenNames, ['Hunter', 'Uriah', 'Mathew']);
    assert.equal(name.lastName, 'Clarke');
  });

  it('accepts a single given name', () => {
    const name = Name.parse('Leo Gardner');

    assert.deepEqual(name.givenNames, ['Leo']);
    assert.equal(name.lastName, 'Gardner');
  });

  it('ignores surrounding whitespace and collapses repeated spaces', () => {
    const name = Name.parse('   Janet \t  Parsons  ');

    assert.deepEqual(name.givenNames, ['Janet']);
    assert.equal(name.lastName, 'Parsons');
  });

  it('rejects a blank line', () => {
    assert.throws(() => Name.parse('   '), InvalidNameError);
  });

  it('rejects a name with no given names', () => {
    assert.throws(() => Name.parse('Clarke'), InvalidNameError);
  });

  it('rejects a name with more than three given names', () => {
    assert.throws(() => Name.parse('One Two Three Four Clarke'), InvalidNameError);
  });

  it('explains what went wrong, quoting the offending text', () => {
    assert.throws(
      () => Name.parse('Clarke'),
      (error: unknown) =>
        error instanceof InvalidNameError &&
        error.input === 'Clarke' &&
        error.message.includes('"Clarke"') &&
        error.message.includes('between 1 and 3 given names'),
    );
  });
});

describe('Name.toString', () => {
  it('joins the given names and last name with single spaces', () => {
    assert.equal(String(Name.parse('  Adonis   Julius Archer ')), 'Adonis Julius Archer');
  });
});
