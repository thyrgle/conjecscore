import {Problem} from './problem.js';
import {Decimal} from 'decimal.js';

function mean(numbers: Decimal[]) {
  let result = new Decimal(0);
  for (const num of numbers) {
    result = result.plus(num);
  }
  return result.div(new Decimal(numbers.length));
}

function longestPrefix(s1: string, s2: string): Decimal {
  let result = new Decimal(0);
  try {
    // Skip '0b'.
    let i = 2;
    while (s1[i] == s2[i] && i < s1.length) {
      result = result.plus(1);
      i += 1;
    }
    return result;
  } catch (e) {
    console.log(e);
    return result;
  }
}

function reverse(s: string) {
  return s.split('').reverse().join('');
}

function score(submission: Decimal[]) {
  try {
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
    console.log("HERERE");
    
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
  const problem = new Problem(score, "csv", "/problems/magicsos-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});

