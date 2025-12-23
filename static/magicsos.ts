document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", magicsosSubmit);
});

function mean(numbers: number[]) {
  return numbers.reduce((pre, cur) => cur + pre, 0) / numbers.length
}

function variance(numbers: number[]) {
  const mu: number = mean(numbers);
  const summand: number = numbers.reduce(
	(pre, cur) => ((cur - mu) ** 2) + pre, 0);
  return summand / numbers.length;
}

async function magicsosSubmit(event) {
  // Don't go to new page.
  event.preventDefault();
  const statusDiv = document.getElementById("status");
  const csvFile: HTMLInputElement | null 
    = document.getElementById("square") as HTMLInputElement;
  const file = csvFile.files![0];
  if (!file) {
    statusDiv.textContent = "No CSV file selected!";
    return;
  }
  const reader = new FileReader();
  reader.readAsText(file);
  const result: number[] = await new Promise((resolve, reject) => {
    reader.onload = () => {
      // Check if valid CSV file.
      try {
        const submission: number[] = reader.result.toString().split(",")
	                                   .map(num => parseInt(num, 10));
        resolve(submission)
      } catch (e) {
        statusDiv.textContent = "Invalid CSV file!";
	console.error(e);
	reject("Invalid CSV");
      }
    };
    reader.onerror = (e) => {
      reject(e)
    };
  });
  try {
    const sums: number[] = [];
    // TODO Check for distinct squares!
    // Rows
    sums.push(result[0] + result[1] + result[2]);
    sums.push(result[3] + result[4] + result[5]);
    sums.push(result[6] + result[7] + result[8]);
    // Columns
    sums.push(result[0] + result[3] + result[6]);
    sums.push(result[1] + result[4] + result[7]);
    sums.push(result[2] + result[5] + result[8]);
    // Diagonals
    sums.push(result[0] + result[4] + result[8]);
    sums.push(result[6] + result[4] + result[2]);
    
    console.log(sums);
    statusDiv.textContent = `You scored ${Math.floor((10 ** 9) * variance(sums) / mean(sums))}`;
  } catch (e) {
    statusDiv.textContent = "Could not score CSV file!";
    console.error(e);
  }
  const formData = new FormData();
  formData.append("square", result.toString());
  console.log(result);
  const response = await fetch("/magicsos-submit", {
    method: "POST",
    body: formData,
  });
  console.log(await response);
}
