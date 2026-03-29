async function conway_score(submission: JSON, N: number) {
  try {
    let score = 0;
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
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

export async function score(submission: JSON) {
  return await conway_score(submission, 99);
}

export async function score6273(submission: JSON) {
  return await conway_score(submission, 6273);
}

export async function score494019(submission: JSON) {
  return await conway_score(submission, 494019);
}

