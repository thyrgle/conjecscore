import Decimal from "decimal.js";
import * as math from 'mathjs';

// From https://stackoverflow.com/a/31129384/667648
const eqSet = (xs, ys) =>
    xs.size === ys.size &&
    [...xs].every((x) => ys.has(x));

function isLatin(
    sqr: math.Matrix<math.MathNumericType>, order: number
  ): boolean {
  const need = new Set(Array.from(new Array(order), (x, i) => i+1));
  for (let i = 0; i < order; i++) {
    const row = math.row(sqr, i).valueOf()[0] as Array<number>;
    const has = new Set(row);
    if (!eqSet(need, has)) {
      return false;
    }
  }
  const sqrT = math.transpose(sqr);
  for (let i = 0; i < order; i++) {
    // col is the row of the transpose
    const col = math.row(sqrT, i).valueOf()[0] as Array<number>;
    const has = new Set(col);
    console.log(col);
    if (!eqSet(need, has)) {
      return false;
    }
  }
  console.log("HERE?");
  // Checks all passed!
  return true;
}

function isIntercalate(
    sqr: math.Matrix<math.MathNumericType>, 
    r1: number, r2: number, c1: number, c2: number
  ): boolean {
  const arr = sqr.valueOf();
  return arr[r1][c1] == arr[r2][c2] && arr[r2][c1] == arr[r1][c2];
}

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    const N = 30;
    if (entries.length != N * N) {
      return "Not a 30 × 30 square!";
    }
    const mat = math.reshape(math.matrix(entries), [N, N]);
    if (!isLatin(mat, N)) {
      return "Not a Latin Square!";
    }
    let count = 0;
    for (let r1 = 0; r1 < N; r1++) {
      for (let r2 = r1+1; r2 < N; r2++) {
        for (let c1 = 0; c1 < N; c1++) {
          for (let c2 = c1+1; c2 < N; c2++) {
            if (isIntercalate(mat, r1, r2, c1, c2)) {
              count++;
	    }
	  }
	}
      }
    }
    return BigInt(count);
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
