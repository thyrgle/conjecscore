document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", login);
});

async function login(event) {
  event.preventDefault();
}
