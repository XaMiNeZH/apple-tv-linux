const continueButton = document.getElementById("continue");
const learnMoreButton = document.getElementById("learn-more");

continueButton.addEventListener("click", async () => {
  continueButton.disabled = true;
  continueButton.textContent = "Opening…";
  try {
    await window.tvweb.completeFirstRun();
  } catch {
    continueButton.disabled = false;
    continueButton.textContent = "Try again";
  }
});

learnMoreButton.addEventListener("click", () => {
  window.tvweb.openHelp("project");
});
