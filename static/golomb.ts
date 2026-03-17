import Decimal from 'decimal.js';

export async function score(nums: Decimal[]): Promise<bigint | string> {
  const N = 213;
  // Make sure only 3 integers are supplied.
  if (nums.length != N) {
    console.log(nums.length);
    return "Must submit 213 numbers!";
  }
 
  const smlNums = nums.map((num) => num.toNumber());
  const diffs: number[] = [];
  for (let i = 0; i < smlNums.length; i++) {
    for (let j = i+1; j < smlNums.length; j++) {
      diffs.push(Math.abs(smlNums[i] - smlNums[j]));
    }
  }

  const setDiffs = new Set(diffs);
  if (diffs.length != setDiffs.size) {
    return "Not a Golomb ruler!";
  }
  return BigInt(Math.max(...smlNums) - Math.min(...smlNums));
}
