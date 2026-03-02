import {Decimal} from 'decimal.js';

export function mean(numbers: Decimal[]) {
  let result = new Decimal(0);
  for (const num of numbers) {
    result = result.plus(num);
  }
  return result.div(numbers.length);
}

export function variance(numbers: Decimal[]) {
  const me = mean(numbers);
  let result = Decimal(0);
  for (const num of numbers) {
    result = result.plus((num.sub(me).mul(num.sub(me))));
  }
  return result.div(numbers.length);
}


export function reverse(s: string) {
  return s.split('').reverse().join('');
}
