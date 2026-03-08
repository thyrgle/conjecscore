import isqrt from 'bigint-isqrt';


function sleep(time: number) {
  return new Promise((resolve) => setTimeout(resolve, time));
}


async function factorial(n: bigint): Promise<bigint> {
  let result: bigint = 1n;
  while (n > 1n) {
    await sleep(1);
    result *= n;
    n -= 1n;
  }
  return result;
}

// Math.min does not work on biginters. This does.
const min = (a, b) => (a < b ? a : b);

export async function score(num: bigint): Promise<bigint | string> {
  try {
    if (num < 8) {
      return "Numbers are too small.";
    }
    if (num >= 5000) {
      return "Scoring on server!";
    }
    const nfact = (await factorial(num)) + 1n;
    let smlSqr = isqrt(nfact);
    const bigSqr = (smlSqr + 1n) ** 2n;
    smlSqr = smlSqr ** 2n;
    const interval = bigSqr - smlSqr;
    const sfact = nfact - smlSqr;
    const bfact = bigSqr - nfact;
    const numerator = min(sfact, bfact);
    const bil = BigInt(10 ** 9);
    return (numerator * bil) / interval;
  } catch (e) {
    console.error(e);
    return "Could not score number!";
  }
}
