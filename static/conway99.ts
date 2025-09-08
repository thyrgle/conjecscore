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
  const response = await fetch("/conway-submit", {
    method: "POST",
    body: result
  });
  console.log(await response.json());
}
