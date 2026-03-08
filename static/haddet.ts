import Decimal from "decimal.js";
import * as math from 'mathjs';

export async function score(nums: Decimal[]): Promise<bigint | string> {
  try {
    const entries = nums.map((num) => num.toNumber());
    console.log(entries);
    if (entries.length != 23 * 23) {
      return "Not a 23 × 23 matrix!";
    }
    const onePmOne = (num) => num == 1 || num == -1;
    if (entries.every(onePmOne)) {
      const mat = math.reshape(math.matrix(entries), [23, 23]);
      return math.bigint(math.det(mat)) / (10n ** 9n);
    } else {
      return "All entries must be ±1!";
    }
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
