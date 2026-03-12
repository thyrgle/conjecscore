import Decimal from "decimal.js";
import * as math from 'mathjs';

// From https://stackoverflow.com/a/31129384/667648
const eqSet = (xs: Set<number>, ys: Set<number>) =>
  xs.size === ys.size &&
  [...xs].every((x) => ys.has(x));

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    if (entries.length != 10 * 10) {
      return "Not a 10 × 10 matrix!";
    }
    const mat = math.reshape(math.matrix(entries), [10 * 10]);
    const shouldHave = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    for (let i = 0; i < 10; i++) {

      const rowEntries = math.row(mat, i).valueOf() as Array<Array<number>>;
      const rowValues = new Set(rowEntries[0]);
      if (!eqSet(rowValues, shouldHave)) {
        return "Rows must be some permutation of 1, ..., 10";
      }
    }
    return math.bigint(math.det(mat));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
