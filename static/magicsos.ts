import {Problem} from './problem.js';

function mean(numbers: number[]) {
  return numbers.reduce((pre, cur) => cur + pre, 0) / numbers.length
}

function variance(numbers: number[]) {
  const mu: number = mean(numbers);
  const summand: number = numbers.reduce(
	(pre, cur) => ((cur - mu) ** 2) + pre, 0);
  return summand / numbers.length;
}

function score(submission: number[]) {
  try {
    const sums: number[] = [];
    // TODO Check for distinct squares!
    // Rows
    sums.push(submission[0] + submission[1] + submission[2]);
    sums.push(submission[3] + submission[4] + submission[5]);
    sums.push(submission[6] + submission[7] + submission[8]);
    // Columns
    sums.push(submission[0] + submission[3] + submission[6]);
    sums.push(submission[1] + submission[4] + submission[7]);
    sums.push(submission[2] + submission[5] + submission[8]);
    // Diagonals
    sums.push(submission[0] + submission[4] + submission[8]);
    sums.push(submission[6] + submission[4] + submission[2]);
    
    return Math.floor((10 ** 9) * variance(sums) / mean(sums));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv", "/problems/magicsos-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});

