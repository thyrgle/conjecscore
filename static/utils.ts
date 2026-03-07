export function mean(numbers: number[]): number {
  let result = 0;
  for (const num of numbers) {
    result = result + num;
  }
  return result / numbers.length;
}

export function variance(numbers: number[]): number {
  console.log(numbers);
  const me = mean(numbers);
  let result = 0;
  for (const num of numbers) {
    result += (num - me) ** 2;
  }
  return result / numbers.length;
}


export function reverse(s: string) {
  return s.split('').reverse().join('');
}
