function conwaySubmit(event) {
  event.preventDefault();
}

document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  form.addEventListener("submit", conwaySubmit);
});
