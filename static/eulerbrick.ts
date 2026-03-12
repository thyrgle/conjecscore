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
  // Make sure only 3 integers are supplied.
  if (nums.length != 3) {
    return "Must submit 3 numbers!";
  }
  // Make sure it is an Euler brick.
  const [a, b, c] = nums.map((num) => BigInt(num.toString()));
  if (a < 1 || a > 10n ** 100n) {
    return "First number is out of range.";
  }
  if (b < 1 || b > 10n ** 100n) {
    return "Second number is out of range.";
  }
  if (c < 1 || c > 10n ** 100n) {
    return "Third number is out of range.";
  }
  // Ensure it is primitive.
  if (gcd(a, gcd(b, c)) > 1n) {
    return "Not primitive";
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
  const interval = new Decimal((bigSqr - smlSqr).toString());
  const denom = new Decimal(min(abc - smlSqr, bigSqr - abc).toString());
  const mil = 10 ** 6;
  return BigInt(Math.floor(-Math.log(denom.div(interval).toNumber()) * mil));
}
