import Decimal from 'decimal.js';
Decimal.set({
  precision: 1000,
  toExpPos: 9e15
});
export {Problem};

// Promisfy RileReader, modified from:
// https://thecompetentdev.com/weeklyjstips/tips/65_promisify_filereader/
const read = (blob) => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = (event) => resolve(event.target.result);
  reader.onerror = reject;
  reader.readAsText(blob);
});

function safeJSONParse(json_string: string): JSON | string {
  try {
    return JSON.parse(json_string);
  } catch (e) { // Invalid JSON file!
    console.log(e);
    return "Error parsing JSON file!";
  }
}

function safeCSVParse(csv_string: string): Decimal[] | string {
  try {
    const csv_list = csv_string.trim().split(",");
    return csv_list.map((num) => new Decimal(num));
  } catch (e) {
    console.log(e);
    return "Error parsing CSV file!";
  }
}

function safeNumberParse(num_string: string): bigint | string {
  try {
    return BigInt(num_string);
  } catch (e) {
    console.log(e);
    return "Error parsing number";
  }
}

const stringify = {
  "json": JSON.stringify,
  "csv": (csv) => csv.toString(),
  "text": (text) => text.toString()
}

const parse = {
  "json": safeJSONParse,
  "csv": safeCSVParse,
  "text": safeNumberParse
}

type Input = JSON | Decimal[] | Decimal | bigint | number[];
type Error = string;
type Result = Decimal | number | bigint | string;

class Problem {
  private readonly score: (file: Input) => Promise<Result>;
  private readonly extension: string;
  private readonly post_url: string;

  constructor(score: (file: Input) => Promise<Result>,
	      extension: string,
	      post_url: string) {
    this.score = score;
    this.extension = extension;
    this.post_url = post_url;
  }

  public async submit(event) {
    event.preventDefault();
    const statusDiv = document.getElementById("status");

    const submission: HTMLInputElement | null
      = document.getElementById("submission") as HTMLInputElement;

    let inputContents: Input | Error = "";
    switch (submission.type) {
      case "file": {
        if (!submission.files![0]) { // No file selected!
          statusDiv.textContent 
	    = `No ${this.extension.toUpperCase()} file selected!`;
	    return;
	}
	const result = await read(submission.files![0]);
	inputContents = parse[this.extension](
          result.toString()
	);
	break;
      }
      case "text":
        inputContents = parse[this.extension](submission.value);
        break;
    }
    if (typeof inputContents === "string") { // Problem parsing contents.
      statusDiv.textContent = inputContents;
    } else {
      const s = await this.score(inputContents);
      if (typeof s === "string") { // Problem scoring contents.
        statusDiv.textContent = s;
      } else {
        statusDiv.textContent = `You scored ${s}.`;
      }
      const formData = new FormData();
      formData.append("submission", stringify[this.extension](inputContents));
      fetch(this.post_url, {
        method: "POST",
        body: formData
      }); 
    }
  }
}
