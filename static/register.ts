document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", register);
});

async function register(event) {
  event.preventDefault();
  const url = "/auth/register";
  const email = (<HTMLInputElement>document.getElementById("email")).value;
  const nickname = (<HTMLInputElement>document.getElementById("nickname"))
    .value;
  const pass = (<HTMLInputElement>document.getElementById("password")).value;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
	"Content-Type": "application/json",
      },
      body: JSON.stringify({ 
	email: email,
	password: pass,
	nickname: nickname,
      }),
    });
    const registerStatus = document.getElementById("registerstatus");
    const result = await response.json();
    if (!response.ok) {
      registerStatus.textContent = result["detail"];
      throw new Error(`Response status: ${response.status}`);
    } else {
      location.href = "/login";
    }
  } catch (error) {
    console.error(error.message);
  }
}
