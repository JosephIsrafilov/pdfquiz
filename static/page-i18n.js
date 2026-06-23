const pageLanguage = localStorage.getItem("quizLanguage") === "ru" ? "ru" : "en";
document.documentElement.lang = pageLanguage;

document.querySelectorAll("[data-en][data-ru]").forEach((element) => {
  element.textContent = element.dataset[pageLanguage];
});

document.querySelectorAll(".language-button").forEach((button) => {
  button.classList.toggle("is-active", button.dataset.language === pageLanguage);
  button.addEventListener("click", () => {
    localStorage.setItem("quizLanguage", button.dataset.language);
    window.location.reload();
  });
});
