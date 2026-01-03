import {Problem} from './problem.js';

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

function score(nums: number[]) {
  try {
    if (nums.length != 4) {
      return "Need 4 numbers!";
    }
    const dup_check = new Set<number>(nums);
    if (dup_check.size != 4) {
      return "Not all numbers are distinct!";
    }
    const [a, b, c, d] = nums;
    const big = Math.max(a ** 5 + b ** 5, c ** 5 + d ** 5).toString(2);
    // Not const because it will be padded with 0s.
    let small = Math.min(a ** 5 + b ** 5, c ** 5 + d ** 5).toString(2);
    let i = small.length;
    // Pad the smaller number to have the same length as the big number.
    while (i < big.length) {
      small = "0" + small;
      i += 1;
    }
    const pre = longestPrefix(big, small) + 1;
    const suf = longestPrefix(big.split('').reverse().join(''),
                              small.split('').reverse().join('')) + 1;
    console.log(pre, suf);
    return Math.floor((1 - Math.min(pre, suf) / (big.length + 1)) * (10 ** 6));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const problem = new Problem(score, "csv", "/problems/taxicab-submit");
  const form = document.getElementById("form");
  form.addEventListener("submit", (e) => problem.submit(e));
});
