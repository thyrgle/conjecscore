export async function score(submission: JSON) {
  try {
    let score = 0;
    for (let i = 0; i < 99; i++) {
      for (let j = i + 1; j < 99; j++) {
	const adj1 = new Set(submission[i.toString()]);
	const adj2 = new Set(submission[j.toString()]);
	const c = adj1.intersection(adj2).size;
	const e = +adj2.has(i);
	score += (c - (2 - e)) ** 2;
      }
    }
    return score;
  } catch (e) {
    console.error(e);
    return "Could not score JSON file!";
  }
}
