import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import * as math from 'mathjs';

function score(nums: [Decimal]) {
  try {
    if (nums.length != 23 * 23) {
      return "Not a 23 × 23 matrix!";
    }
    // Don't need high precision for this.
    const small_nums = nums.map((num) => num.toNumber());
    const onePmOne = (num) => num == 1 || num == -1;
    if (small_nums.every(onePmOne)) {
      const mat = math.reshape(math.matrix(small_nums), [23, 23]);
      return new Decimal(math.det(mat)).div(10 ** 9).floor();
    } else {
      return "All entries must be ±1!";
    }
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, 
                              "csv",
                              "/problems/hadamard-determinant-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
