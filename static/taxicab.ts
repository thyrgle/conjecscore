import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';

function longestPrefix(s1: string, s2: string): Decimal {
  let result = new Decimal(0);
  try {
    // Skip '0b'
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

function reverse(s: string) {
  return s.split('').reverse().join('');
}

function score(nums: Decimal[]) {
  try {
    if (nums.length != 4) {
      return "Need 4 numbers!";
    }
    const dup_check = new Set<Decimal>(nums);
    if (dup_check.size != 4) {
      return "Not all numbers are distinct!";
    }
    for (const num of nums) {
      if (num.lte(0)) {
        return "All numbers must be positive!";
      }
    }
    const [a, b, c, d] = nums;
    const big = reverse((a.toPower(5).plus(b.toPower(5))).toBinary().slice(2));
    const small = reverse((c.toPower(5).plus(d.toPower(5))).toBinary().slice(2));
    console.log(big);
    console.log(small);
    const size = big.length;
    if (size != small.length) {
      return new Decimal(10 ** 6);
    }
    const pre = longestPrefix(big, small);
    console.log("HERE??");
    const mil = new Decimal(10 ** 6);
    const one = new Decimal(1);
    return Decimal.floor((one.minus(pre.div(new Decimal(size)))).mul(mil));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv", "/problems/taxicab-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
