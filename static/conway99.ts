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
  const result: JSON = await new Promise((resolve, reject) => {
    reader.onload = () => {
      // Check if valid JSON file.
      try {
        const submission: JSON = JSON.parse(reader.result.toString());
        resolve(submission)
      } catch (e) {
        statusDiv.textContent = "Invalid JSON file!";
	console.error(e);
	reject("Invalid JSON");
      }
    };
    reader.onerror = (e) => {
      reject(e)
    };
  });
  try {
    const submission = JSON.parse(JSON.stringify(result));
    let score = 0;
    for (let i = 0; i < 99; i++) {
      for (let j = i + 1; j < 99; j++) {
	const adj1 = new Set(submission[i.toString()]);
	const adj2 = new Set(submission[j.toString()]);
	const c = adj1.intersection(adj2).size;
	const e = +adj2.has(i);
	score += (c - (2 - e)) * (c - (2 - e));
      }
    }
    statusDiv.textContent = `You scored ${score}`;
  } catch (e) {
    statusDiv.textContent = "Could not score JSON file!";
    console.error(e);
  }
  const formData = new FormData();
  formData.append("graph", JSON.stringify(result));
  console.log("HERE");
  console.log(result);
  const response = await fetch("/conway-submit", {
    method: "POST",
    body: formData,
  });
  console.log(await response.json());
}
