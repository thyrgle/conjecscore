import {Decimal} from 'https://esm.sh/decimal.js';
type Decimal = typeof Decimal
Decimal.set({
  precision: 1000,
  toExpPos: 9e15
});

// Promisfy RileReader, modified from:
// https://thecompetentdev.com/weeklyjstips/tips/65_promisify_filereader/
function read(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result!.toString());
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file);
  });
}

type Input = JSON | Decimal[] | Decimal | bigint | number[];
type Error = string;
type Result = Decimal | number | bigint | string;

function safeJSONParse(json_string: string): Input {
  try {
    return JSON.parse(json_string);
  } catch (e) { // Invalid JSON file!
    console.log(e);
    return "Error parsing JSON file!";
  }
}

function safeCSVParse(csv_string: string): Input {
  try {
    const csv_list = csv_string.trim().split(",");
    const numbers = csv_list.map((num) => new Decimal(num));
    if (!numbers.every((num) => num.isInt())) {
      return "Not every input is an integer!";
    }
    return numbers;
  } catch (e) {
    console.log(e);
    return "Error parsing CSV file!";
  }
}

function safeNumberParse(num_string: string): Input {
  try {
    return BigInt(num_string);
  } catch (e) {
    console.log(e);
    return "Error parsing number";
  }
}

const stringify: Record<string, ((txt: (JSON | string)) => string)> = {
  "json": JSON.stringify,
  "csv": (csv) => csv.toString(),
  "text": (text) => text.toString()
}

const parse: Record<string, ((s: string) => Input)> = {
  "json": safeJSONParse,
  "csv": safeCSVParse,
  "text": safeNumberParse
}

class Problem {
  private readonly score: (file: Input) => Promise<Result>;
  private readonly extension: string;
  private readonly post_url: string;
  private readonly variant: string;

  constructor(score: (file: Input) => Promise<Result>,
              extension: string,
  post_url: string,
  variant: string) {
    this.score = score;
    this.extension = extension;
    this.post_url = post_url;
    this.variant = variant;
  }

  public async submit(event: any) {
    event.preventDefault();
    const statusDiv = document.getElementById("status");

    const submission: HTMLInputElement | null
    = document.getElementById("submission") as HTMLInputElement;

    let inputContents: Input | Error = "";
    switch (submission.type) {
      case "file": {
        if (!submission.files![0]) { // No file selected!
          statusDiv!.textContent 
          = `No ${this.extension.toUpperCase()} file selected!`;
          return;
        }
        const result = await read(submission.files![0]);
        inputContents = parse[this.extension](result.toString());
        break;
      }
      case "text":
        inputContents = parse[this.extension](submission.value);
      break;
    }
    if (typeof inputContents === "string") { // Problem parsing contents.
      statusDiv!.textContent = inputContents;
    } else {
      const s = await this.score(inputContents);
      if (typeof s === "string") { // Problem scoring contents.
        statusDiv!.textContent = s;
      } else {
        statusDiv!.textContent = `You scored ${s}.`;
      }
      fetch(this.post_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "submission": stringify[this.extension](inputContents),
          "variant": this.variant
        }),
      }); 
    }
  }
}
export {Problem};
