import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { Name } from '../../src/domain/Name.ts';
import { byLastNameThenGivenNames } from '../../src/domain/NameOrdering.ts';

const compare = (a: string, b: string) => byLastNameThenGivenNames(Name.parse(a), Name.parse(b));

describe('byLastNameThenGivenNames', () => {
  it('orders by last name before anything else', () => {
    assert.ok(compare('Zoe Adams', 'Aaron Brown') < 0);
    assert.ok(compare('Aaron Brown', 'Zoe Adams') > 0);
  });

  it('breaks last-name ties using the first given name', () => {
    assert.ok(compare('Adam Smith', 'Zoe Smith') < 0);
  });

  it('then moves on to the second and third given names', () => {
    assert.ok(compare('Adam Bob Smith', 'Adam Carl Smith') < 0);
    assert.ok(compare('Adam Bob Carl Smith', 'Adam Bob Dave Smith') < 0);
  });

  it('puts a name with fewer given names first when the shared ones match', () => {
    assert.ok(compare('Leo Gardner', 'Leo Alan Gardner') < 0);
    assert.ok(compare('Leo Alan Gardner', 'Leo Gardner') > 0);
  });

  it('ignores letter case', () => {
    assert.equal(compare('adam smith', 'Adam Smith'), 0);
    assert.ok(compare('adam smith', 'Adam Smyth') < 0);
  });

  it('reports equal names as equivalent', () => {
    assert.equal(compare('Marin Alvarez', 'Marin Alvarez'), 0);
  });
});
