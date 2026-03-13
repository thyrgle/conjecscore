import Decimal from "decimal.js";
import * as math from 'mathjs';


export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    if (entries.length != 10 * 10) {
      return "Not a 10 × 10 matrix!";
    }
    const mat = math.reshape(math.matrix(entries), [10, 10]);
    const shouldHave = new Array(10).fill(0);
    const arr = mat.valueOf();
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 10; j++) {
        shouldHave[arr[i][j] - 1] += 1;
      }
    }
    for (const val of shouldHave) {
      if (val != 10) {
        console.log(val);
        return "Not all 1, ..., 10 show up exactly 10 times.";
      }
    }
    return math.bigint(math.det(mat));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
