import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {longestPrefix, mean, reverse, removeTwoPow} from './utils.js';

function score(submission: Decimal[]) {
  try {
    submission = removeTwoPow(submission);
    const sums: Decimal[] = [];
    // TODO Check for distinct squares!
    // Rows
    sums.push(submission[0].plus(submission[1]).plus(submission[2]));
    sums.push(submission[3].plus(submission[4]).plus(submission[5]));
    sums.push(submission[6].plus(submission[7]).plus(submission[8]));
    // Columns
    sums.push(submission[0].plus(submission[3]).plus(submission[6]));
    sums.push(submission[1].plus(submission[4]).plus(submission[7]));
    sums.push(submission[2].plus(submission[5]).plus(submission[8]));
    // Diagonals
    sums.push(submission[0].plus(submission[4]).plus(submission[8]));
    sums.push(submission[6].plus(submission[4]).plus(submission[2]));
    
    const scores: Decimal[] = [];
    for (let i = 0; i < sums.length; i++) {
      for (let j = i + 1; j < sums.length; j++) {
        const b1 = reverse(sums[i].toBinary().slice(2));
	const b2 = reverse(sums[j].toBinary().slice(2));
	const mil = new Decimal(10 ** 6);
        if (b1.length != b2.length) {
          scores.push(mil);
	} else {
           const pre = longestPrefix(b1, b2);
	   const one = new Decimal(1);
	   const len = new Decimal(b1.length);
           scores.push(mil.mul(one.minus(pre.div(len))));
	}
      }
    }
    return Decimal.floor(mean(scores));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv",
                              "/problems/magic-square-of-squares-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
