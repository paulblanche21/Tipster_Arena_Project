const assert = require('assert');
const { calculateSum } = require('./your-code-filepath');

describe('calculateSum', () => {
  it('should return the correct sum when given valid input', () => {
    const result = calculateSum([1, 2, 3]);
    assert.strictEqual(result, 6);
  });

  it('should throw an error when given invalid input', () => {
    assert.throws(() => calculateSum('not an array'), TypeError);
  });

  it('should return 0 when given an empty array', () => {
    const result = calculateSum([]);
    assert.strictEqual(result, 0);
  });
});