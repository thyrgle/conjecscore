import Decimal from "decimal.js";
import * as math from 'mathjs';

export async function score(submission: Decimal[]) {
  try {
    const entries = submission.map((num) => num.toNumber());
    const std = Math.sqrt(math.variance(entries, 'uncorrected') as number);
    console.log(std);
    const squares = entries.map((num) => num * num);
    const sums: number[] = [];
    const dupCheck = new Set<number>(entries);
    if (dupCheck.size != 9) {
      return "Not all numbers are distinct!";
    }
    for (const num of entries) {
      if (num <= 0) {
        return "All number must be positive!";
      }
    }
    // Rows
    sums.push(squares[0] + squares[1] + squares[2]);
    sums.push(squares[3] + squares[4] + squares[5]);
    sums.push(squares[6] + squares[7] + squares[8]);
    // Columns
    sums.push(squares[0] + squares[3] + squares[6]);
    sums.push(squares[1] + squares[4] + squares[7]);
    sums.push(squares[2] + squares[5] + squares[8]);
    // Diagonals
    sums.push(squares[0] + squares[4] + squares[8]);
    sums.push(squares[6] + squares[4] + squares[2]);
 
    const M: number = Math.max(...sums);
    const m: number = Math.min(...sums);
    const result = (M - m) / (math.log(M) * std);
    return math.floor(result * (10 ** 6));
  } catch (e) {
    console.error(e);
    return "Could not score CSV file!";
  }
}
