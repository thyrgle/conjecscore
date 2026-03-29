import Decimal from 'decimal.js';

export async function score(nums: Decimal[]): Promise<number | string> {
  const N = 7;

  // Check the length of array
  if (nums.length != N * (N + 1) / 2) {
    return "Must submit 28 numbers!";
  }

  // Check the value range of array elements
  const ns = nums.map((num) => num.toNumber());
  for (const num of ns) {
    if (num < 1 || num > 10000) {
      return "Value not in the range [1, 10000]!";
    }
  }

  // Calculate the set of lengths measured by all rulers
  const diffs = new Set<number>();
  for (let k = 0; k < N; k++) {
    const v: number[] = [0];
    let a = 0;
    const start = Math.floor((k * (k + 1)) / 2);
    const end = start + k;
    for (let i = start; i <= end; i++) {
      a += ns[i];
      v.push(a);
    }
    for (let i = 0; i < v.length; i++) {
      for (let j = i + 1; j < v.length; j++) {
        diffs.add(Math.abs(v[i] - v[j]));
      }
    }
  }

  // Calculate score
  const maxPerfect = Math.floor((N * (N + 1) * (N + 2)) / 6);
  let score = 0;
  for (let x = 1; x <= maxPerfect; x++) {
    if (diffs.has(x)) {
      score++;
    }
  }
  return score;
}
