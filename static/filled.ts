import Decimal from "decimal.js";
import * as math from 'mathjs';


// From https://stackoverflow.com/a/31129384/667648
const eqSet = (xs, ys) =>
    xs.size === ys.size &&
    [...xs].every((x) => ys.has(x));

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const N = 8;
    const entries = nums.map((num) => num.toNumber());
    console.log(entries);
    if (entries.length != N * N) {
      return "Not a 8 × 8 matrix!";
    }
    const need = new Set(Array.from(new Array(N * N), (x, i) => i+1));
    const have = new Set(entries);
    if (!eqSet(need, have)) {
      return "Not the correct numbers!";
    }
    const mat = math.reshape(math.matrix(entries), [N, N]);
    const P = 441077015225642;
    return math.bigint(Math.floor(math.det(mat) / P * 100));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
