import Decimal from 'decimal.js';
import isqrt from 'bigint-isqrt';

function gcd(a: bigint, b: bigint): bigint {
  if (a < b) {
    [a, b] = [b, a];
  }
  while (b != 0n) {
    const temp = b;
    b = a % b;
    a = temp;
  }
  return a;
}

// Math.min does not work on bigintegers. This does.
const min = (a, b) => (a < b ? a : b);

export async function score(nums: Decimal[]): Promise<bigint | string> {
  if (nums.length != 3) {
    return "Must submit 3 numbers!";
  }
  // Make sure it is an Euler brick.
  const [a, b, c] = nums.map((num) => BigInt(num.toString()));
  // Ensure it is primitive.
  if (gcd(a, gcd(b, c)) > 1n) {
    return "Not primitive";
  }

  if (a <= 0n || b <= 0n || c <= 0n) {
    return "All numbers must be positive!";
  }
  const ab = a ** 2n + b ** 2n;
  if (isqrt(a ** 2n + b ** 2n) ** 2n != ab) {
    return "a^2 + b^2 is not a square!";
  }
  const ac = a ** 2n + c ** 2n;
  if (isqrt(a ** 2n + c ** 2n) ** 2n != ac) {
    return "a^2 + c^2 is not a square!";
  }
  const bc = b ** 2n + c ** 2n;
  if (isqrt(b ** 2n + c ** 2n) ** 2n != bc) {
    return "b^2 + c^2 is not a square!";
  }
  
  const abc = a ** 2n + b ** 2n + c ** 2n;
  const smlSqrt = isqrt(abc);
  const bigSqr = (smlSqrt + 1n) ** 2n;
  const smlSqr = smlSqrt ** 2n;
  const interval = bigSqr - smlSqr;
  const bil = 10n ** 9n;
  return (min(abc - smlSqr, bigSqr - abc) * bil) / interval;
}
