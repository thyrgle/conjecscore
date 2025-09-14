document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", login);
});

async function login(event) {
  event.preventDefault();
  const url = "/auth/jwt/login";
  const email = (<HTMLInputElement>document.getElementById("email")).value;
  const pass = (<HTMLInputElement>document.getElementById("password")).value;
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", pass);
  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });
    const loginStatus = document.getElementById("loginstatus");
    const result = await response;
    if (!response.ok) {
      loginStatus.textContent = result.json()["detail"];
      throw new Error(`Response status: ${response.status}`);
    } else {
      // TODO: Don't hard code when more problems are available.
      location.href = "/conway-99";
    }
  } catch (error) {
    console.error(error.message);
  }
}
