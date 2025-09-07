async function conwaySubmit(event) {
  // Don't go to new page.
  event.preventDefault();
  const jsonFile: HTMLInputElement | null 
    = document.getElementById("json") as HTMLInputElement;
  const file = jsonFile.files![0];
  const reader = new FileReader();
  reader.readAsText(file);
  const result: string = await new Promise((resolve, reject) => {
    reader.onload = () => {
      const submission: JSON = JSON.parse(reader.result.toString());
      resolve(submission.toString())
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

document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", conwaySubmit);
});
