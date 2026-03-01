import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {longestPrefix, mean, reverse, removeTwoPow} from './utils.js';

function score(submission: Decimal[]) {
  try {
    submission = removeTwoPow(submission);
    const squares = submission.map((num) => num.mul(num));
    const sums: Decimal[] = [];
    // TODO Check for distinct squares!
    // Rows
    sums.push(squares[0].plus(squares[1]).plus(squares[2]));
    sums.push(squares[3].plus(squares[4]).plus(squares[5]));
    sums.push(squares[6].plus(squares[7]).plus(squares[8]));
    // Columns
    sums.push(squares[0].plus(squares[3]).plus(squares[6]));
    sums.push(squares[1].plus(squares[4]).plus(squares[7]));
    sums.push(squares[2].plus(squares[5]).plus(squares[8]));
    // Diagonals
    sums.push(squares[0].plus(squares[4]).plus(squares[8]));
    sums.push(squares[6].plus(squares[4]).plus(squares[2]));
    
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
