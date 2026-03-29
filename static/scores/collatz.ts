export async function score(n: bigint): Promise<number | string> {
  if (n <= 0) {
    return "The number must be positive!";
  }
  try {
    const magnitude = n.toString(2).length;
    let orbit = 0;
    while (n != 1n) {
      if (n % 2n == 1n) {
        orbit = orbit + 1;
	n = 3n * n + 1n;
      } else {
        n = n / 2n;
      }
    }
    return Math.floor((orbit * 1000) / magnitude);
  } catch (e) {
    console.error(e);
    return "Could not score input!";
  }
}
