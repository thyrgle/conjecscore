import {Problem} from './problem.js';


function score(nums: number[]) {
  try {
    const big = Math.max(nums[0] ** 5 + nums[1] ** 5, nums[2] ** 5 + nums[3] ** 5);
    const small = Math.min(nums[0] ** 5 + nums[1] ** 5, nums[2] ** 5 + nums[3] ** 5);

    return Math.floor((big / small - 1) * 10 ** 6);
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

