import {Decimal} from 'decimal.js';

// Adapted from:
// https://en.wikipedia.org/wiki/Integer_square_root#Using_bitwise_operations
export function isqrt(n: Decimal): Decimal {
  let op = n;
  let res = new Decimal(0);
  let twoPow = new Decimal(1);
  while (twoPow.lte(op)) {
    twoPow = twoPow.times(4);
  }
  twoPow = twoPow.div(4).floor();

  while (!twoPow.isZero()) {
    const dltaSqr = res.add(twoPow);
    if (op.gte(dltaSqr)) {
      op = op.minus(dltaSqr);
      res = res.add(twoPow.times(2));
    }
    res = res.div(2).floor();
    twoPow = twoPow.div(4).floor();
  }
  return res;
}

export function factorial(n: Decimal): Decimal {
  let i = n;
  let result = new Decimal(1);
  while (i.gt(1)) {
    result = result.times(i);
    i = i.minus(1);
  }
  return result;
}

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
