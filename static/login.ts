document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", login);
});

async function login(event) {
  event.preventDefault();
  const url = "/auth/jwt/login";
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
	'Content-Type': 'multipart/form-data',
      },
      body: JSON.stringify({ 
	username: email,
	password: password,
      }),
    });
    const loginStatus = document.getElementById("loginstatus");
    if (response.status == 400) {
        loginStatus.textContent = "Not a registered email!";
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
