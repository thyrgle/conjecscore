import Decimal from "decimal.js";
import * as math from 'mathjs';

// From https://stackoverflow.com/a/31129384/667648
const eqSet = (xs: Set<number>, ys: Set<number>) =>
  xs.size === ys.size &&
  [...xs].every((x) => ys.has(x));

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    if (entries.length != 9 * 9) {
      return "Not a 9 × 9 matrix!";
    }
    const mat = math.reshape(math.matrix(entries), [9, 9]);
    const shouldHave = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);
    for (let i = 0; i < 9; i++) {

      const rowEntries = math.row(mat, i).valueOf() as Array<Array<number>>;
      const rowValues = new Set(rowEntries[0]);
      if (!eqSet(rowValues, shouldHave)) {
        console.log(rowValues);
	console.log(shouldHave);
        return "Rows must be some permutation of 1, ..., 9";
      }
    }
    return math.bigint(math.det(mat));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
