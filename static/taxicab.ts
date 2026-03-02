import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {mean, variance} from './utils.js';

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

    const lhs = (a.toPower(5).plus(b.toPower(5)));
    const rhs = (c.toPower(5).plus(d.toPower(5)));
    const M = Decimal.max(lhs, rhs);
    const m = Decimal.min(lhs, rhs);
    const me = mean([lhs, rhs]);
    const vr = variance(nums);
    const mil = new Decimal(10 ** 6);
    return Decimal.floor(M.sub(m).div(Decimal.ln(me).mul(vr)).mul(mil));
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
