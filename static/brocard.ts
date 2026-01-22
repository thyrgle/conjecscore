import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {factorial, isqrt} from './utils.js';

function score(nums: Decimal[]) {
  try {
    if (nums.length != 1) {
      return "Need only 1 number!";
    }
    const num = nums[0]
    if (num.lte(0)) {
      return "All numbers must be positive!";
    }
    const bil = new Decimal(10 ** 9);
    const one = new Decimal(1);
    const nFactOne = factorial(num).add(1);
    let smlSqr = isqrt(nFactOne);
    const bigSqr = (smlSqr.add(one)).times(smlSqr.add(one));
    smlSqr = smlSqr.times(smlSqr);
    console.log(nFactOne);
    console.log(smlSqr);
    console.log(bigSqr);
    return Decimal.min(nFactOne.minus(smlSqr), bigSqr.minus(nFactOne))
                  .div(bigSqr.minus(smlSqr)).times(bil).floor();
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv", "/problems/brocard-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
