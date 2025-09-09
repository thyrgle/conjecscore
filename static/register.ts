document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", register);
});

async function register(event) {
  event.preventDefault();
  const url = "/auth/register";
  const email = (<HTMLInputElement>document.getElementById("email")).value;
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
      }),
    });
    const registerStatus = document.getElementById("registerstatus");
    if (response.status == 422) {
      registerStatus.textContent = "Not a valid email.";
    }
    if (response.status == 400) {
      registerStatus.textContent = "Unable to register. Check if username is already registered, or if password is too short.";
      return;
    }
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.error(error.message);
  }
}
