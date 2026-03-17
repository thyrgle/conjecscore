import Decimal from 'decimal.js';

export async function score(nums: Decimal[]): Promise<bigint | string> {
  const N = 14;
  // Make sure only 3 integers are supplied.
  // Remember each point is 2 values of the CSV.
  if (nums.length != 2 * N) {
    return "Must submit 14 points (28 numbers)!";
  }
  // Ensure integrality. 
  const smlNums = nums.map((num) => num.toNumber());
  for (const num of smlNums) {
    if (Math.floor(num) != num) {
      return "Not all values are integers!";
    }
  }

  const sqrdDists: number[] = [];
  for (let i = 0; i < smlNums.length - 1; i += 2) {
    for (let j = i+2; j < smlNums.length - 1; j += 2) {
      const p1 = [smlNums[i], smlNums[i+1]];
      const p2 = [smlNums[j], smlNums[j+1]];
      if (p1[0] == p2[0] && p1[1] == p2[1]) {
        return "Not all points are distinct!";
      }
      const sqrdDist = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2;
      sqrdDists.push(sqrdDist);
    }
  }

  return BigInt(Math.max(...sqrdDists));
}
