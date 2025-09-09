document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", register);
});

async function register(event) {
  event.preventDefault();
  const loc = document.location;
  const url = loc.host + "/auth/register";
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  try {
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify({ 
	email: email,
	password: password,
      }),
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.error(error.message);
  }
}
