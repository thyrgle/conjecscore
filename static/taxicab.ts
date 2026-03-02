import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {longestPrefix} from './utils.js';

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

    const big = (a.toPower(5).plus(b.toPower(5))).toBinary().slice(2);
    const small = (c.toPower(5).plus(d.toPower(5))).toBinary().slice(2);
    const size = big.length;
    if (size != small.length) {
      return new Decimal(10 ** 6);
    }
    const pre = longestPrefix(big, small);
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
