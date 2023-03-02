var container = document.getElementById("my-container");
var containerOffset = container.offsetTop;

window.addEventListener("load", function() {
  container.style.position = "absolute";
  container.style.top = containerOffset + "px";
});