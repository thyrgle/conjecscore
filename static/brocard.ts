import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';


function score(num: Decimal) {
  try {
    if (num.lte(0)) {
      return "All numbers must be positive!";
    }
    // TODO: Numbers too big for javascript to handle, just score on server by
    // default for now.
    return new Decimal(-Infinity);
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
