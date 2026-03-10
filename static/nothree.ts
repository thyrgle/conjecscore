import {Decimal} from "decimal.js";


function colinear(p1: [number, number], 
                  p2: [number, number],
                  p3: [number, number]): boolean {
  // From https://math.stackexchange.com/a/405981/15140
  const [a, b] = p1;
  const [m, n] = p2;
  const [x, y] = p3;
  return (n - b) * (x - m) == (y - n) * (m - a);
}


function couple(lst: number[]): [number, number][] {
  const result: [number, number][] = [];
  for (let i = 0; i < lst.length - 1; i += 2) {
    result.push([lst[i], lst[i+1]]);
  }
  return result;
}


export async function score(nums: Decimal[]): Promise<number | string> {
  const ns = nums.map((num) => num.toNumber());
  for (const num of ns) {
    if (num < 0 || num >= 100) {
      return "Coordinate value not in range [0, 99]!";
    }
  }
  if (ns.length % 2 == 1) {
    return "Not a CSV of points! (Need even length CSV!)";
  }
  const points: [number, number][] = couple(ns);
  if (points.length > 200) {
    return "Too many points!";
  }
  const dupCheck = new Set<[number, number]>(points);
  if (dupCheck.size != points.length) {
    return "All points should be distinct!";
  }
  for (let i = 0; i < points.length; i++) {
    for (let j = i+1; j < points.length; j++) {
      for (let k = j+1; k < points.length; k++) {
        if (colinear(points[i], points[j], points[k])) {
          return "Invalid configuration! 3 points are colinear!";
	}
      }
    }
  }
  return (1 - (points.length / 200)) * 10 ** 6;
}
