import {match, P} from 'ts-pattern';
import Decimal from 'decimal.js';
Decimal.set({
  precision: 1000,
});
export {Problem};

class Problem {
  private readonly score: (file: JSON | Decimal[] | Decimal) => Decimal | string;
  private readonly extension: string;
  private readonly post_url: string;

  constructor(score: (file: JSON | Decimal[] | Decimal) => Decimal | string,
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
    try {
      // Might be a file.
      const file = submission.files![0];
      if (!file) {
        statusDiv.textContent 
          = `No ${this.extension.toUpperCase()} file selected!`;
        return;
      }
      const reader = new FileReader();
      match(this.extension)
        .with("json", () => {
          reader.onload = () => {
            try {
              const s = this.score(JSON.parse(reader.result.toString()));
              match(s)
                .with(P.string, (err) => { // Return error as string.
                  statusDiv.textContent = err;
                })
                .otherwise((num) => { // Otherwise return number.
                  statusDiv.textContent = `You scored ${num.toString()}.`;
                  const formData = new FormData();
                  formData.append("submission", reader.result.toString());
                  fetch(this.post_url, {
                    method: "POST",
                    body: formData,
                  });
                })
	    } catch (e) {
              statusDiv.textContent = "Could not parse JSON!"
	      console.log(e);
	    }
          };
        })
        .with("csv", () => {
          reader.onload = () => {
            try {
              const split_csv = reader.result.toString().trim().split(",");
	      const num_list = split_csv.map(num => new Decimal(num));
	      console.log(num_list[0].toString());
              const s = this.score(num_list);
              match(s)
                .with(P.string, (err) => { // Return error as string.
                  statusDiv.textContent = err;
                })
                .otherwise((num) => { // Otherwise return number.
                  if (!num.isFinite()) {
                    statusDiv.textContent = "Scoring on server."
		  } else {
                    statusDiv.textContent = `You scored ${num.toString()}.`;
		  }
                  const formData = new FormData();
                  formData.append("submission", reader.result.toString());
                  fetch(this.post_url, {
                    method: "POST",
                    body: formData,
                  });
                })
            } catch (e) {
              statusDiv.textContent = "Could not parse CSV!";
              console.log(e);
            }
	  }
        })
      reader.onerror = () => {
        statusDiv.textContent = "Error reading file. Please try again.";
      };
      reader.readAsText(file);
    } catch (e) {
      // Might just be text.
      console.log(e);
      const num = this.score(new Decimal(submission.value));
      match(num)
        .with(P.string, (err) => {
	  statusDiv.textContent = err;
        })
	.otherwise((num) => {
          if (!num.isFinite()) {
            statusDiv.textContent = "Scoring on server";
          } else {
            statusDiv.textContent = `You scored ${num.toString()}.`;
          }   
	});
      const formData = new FormData();
      formData.append("submission", submission.value);
      fetch(this.post_url, {
        method: "POST",
        body: formData,
      });
    }
  }
}
