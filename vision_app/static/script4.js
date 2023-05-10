const colorPicker = document.getElementById("colorPicker");
const body = document.body;
const html = document.documentElement;

colorPicker.addEventListener("input", function() {
  body.style.backgroundColor = colorPicker.value;
  html.style.backgroundColor = colorPicker.value;
});