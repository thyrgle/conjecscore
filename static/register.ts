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
  if (!response.ok) {
    const result = await response.json();
    const readable = {};
    readable["REGISTER_USER_ALREADY_EXISTS"] = "A user with this email already exists.";
    const content = document.createTextNode(readable[result["detail"]]);
    registerStatus.appendChild(content);
  } else {
    location.href = "/login";
  }
}
