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
  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });
  const loginStatus = document.getElementById("loginstatus");
  if (!response.ok) {
    const content = document.createTextNode(response.statusText);
    loginStatus.appendChild(content);
  } else {
    // TODO: Redirect to page person logged in from. Currently just defaults
    // to Problems
    location.href = "/problems";
  }
}
