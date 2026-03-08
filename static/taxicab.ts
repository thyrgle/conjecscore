import Decimal from 'decimal.js';
import * as math from 'mathjs';
// TODO? I want to use mathjs, but the typing for variance seems wrong?
import {variance} from './utils.js';

export async function score(nums: Decimal[]): Promise<number | string> {
  try {
    const numbers = nums.map((num) => num.toNumber());
    if (numbers.length != 4) {
      return "Need 4 numbers!";
    }
    const dupCheck = new Set<number>(numbers);
    if (dupCheck.size != 4) {
      return "Not all numbers are distinct!";
    }
    for (const num of numbers) {
      if (num <= 0) {
        return "All numbers must be positive!";
      }
    }
    const [a, b, c, d] = numbers;

    const lhs = a ** 5 + b ** 5;
    const rhs = c ** 5 + d ** 5;
    const M = Math.max(lhs, rhs);
    const m = Math.min(lhs, rhs);
    const me = math.mean([lhs, rhs]);
    const vr = variance(numbers);
    return Math.floor(((M - m) * (10 ** 6))  / (math.log(me) * vr));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
