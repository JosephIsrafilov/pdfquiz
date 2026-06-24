const pageLanguage = localStorage.getItem("quizLanguage") === "ru" ? "ru" : "en";
document.documentElement.lang = pageLanguage;

function themeLabel(theme) {
  const labels = {
    en: {
      auto: "Theme: Auto",
      dark: "Theme: Dark",
      light: "Theme: Light",
    },
    ru: {
      auto: "Тема: авто",
      dark: "Тема: тёмная",
      light: "Тема: светлая",
    },
  };
  return labels[pageLanguage][theme] || labels[pageLanguage].auto;
}

function applyTheme(theme) {
  document.documentElement.classList.remove("dark-init", "light-init");
  document.body.classList.remove("dark", "light");

  if (theme === "dark" || theme === "light") {
    document.documentElement.classList.add(`${theme}-init`);
    document.body.classList.add(theme);
  }

  document.querySelectorAll(".theme-toggle").forEach((button) => {
    button.textContent = theme === "dark" ? "☀" : theme === "light" ? "☾" : "◐";
    button.setAttribute("aria-label", themeLabel(theme));
    button.setAttribute("title", themeLabel(theme));
  });
  window.dispatchEvent(new CustomEvent("themechange", { detail: { theme } }));
}

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

document.querySelectorAll(".theme-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const current = localStorage.getItem("theme") || "auto";
    const next = current === "auto" ? "dark" : current === "dark" ? "light" : "auto";
    localStorage.setItem("theme", next);
    applyTheme(next);
  });
});

applyTheme(localStorage.getItem("theme") || "auto");
