import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';

function score(submission: JSON) {
  try {
    let score = new Decimal(0);
    for (let i = 0; i < 99; i++) {
      for (let j = i + 1; j < 99; j++) {
	const adj1 = new Set(submission[i.toString()]);
	const adj2 = new Set(submission[j.toString()]);
	const c = new Decimal(adj1.intersection(adj2).size);
	const e = new Decimal(+adj2.has(i));
	const two = new Decimal(2);
	score = score.plus(c.minus(two.minus(e)).mul(c.minus(two.minus(e))));
      }
    }
    return score;
  } catch (e) {
    console.error(e);
    return "Could not score JSON file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "json", "/problems/conway-submit");
  const form = document.getElementById("form");
  // (e) => problem.submit(e) is so this is not overriden in class to be the
  // form.
  form.addEventListener("submit", (e) => problem.submit(e));
});
