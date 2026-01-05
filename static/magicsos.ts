import {Problem} from './problem.js';

function mean(numbers: number[]) {
  return numbers.reduce((pre, cur) => cur + pre, 0) / numbers.length
}

function longestPrefix(s1, s2): number {
  let result = 0;
  try {
    let i = 0;
    while (s1[i] == s2[i]) {
      result += 1;
      i += 1;
    }
    return result;
  } catch (e) {
    console.log(e);
    return result;
  }
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
    
    const scores: number[] = [];
    for (let i = 0; i < sums.length; i++) {
      for (let j = i + 1; j < sums.length; j++) {
        const b1 = sums[i].toString(2);
	const b2 = sums[j].toString(2);
        if (b1.length != b2.length) {
          scores.push(10 ** 6);
	} else {
           const pre = longestPrefix(b1, b2);
           scores.push((10 ** 6) * (1 - pre / b1.length));
	}
      }
    }
    return Math.floor(mean(scores));
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

