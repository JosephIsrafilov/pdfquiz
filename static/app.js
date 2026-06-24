const bootstrap = window.APP_BOOTSTRAP || { currentUser: null, catalog: [] };

const copy = {
  en: {
    theme: "Change theme",
    profile: "Profile",
    admin: "Teacher panel",
    logout: "Log out",
    login: "Log in",
    register: "Register",
    eyebrow: "SELF-PACED IT PRACTICE",
    heroTitle: "Build a test from the topics you studied",
    heroSubtitle: "Select a course and one or more topics. Questions are balanced across your selection and checked securely.",
    curriculumSource: "Core topic sequence aligned with",
    availableQuestions: "available questions",
    stepOne: "STEP 1",
    chooseCourse: "Choose a course",
    stepTwo: "STEP 2",
    chooseTopics: "Choose topics",
    chooseTopicsHint: "Select one or several topics. The test will distribute questions as evenly as possible.",
    stepThree: "STEP 3",
    configureTest: "Configure your test",
    questionCount: "Question count",
    difficulty: "Difficulty",
    allLevels: "All levels",
    beginner: "Beginner",
    intermediate: "Intermediate",
    advanced: "Advanced",
    textSize: "Text size",
    checkingMode: "Checking mode",
    instantCheck: "Check each question",
    instantCheckHint: "Show feedback before final submission.",
    startTest: "Start knowledge check",
    yourTest: "YOUR TEST",
    emptyQuiz: "Select your topics and start a knowledge check.",
    submitTest: "Submit test",
    buildingTest: "Building your test",
    buildingTestHint: "Balancing questions across the selected topics.",
    topics: "topics",
    topic: "topic",
    questions: "questions",
    question: "question",
    selected: "selected",
    availableForSelection: "{count} questions available for the selected topics.",
    noTopics: "This course does not have active topics yet.",
    selectTopic: "Select at least one topic.",
    invalidCount: "Choose a question count between 1 and {count}.",
    checkQuestion: "Check question",
    chooseAnswer: "Choose an answer first.",
    correct: "Correct.",
    incorrect: "Not quite. The correct answer is highlighted.",
    excellent: "Excellent!",
    good: "Good job!",
    needsPractice: "Needs practice",
    explanation: "Explanation",
    yourAnswer: "Your answer",
    correctAnswer: "Correct answer",
    notAnswered: "Not answered",
    answered: "{answered} of {total} answered",
    score: "Score",
    correctAnswers: "{correct} of {total} correct",
    unanswered: "{count} unanswered",
    submitConfirm: "Are you sure you want to submit?",
    saved: "This result was saved to your profile.",
    guest: "Log in to save future results.",
    mistakes: "Review:",
    questionLabel: "Question {number}",
    newTest: "Start another test",
    stageFoundations: "1 · Foundations",
    stageCollections: "2 · Collections",
    stageFlow: "3 · Decisions and loops",
    stageFunctions: "4 · Functions and reusable code",
    stageToolkit: "5 · Python toolkit",
    stageOop: "6 · OOP and files",
    stageDeep: "7 · Python deep dive",
    joinRoomTitle: "Join a Teacher's Room",
    joinRoomDesc: "If your teacher gave you a 6-digit code, enter it here to start your configured test.",
    joinRoomBtn: "Join Room",
    resultCorrect: "Correct",
    resultUnanswered: "Unanswered",
    resultStatus: "Status",
    resultSaved: "Saved",
    resultGuest: "Guest",
  },
  ru: {
    theme: "Сменить тему",
    profile: "Профиль",
    admin: "Панель преподавателя",
    logout: "Выйти",
    login: "Войти",
    register: "Регистрация",
    eyebrow: "САМОСТОЯТЕЛЬНАЯ ПРАКТИКА ПО IT",
    heroTitle: "Соберите тест по изученным темам",
    heroSubtitle: "Выберите курс и одну или несколько тем. Вопросы распределяются между темами и проверяются на сервере.",
    curriculumSource: "Последовательность основных тем соответствует",
    availableQuestions: "доступных вопросов",
    stepOne: "ШАГ 1",
    chooseCourse: "Выберите курс",
    stepTwo: "ШАГ 2",
    chooseTopics: "Выберите темы",
    chooseTopicsHint: "Можно выбрать несколько тем. Тест распределит вопросы между ними максимально равномерно.",
    stepThree: "ШАГ 3",
    configureTest: "Настройте тест",
    questionCount: "Количество вопросов",
    difficulty: "Сложность",
    allLevels: "Все уровни",
    beginner: "Начальный",
    intermediate: "Средний",
    advanced: "Продвинутый",
    textSize: "Размер текста",
    checkingMode: "Режим проверки",
    instantCheck: "Проверять каждый вопрос",
    instantCheckHint: "Показывать результат до финальной отправки.",
    startTest: "Начать проверку знаний",
    yourTest: "ВАШ ТЕСТ",
    emptyQuiz: "Выберите темы и начните проверку знаний.",
    submitTest: "Завершить тест",
    buildingTest: "Формируем тест",
    buildingTestHint: "Равномерно распределяем вопросы между выбранными темами.",
    topics: "тем",
    topic: "тема",
    questions: "вопросов",
    question: "вопрос",
    selected: "выбрано",
    availableForSelection: "Для выбранных тем доступно вопросов: {count}.",
    noTopics: "В этом курсе пока нет активных тем.",
    selectTopic: "Выберите хотя бы одну тему.",
    invalidCount: "Выберите количество вопросов от 1 до {count}.",
    checkQuestion: "Проверить вопрос",
    chooseAnswer: "Сначала выберите ответ.",
    correct: "Верно.",
    incorrect: "Есть ошибка. Правильный ответ подсвечен.",
    excellent: "Отлично!",
    good: "Хороший результат!",
    needsPractice: "Нужно ещё потренироваться",
    explanation: "Объяснение",
    yourAnswer: "Ваш ответ",
    correctAnswer: "Правильный ответ",
    notAnswered: "Нет ответа",
    answered: "Отвечено: {answered} из {total}",
    score: "Результат",
    correctAnswers: "Верно: {correct} из {total}",
    unanswered: "Без ответа: {count}",
    submitConfirm: "Вы уверены, что хотите завершить тест?",
    saved: "Результат сохранен в профиле.",
    guest: "Войдите, чтобы сохранять следующие результаты.",
    mistakes: "Разобрать:",
    questionLabel: "Вопрос {number}",
    newTest: "Начать новый тест",
    stageFoundations: "1 · Основы",
    stageCollections: "2 · Коллекции",
    stageFlow: "3 · Условия и циклы",
    stageFunctions: "4 · Функции и повторное использование кода",
    stageToolkit: "5 · Инструменты Python",
    stageOop: "6 · ООП и файлы",
    stageDeep: "7 · Углублённый Python",
    joinRoomTitle: "Присоединиться к комнате",
    joinRoomDesc: "Если преподаватель дал вам 6-значный код, введите его здесь.",
    joinRoomBtn: "Войти",
    resultCorrect: "Верно",
    resultUnanswered: "Без ответа",
    resultStatus: "Статус",
    resultSaved: "Сохранено",
    resultGuest: "Гость",
  },
};

const state = {
  language: localStorage.getItem("quizLanguage") === "ru" ? "ru" : "en",
  courseId: bootstrap.catalog[0]?.id || null,
  selectedTopics: new Set(),
  quizToken: null,
  questions: [],
  answers: {},
  checked: new Set(),
  submitted: false,
  timerInterval: null,
  timerRemaining: null,
};

const courseList = document.getElementById("courseList");
const topicList = document.getElementById("topicList");
const selectionSummary = document.getElementById("selectionSummary");
const quizSize = document.getElementById("quizSize");
const difficulty = document.getElementById("difficulty");
const availabilityHint = document.getElementById("availabilityHint");
const instantCheck = document.getElementById("instantCheck");
const generateBtn = document.getElementById("generateBtn");
const builderError = document.getElementById("builderError");
const quizArea = document.getElementById("quizArea");
const quizEmpty = document.getElementById("quizEmpty");
const quizHeader = document.getElementById("quizHeader");
const quizTitle = document.getElementById("quizTitle");
const quizProgress = document.getElementById("quizProgress");
const summaryBox = document.getElementById("summaryBox");
const topicResults = document.getElementById("topicResults");
const mistakeNav = document.getElementById("mistakeNav");
const submitButton = document.getElementById("checkBtnBottom");
const loadingOverlay = document.getElementById("loadingOverlay");
const fontSizeSlider = document.getElementById("fontSize");
const fontSizeValue = document.getElementById("fontSizeValue");

function t(key, values = {}) {
  let value = copy[state.language][key] || key;
  Object.entries(values).forEach(([name, replacement]) => {
    value = value.replace(`{${name}}`, replacement);
  });
  return value;
}

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
  return labels[state.language][theme] || labels[state.language].auto;
}

function csrfToken() {
  return document.querySelector('meta[name="csrf-token"]').content;
}

async function api(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken() },
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}

function currentCourse() {
  return bootstrap.catalog.find((course) => course.id === state.courseId);
}

function localized(item, field = "title") {
  return item[`${field}_${state.language}`] || item[`${field}_${state.language === "en" ? "ru" : "en"}`] || "";
}

function selectedAvailableCount() {
  const course = currentCourse();
  if (!course) return 0;
  const countField = difficulty.value === "all" ? "question_count" : `${difficulty.value}_count`;
  return course.topics
    .filter((topic) => state.selectedTopics.has(topic.id))
    .reduce((sum, topic) => sum + Number(topic[countField] || 0), 0);
}

function stageForTopic(sortOrder) {
  if (sortOrder <= 8) return "stageFoundations";
  if (sortOrder <= 12) return "stageCollections";
  if (sortOrder <= 16) return "stageFlow";
  if (sortOrder <= 21) return "stageFunctions";
  if (sortOrder <= 27) return "stageToolkit";
  if (sortOrder <= 30) return "stageOop";
  return "stageDeep";
}

function applyTranslations() {
  document.documentElement.lang = state.language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAria));
  });
  document.querySelectorAll(".language-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.language === state.language);
  });
  renderCatalog();
  if (state.questions.length) {
    quizTitle.textContent = state.questions.map((question) => question.topic).filter((value, index, all) => all.indexOf(value) === index).join(" + ");
    updateProgress();
  }
  applyTheme(localStorage.getItem("theme") || "auto");
}

function renderCatalog() {
  courseList.innerHTML = "";
  bootstrap.catalog.forEach((course) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `course-card${course.id === state.courseId ? " is-active" : ""}`;
    button.innerHTML = `
      <span class="course-card__mark">${localized(course).slice(0, 2).toUpperCase()}</span>
      <span>
        <strong>${localized(course)}</strong>
        <small>${course.topic_count} ${t("topics")} · ${course.question_count} ${t("questions")}</small>
      </span>
    `;
    button.addEventListener("click", () => {
      state.courseId = course.id;
      state.selectedTopics.clear();
      renderCatalog();
    });
    courseList.appendChild(button);
  });

  topicList.innerHTML = "";
  const course = currentCourse();
  if (!course?.topics.length) {
    topicList.innerHTML = `<div class="empty-state">${t("noTopics")}</div>`;
  } else {
    const groups = new Map();
    course.topics.forEach((topic) => {
      const stage = stageForTopic(Number(topic.sort_order));
      if (!groups.has(stage)) groups.set(stage, []);
      groups.get(stage).push(topic);
    });
    let stageIndex = 0;
    groups.forEach((topics, stage) => {
      const section = document.createElement("section");
      section.className = "topic-stage";
      // Open the first stage by default
      if (stageIndex === 0) {
        section.classList.add("is-open");
      }
      
      const heading = document.createElement("h3");
      heading.textContent = t(stage);
      heading.addEventListener("click", () => {
        section.classList.toggle("is-open");
      });
      
      const grid = document.createElement("div");
      grid.className = "topic-grid";
      topics.forEach((topic) => {
      const label = document.createElement("label");
      label.className = `topic-card${state.selectedTopics.has(topic.id) ? " is-selected" : ""}`;
      label.innerHTML = `
        <input type="checkbox" value="${topic.id}" ${state.selectedTopics.has(topic.id) ? "checked" : ""} />
        <span class="topic-card__check">✓</span>
        <span class="topic-card__body">
          <strong>${localized(topic)}</strong>
          <small>${localized(topic, "description")}</small>
          <span class="topic-card__count">${topic.question_count} ${t(topic.question_count === 1 ? "question" : "questions")}</span>
        </span>
      `;
      label.querySelector("input").addEventListener("change", (event) => {
        if (event.target.checked) state.selectedTopics.add(topic.id);
        else state.selectedTopics.delete(topic.id);
        renderCatalog();
      });
        grid.appendChild(label);
      });
      section.append(heading, grid);
      topicList.appendChild(section);
      stageIndex++;
    });
  }

  const selectedCount = state.selectedTopics.size;
  selectionSummary.textContent = `${selectedCount} ${t("selected")}`;
  const available = selectedAvailableCount();
  availabilityHint.textContent = t("availableForSelection", { count: available });
  quizSize.max = Math.max(available, 1);
  if (available && Number(quizSize.value) > available) quizSize.value = available;
  document.querySelectorAll("[data-quiz-size]").forEach((button) => {
    const size = Number(button.dataset.quizSize);
    button.disabled = size > available;
    button.classList.toggle("is-active", Number(quizSize.value) === size);
  });
  [...difficulty.options].forEach((option) => {
    if (option.value === "all") return;
    const field = `${option.value}_count`;
    const count = (course?.topics || [])
      .filter((topic) => state.selectedTopics.has(topic.id))
      .reduce((sum, topic) => sum + Number(topic[field] || 0), 0);
    option.disabled = selectedCount > 0 && count === 0;
  });
  generateBtn.disabled = !selectedCount || !available;
}

function setBuilderError(message = "") {
  builderError.textContent = message;
  builderError.classList.toggle("hidden", !message);
}

function resetQuiz() {
  state.quizToken = null;
  state.questions = [];
  state.answers = {};
  state.checked.clear();
  state.submitted = false;
  quizArea.innerHTML = "";
  quizHeader.classList.add("hidden");
  quizEmpty.classList.remove("hidden");
  summaryBox.classList.add("hidden");
  topicResults.classList.add("hidden");
  mistakeNav.classList.add("hidden");
  submitButton.disabled = true;
  clearQuizTimer();
}

function updateTimerDisplay() {
  const min = Math.floor(state.timerRemaining / 60).toString().padStart(2, "0");
  const sec = (state.timerRemaining % 60).toString().padStart(2, "0");
  const timerEl = document.getElementById("quizTimer");
  if (timerEl) {
    timerEl.textContent = `${min}:${sec}`;
    if (state.timerRemaining <= 60) {
      timerEl.style.color = "var(--danger)";
    } else {
      timerEl.style.color = "var(--ink)";
    }
  }
}

function startQuizTimer(minutes) {
  clearQuizTimer();
  state.timerRemaining = minutes * 60;
  
  const timerEl = document.getElementById("quizTimer");
  if (timerEl) {
    timerEl.classList.remove("hidden");
    timerEl.style.color = "var(--ink)";
  }
  
  updateTimerDisplay();
  
  state.timerInterval = setInterval(() => {
    state.timerRemaining -= 1;
    updateTimerDisplay();
    if (state.timerRemaining <= 0) {
      clearQuizTimer();
      submitQuiz(); // Auto submit
    }
  }, 1000);
}

function clearQuizTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
  }
  const timerEl = document.getElementById("quizTimer");
  if (timerEl) timerEl.classList.add("hidden");
}

function updateProgress() {
  const answered = Object.keys(state.answers).length;
  quizProgress.textContent = t("answered", { answered, total: state.questions.length });
}

function renderQuestion(question, index) {
  const card = document.createElement("article");
  card.className = "question-card";
  card.dataset.questionId = question.id;

  const heading = document.createElement("div");
  heading.className = "question-title";
  heading.innerHTML = `<span class="q-number">${index + 1}.</span> <span></span>`;
  heading.querySelector("span:last-child").textContent = question.text;
  card.appendChild(heading);

  const topic = document.createElement("div");
  topic.className = "question-meta";
  topic.textContent = `${question.topic} · ${t(question.difficulty)}`;
  card.appendChild(topic);

  const options = document.createElement("div");
  options.className = "options";
  
  const qType = question.question_type || "mcq";

  if (qType === "mcq" || qType === "true_false") {
    question.options.forEach((option, optionIndex) => {
      const row = document.createElement("label");
      row.className = "option";
      row.dataset.option = optionIndex;
      const radio = document.createElement("input");
      radio.type = "radio";
      radio.name = `question-${question.id}`;
      radio.value = optionIndex;
      radio.checked = state.answers[String(question.id)] === optionIndex;
      radio.disabled = state.submitted;
      radio.addEventListener("change", () => {
        state.answers[String(question.id)] = optionIndex;
        clearFeedback(card);
        state.checked.delete(question.id);
        updateProgress();
      });
      const marker = document.createElement("span");
      marker.className = "option-label";
      marker.textContent = String.fromCharCode(65 + optionIndex);
      const text = document.createElement("div");
      text.className = "option-text";
      text.textContent = option.text;
      row.append(radio, marker, text);
      options.appendChild(row);
    });
  } else if (qType === "multi_select") {
    const currentAnswers = new Set(state.answers[String(question.id)] || []);
    question.options.forEach((option, optionIndex) => {
      const row = document.createElement("label");
      row.className = "option";
      row.dataset.option = optionIndex;
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = `question-${question.id}`;
      checkbox.value = optionIndex;
      checkbox.checked = currentAnswers.has(optionIndex);
      checkbox.disabled = state.submitted;
      checkbox.addEventListener("change", (e) => {
        if (e.target.checked) currentAnswers.add(optionIndex);
        else currentAnswers.delete(optionIndex);
        
        if (currentAnswers.size > 0) {
            state.answers[String(question.id)] = Array.from(currentAnswers);
        } else {
            delete state.answers[String(question.id)];
        }
        clearFeedback(card);
        state.checked.delete(question.id);
        updateProgress();
      });
      const marker = document.createElement("span");
      marker.className = "option-label";
      marker.innerHTML = `✓`;
      const text = document.createElement("div");
      text.className = "option-text";
      text.textContent = option.text;
      row.append(checkbox, marker, text);
      options.appendChild(row);
    });
  } else if (qType === "fill_in_the_blank" || qType === "code_output") {
    const inputRow = document.createElement("div");
    inputRow.className = "option-text-input";
    inputRow.style.padding = "0.5rem 0";
    
    let inputEl;
    if (qType === "code_output") {
      inputEl = document.createElement("textarea");
      inputEl.rows = 3;
      inputEl.style.fontFamily = "monospace";
    } else {
      inputEl = document.createElement("input");
      inputEl.type = "text";
    }
    
    inputEl.className = "text-input";
    inputEl.value = state.answers[String(question.id)] || "";
    inputEl.disabled = state.submitted;
    inputEl.placeholder = t("chooseAnswer");
    inputEl.style.width = "100%";
    inputEl.addEventListener("input", (e) => {
      const val = e.target.value;
      if (val.trim()) {
        state.answers[String(question.id)] = val;
      } else {
        delete state.answers[String(question.id)];
      }
      clearFeedback(card);
      state.checked.delete(question.id);
      updateProgress();
    });
    
    inputRow.appendChild(inputEl);
    options.appendChild(inputRow);
  }

  card.appendChild(options);

  const feedback = document.createElement("div");
  feedback.className = "question-feedback hidden";
  card.appendChild(feedback);

  if (instantCheck.checked) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "button button--soft question-check";
    button.textContent = t("checkQuestion");
    button.addEventListener("click", () => checkOne(question, card));
    card.appendChild(button);
  }
  return card;
}

function renderQuiz() {
  quizArea.innerHTML = "";
  state.questions.forEach((question, index) => quizArea.appendChild(renderQuestion(question, index)));
  quizEmpty.classList.add("hidden");
  quizHeader.classList.remove("hidden");
  submitButton.disabled = false;
  updateProgress();
}

function clearFeedback(card) {
  card.classList.remove("question--unanswered");
  card.querySelectorAll(".option").forEach((row) => row.classList.remove("option--correct", "option--wrong"));
  card.querySelectorAll(".option-rationale").forEach((el) => el.remove());
  const feedback = card.querySelector(".question-feedback");
  feedback.className = "question-feedback hidden";
  feedback.textContent = "";
}

function applyAssessment(card, assessment) {
  clearFeedback(card);
  if (assessment.is_unanswered) card.classList.add("question--unanswered");
  card.querySelectorAll(".option").forEach((row, index) => {
    if (assessment.correct_options.includes(index)) row.classList.add("option--correct");
    if (assessment.selected === index && !assessment.is_correct) row.classList.add("option--wrong");
    
    const optionData = assessment.options[index];
    if (optionData && optionData.rationale) {
      const rationaleEl = document.createElement("div");
      rationaleEl.className = "option-rationale";
      rationaleEl.textContent = optionData.rationale;
      row.querySelector(".option-text").appendChild(rationaleEl);
    }
  });
  const feedback = card.querySelector(".question-feedback");
  feedback.className = `question-feedback ${assessment.is_correct ? "question-feedback--correct" : "question-feedback--wrong"}`;
  const message = assessment.is_unanswered ? t("chooseAnswer") : assessment.is_correct ? t("correct") : t("incorrect");
  feedback.innerHTML = "";

  const status = document.createElement("strong");
  status.className = "feedback-status";
  status.textContent = message;
  feedback.appendChild(status);

  const answers = document.createElement("div");
  answers.className = "feedback-answers";
  const selected = document.createElement("span");
  selected.textContent = `${t("yourAnswer")}: ${assessment.selected_answer || t("notAnswered")}`;
  const correct = document.createElement("span");
  correct.textContent = `${t("correctAnswer")}: ${(assessment.correct_answers || []).join(", ")}`;
  answers.append(selected, correct);
  feedback.appendChild(answers);

  if (assessment.explanation) {
    const explanation = document.createElement("div");
    explanation.className = "feedback-explanation";
    const title = document.createElement("strong");
    title.textContent = t("explanation");
    const body = document.createElement("div");
    body.textContent = assessment.explanation;
    explanation.append(title, body);
    feedback.appendChild(explanation);
  }
}

async function checkOne(question, card) {
  const selected = state.answers[String(question.id)];
  if (selected === undefined) {
    applyAssessment(card, {
      selected: null,
      selected_answer: null,
      correct_answers: [],
      correct_options: [],
      is_correct: false,
      is_unanswered: true,
      explanation: "",
    });
    return;
  }
  try {
    const assessment = await api(`/api/quizzes/${state.quizToken}/check`, {
      question_id: question.id,
      selected,
    });
    applyAssessment(card, assessment);
    state.checked.add(question.id);
  } catch (error) {
    setBuilderError(error.message);
  }
}

function triggerConfetti() {
  const colors = ["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899"];
  for (let i = 0; i < 50; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";
    confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.left = Math.random() * 100 + "vw";
    confetti.style.animationDelay = Math.random() * 2 + "s";
    confetti.style.animationDuration = Math.random() * 3 + 2 + "s";
    document.body.appendChild(confetti);
    setTimeout(() => confetti.remove(), 5000);
  }
}

function renderResult(result, savedResult) {
  const scorePercent = result.score_percent || 0;
  const gradeClass = scorePercent >= 80 ? "score-card--good" : scorePercent >= 50 ? "score-card--medium" : "score-card--low";
  const gradeMessage = scorePercent >= 80 ? t("excellent") : scorePercent >= 50 ? t("good") : t("needsPractice");

  summaryBox.innerHTML = `
    <div class="score-card ${gradeClass}">
      <div class="score-circle">
        <svg viewBox="0 0 36 36" class="circular-chart">
          <path class="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path class="circle animate-circle"
            stroke-dasharray="${scorePercent}, 100"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <text x="18" y="20.35" class="percentage animate-fade-in">${scorePercent}%</text>
        </svg>
      </div>
      <div class="score-details">
        <h2 class="score-message animate-slide-up">${gradeMessage}</h2>
        <div class="score-stats">
          <div class="stat-item animate-slide-up" style="animation-delay: 0.1s">
            <strong>${result.correct} / ${result.total}</strong>
            <span>${t("resultCorrect")}</span>
          </div>
          <div class="stat-item animate-slide-up" style="animation-delay: 0.2s">
            <strong>${result.unanswered}</strong>
            <span>${t("resultUnanswered")}</span>
          </div>
          <div class="stat-item animate-slide-up" style="animation-delay: 0.3s">
            <strong>${savedResult ? t("resultSaved") : t("resultGuest")}</strong>
            <span>${t("resultStatus")}</span>
          </div>
        </div>
      </div>
    </div>
  `;
  summaryBox.className = "results-summary results-summary--animated";

  if (scorePercent >= 80) {
    triggerConfetti();
  }


  topicResults.innerHTML = "";
  Object.entries(result.topic_stats).forEach(([topic, stats]) => {
    const item = document.createElement("div");
    item.className = "topic-result";
    item.innerHTML = `<strong>${topic}</strong><span>${stats.correct}/${stats.total}</span>`;
    topicResults.appendChild(item);
  });
  topicResults.classList.remove("hidden");

  const mistakes = [];
  result.review.forEach((assessment, index) => {
    const card = quizArea.querySelector(`[data-question-id="${assessment.question_id}"]`);
    if (card) {
      applyAssessment(card, assessment);
      card.querySelectorAll("input").forEach((input) => { input.disabled = true; });
      card.querySelector(".question-check")?.remove();
    }
    if (!assessment.is_correct) mistakes.push(index);
  });
  mistakeNav.innerHTML = `<strong>${t("mistakes")}</strong>`;
  mistakes.forEach((index) => {
    const button = document.createElement("button");
    button.className = "mistake-chip";
    button.textContent = t("questionLabel", { number: index + 1 });
    button.addEventListener("click", () => {
      quizArea.children[index]?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    mistakeNav.appendChild(button);
  });
  mistakeNav.classList.toggle("hidden", !mistakes.length);
}

async function startQuiz() {
  setBuilderError();
  const available = selectedAvailableCount();
  const count = Number(quizSize.value);
  if (!state.selectedTopics.size) {
    setBuilderError(t("selectTopic"));
    return;
  }
  if (!Number.isInteger(count) || count < 1 || count > available) {
    setBuilderError(t("invalidCount", { count: available }));
    return;
  }
  loadingOverlay.classList.remove("hidden");
  try {
    const result = await api("/api/quizzes", {
      topic_ids: [...state.selectedTopics],
      count,
      language: state.language,
      difficulty: difficulty.value,
    });
    state.quizToken = result.token;
    state.questions = result.questions;
    state.answers = {};
    state.checked.clear();
    state.submitted = false;
    quizTitle.textContent = result.topics.join(" + ");
    summaryBox.classList.add("hidden");
    topicResults.classList.add("hidden");
    mistakeNav.classList.add("hidden");
    renderQuiz();
    document.querySelector(".quiz-stage").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    setBuilderError(error.message);
  } finally {
    loadingOverlay.classList.add("hidden");
  }
}

async function joinRoom(event) {
  event.preventDefault();
  const input = document.getElementById("roomCodeInput");
  const code = input.value.trim().toUpperCase();
  if (!code) return;
  
  const errorEl = document.getElementById("joinRoomError");
  errorEl.textContent = "";
  errorEl.classList.add("hidden");
  loadingOverlay.classList.remove("hidden");
  
  try {
    const result = await api("/api/quizzes/room", { code, language: state.language });
    state.quizToken = result.token;
    state.questions = result.questions;
    state.answers = {};
    state.checked.clear();
    state.submitted = false;
    quizTitle.textContent = result.topics.join(" + ");
    summaryBox.classList.add("hidden");
    topicResults.classList.add("hidden");
    mistakeNav.classList.add("hidden");
    renderQuiz();
    document.querySelector(".quiz-stage").scrollIntoView({ behavior: "smooth", block: "start" });
    if (result.time_limit_minutes) {
      startQuizTimer(result.time_limit_minutes);
    }
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
  } finally {
    loadingOverlay.classList.add("hidden");
  }
}

async function submitQuiz() {
  if (!state.quizToken || state.submitted) return;

  const unanswered = state.questions.filter((q) => {
    const ans = state.answers[q.id];
    if (q.question_type === "multi_select") {
      return !ans || ans.length === 0;
    }
    return ans === undefined || ans === null || ans === "";
  });

  if (unanswered.length > 0) {
    const confirmMessage = (t("unanswered", { count: unanswered.length }) || "You have unanswered questions.") + "\n" + (t("submitConfirm") || "Are you sure you want to submit?");
    if (!confirm(confirmMessage)) return;
  }

  submitButton.disabled = true;
  clearQuizTimer();
  try {
    const payload = await api(`/api/quizzes/${state.quizToken}/submit`, { answers: state.answers });
    state.submitted = true;
    renderResult(payload.result, payload.saved_result);
    summaryBox.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    setBuilderError(error.message);
    submitButton.disabled = false;
  }
}

function applyFontSize(value) {
  const normalized = Number(value) || 100;
  fontSizeSlider.value = normalized;
  fontSizeValue.textContent = `${normalized}%`;
  document.documentElement.style.setProperty("--quiz-font-size", `${normalized / 100}rem`);
  localStorage.setItem("quizFontSize", normalized);
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

document.querySelectorAll(".language-button").forEach((button) => {
  button.addEventListener("click", () => {
    state.language = button.dataset.language;
    localStorage.setItem("quizLanguage", state.language);
    applyTranslations();
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
instantCheck.addEventListener("change", () => {
  if (state.questions.length && !state.submitted) renderQuiz();
});
quizSize.addEventListener("input", () => setBuilderError());
difficulty.addEventListener("change", renderCatalog);
document.querySelectorAll("[data-quiz-size]").forEach((button) => {
  button.addEventListener("click", () => {
    quizSize.value = button.dataset.quizSize;
    renderCatalog();
  });
});
generateBtn.addEventListener("click", startQuiz);
submitButton.addEventListener("click", submitQuiz);
document.getElementById("joinRoomForm")?.addEventListener("submit", joinRoom);
fontSizeSlider.addEventListener("input", () => applyFontSize(fontSizeSlider.value));

document.getElementById("catalogQuestionCount").textContent = bootstrap.catalog.reduce(
  (sum, course) => sum + Number(course.question_count),
  0
);
applyFontSize(localStorage.getItem("quizFontSize") || 100);
applyTheme(localStorage.getItem("theme") || "auto");
applyTranslations();
resetQuiz();
