import {Decimal} from 'decimal.js';

export function longestPrefix(s1: string, s2: string): Decimal {
  let result = new Decimal(0);
  try {
    let i = 0;
    while (s1[i] == s2[i] && i < s1.length) {
      result = result.plus(1);
      i += 1;
    }
    return result;
  } catch (e) {
    console.log(e);
    return result;
  }
}

export function mean(numbers: Decimal[]) {
  let result = new Decimal(0);
  for (const num of numbers) {
    result = result.plus(num);
  }
  return result.div(numbers.length);
}

export function reverse(s: string) {
  return s.split('').reverse().join('');
}

export function removeTwoPow(nums: Decimal[]): Decimal[] {
  const isEven = (val) => val.mod(2).eq(0);
  while (nums.every(isEven)) {
    nums = nums.map((x) => x.div(2));
  }
  return nums
}
