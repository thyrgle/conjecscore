import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';
import {variance} from './utils.js';

function score(submission: Decimal[]) {
  try {
    const std = variance(submission).sqrt();
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
    
    const M = Decimal.max(sums[0], sums[1], sums[2],
                          sums[3], sums[4], sums[5],
                          sums[6], sums[7]);
    const m = Decimal.min(sums[0], sums[1], sums[2],
                          sums[3], sums[4], sums[5],
                          sums[6], sums[7]);
    const result = M.sub(m).div(Decimal.ln(M).mul(std));
    const one_mil = Decimal(10 ** 6);
    return Decimal.floor(result.mul(one_mil));
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
