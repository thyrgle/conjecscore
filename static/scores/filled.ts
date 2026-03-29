import Decimal from "decimal.js";
import * as math from 'mathjs';


// From https://stackoverflow.com/a/31129384/667648
const eqSet = (xs, ys) =>
    xs.size === ys.size &&
    [...xs].every((x) => ys.has(x));

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const N = 11;
    const entries = nums.map((num) => num.toNumber());
    console.log(entries);
    if (entries.length != N * N) {
      return "Not a 11 × 11 matrix!";
    }
    const need = new Set(Array.from(new Array(N * N), (x, i) => i+1));
    const have = new Set(entries);
    if (!eqSet(need, have)) {
      return "Not the correct numbers!";
    }
    const mat = math.reshape(math.matrix(nums, 'dense', 'bignumber'), [N, N]);
    const P = new Decimal("470379650542113331346272");
    const bil = new Decimal(10 ** 9);
    return math.bigint(
	new Decimal(math.det(mat)).div(P).mul(bil)
    );
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
