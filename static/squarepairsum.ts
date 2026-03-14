import Decimal from 'decimal.js';
import isqrt from 'bigint-isqrt';


export async function score(nums: Decimal[]): Promise<bigint | string> {
  const N = 6;
  // Make sure only 6 integers are supplied.
  if (nums.length != N) {
    return "Must submit 6 numbers!";
  }
 
  const smlNums = nums.map((num) => num.toNumber());
  const sums: number[] = [];
  for (let i = 0; i < smlNums.length; i++) {
    for (let j = i+1; j < smlNums.length; j++) {
      sums.push(Math.abs(smlNums[i] + smlNums[j]));
    }
  }

  for (const sum of sums) {
    if (isqrt(sum) ** 2 != sum) {
      return "A pair of numbers does not sum to a square!";
    }
  }

  return BigInt(Math.max(...smlNums));
}
