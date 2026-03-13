import Decimal from "decimal.js";
import * as math from 'mathjs';


export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    const N = 16;
    if (entries.length != N * N) {
      return "Not a 16 × 16 matrix!";
    }
    const mat = math.reshape(math.matrix(entries), [N, N]);
    const shouldHave = new Array(N).fill(0);
    const arr = mat.valueOf();
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        shouldHave[arr[i][j] - 1] += 1;
      }
    }
    for (const val of shouldHave) {
      if (val != N) {
        return "Not all 1, ..., 16 show up exactly 16 times.";
      }
    }
    return math.bigint(Math.floor(math.det(mat) / (10 ** 16)));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
