document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", conwaySubmit);
});

async function conwaySubmit(event) {
  // Don't go to new page.
  event.preventDefault();
  const statusDiv = document.getElementById("status");
  const jsonFile: HTMLInputElement | null 
    = document.getElementById("graph") as HTMLInputElement;
  const file = jsonFile.files![0];
  if (!file) {
    statusDiv.textContent = "No JSON file selected!";
    return;
  }
  const reader = new FileReader();
  reader.readAsText(file);
  const result: string = await new Promise((resolve, reject) => {
    reader.onload = () => {
      // Check if valid JSON file.
      try {
        const submission: JSON = JSON.parse(reader.result.toString());
        resolve(submission.toString())
      } catch (e) {
        statusDiv.textContent = "Invalid JSON file!";
	console.error(e);
	reject("Invalid JSON");
      }
      // TODO Check if JSON file meets submission requirements.
    };
    reader.onerror = (e) => {
      reject(e)
    };
  });
  try {
    const submission = JSON.parse(result);
    let score = 0;
    for (let i = 0; i < 99; i++) {
      for (let j = i + 1; j < 99; j++) {
	const adj1 = new Set(submission[i.toString()]);
	const adj2 = new Set(submission[j.toString()]);
	const c = adj1.intersection(adj2).size;
	const e = +adj2.has(i);
	score += (c - (2 - e)) * (c - (2 - e));
        statusDiv.textContent = `You scored ${score}`;
      }
    }
  } catch (e) {
    statusDiv.textContent = "Could not score JSON file!";
    console.error(e);
  }
  const response = await fetch("/conway-submit", {
    method: "POST",
    body: result
  });
  console.log(await response.json());
}
