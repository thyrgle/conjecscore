import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';


function score(num: Decimal) {
  try {
    const magnitude = num.toBinary().length - 2;
    let orbit = 0;
    while (!num.eq(1)) {
      if (num.mod(2).eq(1)) {
        orbit = orbit + 1;
	num = num.mul(3).plus(1)
      } else {
        num = num.div(2);
      }
    }
    return Decimal.floor(new Decimal(orbit).div(magnitude).mul(1000));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv", "/problems/collatz-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
