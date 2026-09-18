const params = new URLSearchParams(location.search);
const detail = params.get("detail");

if (detail) {
  document.getElementById("detail").textContent = detail;
}

document.getElementById("retry").addEventListener("click", () => {
  window.tvweb.navigate("home");
});
