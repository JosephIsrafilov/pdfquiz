const bootstrap = window.APP_BOOTSTRAP || {
  currentUser: null,
  documents: [],
  results: [],
};

const state = {
  questions: [],
  quiz: [],
  answers: {},
  submitted: false,
  sourceLabel: "",
  sourceDocumentId: null,
  checkedQuestions: {},
};

const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const documentSelect = document.getElementById("documentSelect");
const questionCount = document.getElementById("questionCount");
const sourceLabel = document.getElementById("sourceLabel");
const rangeStart = document.getElementById("rangeStart");
const rangeEnd = document.getElementById("rangeEnd");
const rangeHint = document.getElementById("rangeHint");
const rangeWarning = document.getElementById("rangeWarning");
const quizSize = document.getElementById("quizSize");
const quizSizeHint = document.getElementById("quizSizeHint");
const instantCheck = document.getElementById("instantCheck");
const generateBtn = document.getElementById("generateBtn");
const checkBtn = document.getElementById("checkBtn");
const checkBtnBottom = document.getElementById("checkBtnBottom");
const quizArea = document.getElementById("quizArea");
const quizEmpty = document.getElementById("quizEmpty");
const summaryBox = document.getElementById("summaryBox");
const mistakeNav = document.getElementById("mistakeNav");
const fontSizeSlider = document.getElementById("fontSize");
const fontSizeValue = document.getElementById("fontSizeValue");
const loadingOverlay = document.getElementById("loadingOverlay");
const highlightMenu = document.getElementById("highlightMenu");
const publicLink = document.getElementById("publicLink");
const copyLink = document.getElementById("copyLink");
const resultsHistory = document.getElementById("resultsHistory");
const historyEmpty = document.getElementById("historyEmpty");
const isTouchDevice =
  "ontouchstart" in window || navigator.maxTouchPoints > 0;

function showLoading(show) {
  loadingOverlay.classList.toggle("hidden", !show);
}

function shuffle(array) {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function sample(array, count) {
  return shuffle(array).slice(0, count);
}

function resetState() {
  state.quiz = [];
  state.answers = {};
  state.submitted = false;
  state.checkedQuestions = {};
  quizArea.innerHTML = "";
  summaryBox.textContent = "";
  summaryBox.classList.add("hidden");
  mistakeNav.classList.add("hidden");
  mistakeNav.innerHTML = "";
  quizEmpty.classList.remove("hidden");
  checkBtn.disabled = true;
  checkBtnBottom.disabled = true;
}

function setRangeLimits(total) {
  const max = total || 1;
  rangeStart.max = max;
  rangeEnd.max = max;
  rangeStart.value = total ? 1 : 1;
  rangeEnd.value = total ? total : 1;
  quizSize.max = max;
  quizSize.value = total ? Math.min(50, total) : 1;
}

function getSelectedRangeCount() {
  const start = Number(rangeStart.value);
  const end = Number(rangeEnd.value);
  if (!state.questions.length || Number.isNaN(start) || Number.isNaN(end) || start > end) {
    return 0;
  }
  return end - start + 1;
}

function updateControlsState() {
  const total = state.questions.length;
  const start = Number(rangeStart.value);
  const end = Number(rangeEnd.value);
  const available = getSelectedRangeCount();
  let desired = Number(quizSize.value);

  if (!total) {
    rangeHint.textContent = "Сначала выбери файл или готовый документ.";
    rangeWarning.textContent = "";
    quizSizeHint.textContent = "Количество можно задать вручную в пределах выбранного диапазона.";
    generateBtn.disabled = true;
    return;
  }

  if (start > end) {
    rangeWarning.textContent = "Начало диапазона не может быть больше конца.";
    generateBtn.disabled = true;
    return;
  }

  if (!desired || desired < 1) {
    desired = 1;
  }
  if (available > 0 && desired > available) {
    desired = available;
  }
  quizSize.value = desired;
  quizSize.max = Math.max(available, 1);

  rangeHint.textContent = `В диапазоне доступно ${available} вопросов из ${total}.`;
  quizSizeHint.textContent = `В пробник попадут случайные ${desired} вопросов из выбранного диапазона.`;
  rangeWarning.textContent = available ? "" : "В выбранном диапазоне нет вопросов.";
  generateBtn.disabled = !available;
}

function makeHighlightable(element) {
  if (isTouchDevice) {
    element.setAttribute("contenteditable", "false");
    return;
  }
  element.setAttribute("contenteditable", "true");
  element.setAttribute("spellcheck", "false");
  element.addEventListener("beforeinput", (event) => {
    event.preventDefault();
  });
  element.addEventListener("paste", (event) => {
    event.preventDefault();
  });
}

summaryBox.classList.add("hl-text");
makeHighlightable(summaryBox);

function createHighlightText(text, isHtml = false) {
  const element = document.createElement("div");
  element.className = "hl-text";
  if (isHtml) {
    element.innerHTML = text;
  } else {
    element.textContent = text;
  }
  makeHighlightable(element);
  return element;
}

function applyFontSize(value) {
  const normalized = Number(value) || 100;
  fontSizeSlider.value = normalized;
  fontSizeValue.textContent = `${normalized}%`;
  document.documentElement.style.setProperty("--quiz-font-size", `${normalized / 100}rem`);
  localStorage.setItem("quizFontSize", String(normalized));
}

function renderQuiz() {
  quizArea.innerHTML = "";
  quizEmpty.classList.add("hidden");

  state.quiz.forEach((question, index) => {
    const card = document.createElement("div");
    card.className = "question-card";
    card.dataset.q = index;
    card.style.animationDelay = `${index * 0.02}s`;

    const title = createHighlightText(
      `<span class="q-number">${index + 1}.</span> ${question.text} ${
        question.number ? `<span class="origin">(ориг. №${question.number})</span>` : ""
      }`,
      true
    );
    title.classList.add("question-title");
    card.appendChild(title);

    const options = document.createElement("div");
    options.className = "options";

    question.options.forEach((option, optIndex) => {
      const optionRow = document.createElement("label");
      optionRow.className = "option";
      optionRow.dataset.q = index;
      optionRow.dataset.opt = optIndex;

      const radio = document.createElement("input");
      radio.type = "radio";
      radio.name = `q_${index}`;
      radio.value = String(optIndex);
      radio.checked = state.answers[index] === optIndex;

      const marker = document.createElement("span");
      marker.className = "option-label";
      marker.textContent = String.fromCharCode(65 + optIndex);

      const text = createHighlightText(option.text, false);
      text.classList.add("option-text");

      const setAnswer = () => {
        state.answers[index] = optIndex;
        radio.checked = true;
        if (state.checkedQuestions[index]) {
          clearQuestionFeedback(index);
          delete state.checkedQuestions[index];
        }
      };

      radio.addEventListener("change", setAnswer);
      optionRow.addEventListener("click", (event) => {
        const selection = window.getSelection();
        if (selection && selection.toString()) {
          return;
        }
        if (event.target.closest(".hl-text")) {
          setAnswer();
        }
      });

      optionRow.appendChild(radio);
      optionRow.appendChild(marker);
      optionRow.appendChild(text);
      options.appendChild(optionRow);
    });

    card.appendChild(options);

    if (instantCheck && instantCheck.checked) {
      const actions = document.createElement("div");
      actions.className = "question-actions";

      const status = document.createElement("div");
      status.className = "question-status hidden";
      status.dataset.statusFor = index;

      const button = document.createElement("button");
      button.type = "button";
      button.className = "button button--soft";
      button.textContent = "Проверить вопрос";
      button.addEventListener("click", () => {
        checkSingleQuestion(index);
      });

      actions.appendChild(status);
      actions.appendChild(button);
      card.appendChild(actions);
    }

    quizArea.appendChild(card);
  });
}

function getQuestionAssessment(question, selected) {
  const correctIndices = question.options
    .map((option, index) => (option.is_correct ? index : null))
    .filter((value) => value !== null);

  return {
    hasAnswer: selected !== undefined,
    hasAnswerKey: correctIndices.length > 0,
    isCorrect: correctIndices.includes(selected),
  };
}

function clearQuestionFeedback(qIndex) {
  const card = quizArea.querySelector(`.question-card[data-q="${qIndex}"]`);
  if (card) {
    card.classList.remove("question--unanswered");
  }

  state.quiz[qIndex]?.options.forEach((_option, optIndex) => {
    const row = quizArea.querySelector(`.option[data-q="${qIndex}"][data-opt="${optIndex}"]`);
    if (row) {
      row.classList.remove("option--correct", "option--wrong");
    }
  });

  const status = quizArea.querySelector(`.question-status[data-status-for="${qIndex}"]`);
  if (status) {
    status.textContent = "";
    status.className = "question-status hidden";
  }
}

function applyQuestionFeedback(qIndex) {
  const question = state.quiz[qIndex];
  if (!question) {
    return {
      hasAnswer: false,
      hasAnswerKey: false,
      isCorrect: false,
    };
  }

  clearQuestionFeedback(qIndex);

  const selected = state.answers[qIndex];
  const assessment = getQuestionAssessment(question, selected);
  const card = quizArea.querySelector(`.question-card[data-q="${qIndex}"]`);
  const status = quizArea.querySelector(`.question-status[data-status-for="${qIndex}"]`);

  if (card && !assessment.hasAnswer) {
    card.classList.add("question--unanswered");
  }

  question.options.forEach((option, optIndex) => {
    const row = quizArea.querySelector(`.option[data-q="${qIndex}"][data-opt="${optIndex}"]`);
    if (!row) {
      return;
    }
    const isCorrect = Boolean(option.is_correct);
    if (selected === optIndex) {
      row.classList.add(isCorrect ? "option--correct" : "option--wrong");
    }
    if (isCorrect && selected !== optIndex) {
      row.classList.add("option--correct");
    }
  });

  if (status) {
    status.classList.remove("hidden");
    if (!assessment.hasAnswer) {
      status.classList.add("question-status--info");
      status.textContent = "Сначала выбери вариант ответа.";
    } else if (!assessment.hasAnswerKey) {
      status.classList.add("question-status--info");
      status.textContent = "У этого вопроса нет отмеченного правильного ответа.";
    } else if (assessment.isCorrect) {
      status.classList.add("question-status--correct");
      status.textContent = "Верно.";
    } else {
      status.classList.add("question-status--wrong");
      status.textContent = "Ошибка. Правильный вариант подсвечен.";
    }
  }

  return assessment;
}

function checkSingleQuestion(qIndex) {
  const assessment = applyQuestionFeedback(qIndex);
  state.checkedQuestions[qIndex] = true;
  return assessment;
}

function applyQuizFeedback() {
  state.quiz.forEach((_question, qIndex) => {
    applyQuestionFeedback(qIndex);
    state.checkedQuestions[qIndex] = true;
  });
}

function scrollToQuestion(index) {
  const card = quizArea.querySelector(`.question-card[data-q="${index}"]`);
  if (!card) {
    return;
  }
  card.classList.add("question--jump");
  card.scrollIntoView({ behavior: "smooth", block: "start" });
  setTimeout(() => {
    card.classList.remove("question--jump");
  }, 1200);
}

function renderMistakeNav(mistakeItems) {
  if (!mistakeItems.length) {
    mistakeNav.classList.add("hidden");
    mistakeNav.innerHTML = "";
    return;
  }

  mistakeNav.innerHTML = "";
  const title = document.createElement("div");
  title.className = "mistake-nav__title";
  title.textContent = "Ошибки:";
  mistakeNav.appendChild(title);

  mistakeItems.forEach((item) => {
    const button = document.createElement("button");
    button.className = "mistake-chip";
    button.type = "button";
    button.textContent = item.label;
    button.addEventListener("click", () => scrollToQuestion(item.index));
    mistakeNav.appendChild(button);
  });

  mistakeNav.classList.remove("hidden");
}

function renderHistoryCard(result, prepend = false) {
  if (!resultsHistory) {
    return;
  }

  if (historyEmpty) {
    historyEmpty.remove();
  }

  const card = document.createElement("article");
  card.className = "history-card";

  const title = document.createElement("div");
  title.className = "history-card__title";
  title.textContent = result.source_label;

  const meta = document.createElement("div");
  meta.className = "history-card__meta";
  meta.textContent = result.created_at;

  const stats = document.createElement("div");
  stats.className = "history-card__stats";
  stats.innerHTML = `
    <span>${result.correct}/${result.graded} верно</span>
    <span>${result.quiz_size} в пробнике</span>
    <span>${result.unanswered} без ответа</span>
  `;

  card.appendChild(title);
  card.appendChild(meta);
  card.appendChild(stats);

  if (result.attempt_available) {
    const actions = document.createElement("div");
    actions.className = "history-card__actions";
    const link = document.createElement("a");
    link.className = "button";
    link.href = `/profile/results/${result.id}`;
    link.textContent = "Открыть попытку";
    actions.appendChild(link);
    card.appendChild(actions);
  }

  if (result.mistake_numbers && result.mistake_numbers.length) {
    const mistakes = document.createElement("div");
    mistakes.className = "history-card__mistakes";
    mistakes.textContent = `Ошибки по номерам в документе: ${result.mistake_numbers.join(", ")}`;
    card.appendChild(mistakes);
  }

  if (prepend && resultsHistory.firstChild) {
    resultsHistory.prepend(card);
  } else {
    resultsHistory.appendChild(card);
  }
}

async function saveResult(summary) {
  if (!bootstrap.currentUser) {
    return;
  }

  const response = await fetch("/api/results", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
    },
    body: JSON.stringify({
      ...summary,
      document_id: state.sourceDocumentId,
      source_label: state.sourceLabel || "Загруженный файл",
      total_questions: state.questions.length,
      attempt: {
        quiz: state.quiz,
        answers: state.answers,
      },
    }),
  });

  const raw = await response.text();
  let data = {};
  try {
    data = raw ? JSON.parse(raw) : {};
  } catch (_error) {
    throw new Error("Сервер вернул некорректный ответ при сохранении результата.");
  }
  if (!response.ok) {
    throw new Error(data.error || "Не удалось сохранить результат");
  }

  if (data.result) {
    renderHistoryCard(data.result, true);
  }
}

function renderSummary() {
  const total = state.quiz.length;
  let correct = 0;
  let graded = 0;
  let unanswered = 0;
  let missingAnswerKey = 0;
  const mistakeItems = [];
  const mistakeNumbers = [];

  state.quiz.forEach((question, index) => {
    const selected = state.answers[index];
    const correctIndices = question.options
      .map((option, optIndex) => (option.is_correct ? optIndex : null))
      .filter((value) => value !== null);

    if (selected === undefined) {
      unanswered += 1;
    }

    if (!correctIndices.length) {
      missingAnswerKey += 1;
      return;
    }

    graded += 1;
    if (correctIndices.includes(selected)) {
      correct += 1;
    } else {
      const displayNumber = question.number || index + 1;
      mistakeNumbers.push(displayNumber);
      mistakeItems.push({
        index,
        label: question.number ? `№${question.number}` : `Вопрос ${index + 1}`,
      });
    }
  });

  const summaryLines = [
    `Правильных ответов: ${correct} из ${graded}`,
    `Без ответа: ${unanswered}`,
    `Размер пробника: ${total} вопросов`,
  ];

  if (mistakeNumbers.length) {
    summaryLines.push(`Номера ошибок в документе: ${mistakeNumbers.join(", ")}`);
  }

  if (missingAnswerKey) {
    summaryLines.push(
      `Вопросов без отмеченного правильного ответа: ${missingAnswerKey}. Они не учитывались.`
    );
  }

  if (bootstrap.currentUser) {
    summaryLines.push("Результат сохранен в аккаунте.");
  }

  summaryBox.textContent = summaryLines.join("\n");
  summaryBox.classList.remove("hidden");
  renderMistakeNav(mistakeItems);

  return {
    quiz_size: total,
    graded,
    correct,
    unanswered,
    missing_answer_key: missingAnswerKey,
    mistake_numbers: mistakeNumbers,
  };
}

function xhrParse(formData) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const progressWrap = document.getElementById("uploadProgressWrap");
    const progressBar = document.getElementById("uploadProgressBar");
    const progressText = document.getElementById("uploadProgressText");
    const spinner = document.getElementById("loadingSpinner");

    const hasFile = formData.has("file") && formData.get("file") instanceof File && formData.get("file").size > 0;
    if (hasFile) {
      spinner.classList.add("hidden");
      progressWrap.classList.remove("hidden");
      progressText.classList.remove("hidden");
      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          const pct = Math.round((e.loaded / e.total) * 100);
          progressBar.style.width = pct + "%";
          progressText.textContent = pct + "%";
        }
      };
    }

    xhr.open("POST", "/api/parse");
    xhr.setRequestHeader("X-CSRFToken", document.querySelector('meta[name="csrf-token"]').content);
    xhr.onload = () => {
      spinner.classList.remove("hidden");
      progressWrap.classList.add("hidden");
      progressText.classList.add("hidden");
      progressBar.style.width = "0%";
      resolve({ status: xhr.status, ok: xhr.status >= 200 && xhr.status < 300, text: () => xhr.responseText });
    };
    xhr.onerror = () => reject(new Error("Сетевая ошибка при загрузке файла"));
    xhr.send(formData);
  });
}

async function loadQuestions(formData) {
  showLoading(true);
  try {
    const response = await xhrParse(formData);
    const raw = response.text();
    let data = null;

    try {
      data = raw ? JSON.parse(raw) : {};
    } catch (_error) {
      if (response.status === 502 || response.status === 503 || response.status === 504) {
        throw new Error(
          "Сервер не успел обработать файл. На Render такое бывает с тяжелыми PDF. Попробуй позже или загрузи файл через админ-панель."
        );
      }
      throw new Error(
        "Сервер вернул не JSON, а страницу ошибки. Скорее всего файл обрабатывался слишком долго или Render отдал 502."
      );
    }

    if (!response.ok) {
      throw new Error(data.error || "Не удалось загрузить вопросы");
    }

    state.questions = data.questions || [];
    state.sourceDocumentId = data.document_id || null;
    state.sourceLabel = data.source_label || "Загруженный файл";

    questionCount.textContent = String(data.count || state.questions.length);
    sourceLabel.textContent = state.sourceLabel;
    setRangeLimits(state.questions.length);
    updateControlsState();
    resetState();
  } catch (error) {
    state.questions = [];
    state.sourceDocumentId = null;
    state.sourceLabel = "";
    questionCount.textContent = "0";
    sourceLabel.textContent = "—";
    setRangeLimits(0);
    updateControlsState();
    resetState();
    alert(error.message);
  } finally {
    showLoading(false);
  }
}

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) {
    return;
  }
  fileName.textContent = file.name;
  if (documentSelect) {
    documentSelect.value = "";
  }
  const formData = new FormData();
  formData.append("file", file);
  await loadQuestions(formData);
});

if (documentSelect) {
  documentSelect.addEventListener("change", async () => {
    const documentId = documentSelect.value;
    if (!documentId) {
      state.questions = [];
      state.sourceDocumentId = null;
      state.sourceLabel = "";
      questionCount.textContent = "0";
      sourceLabel.textContent = "—";
      setRangeLimits(0);
      updateControlsState();
      resetState();
      return;
    }

    fileInput.value = "";
    fileName.textContent = "Файл не выбран";

    const formData = new FormData();
    formData.append("document_id", documentId);
    await loadQuestions(formData);
  });
}

rangeStart.addEventListener("input", updateControlsState);
rangeEnd.addEventListener("input", updateControlsState);
quizSize.addEventListener("input", updateControlsState);
if (instantCheck) {
  instantCheck.addEventListener("change", () => {
    if (state.quiz.length) {
      renderQuiz();
    }
  });
}

fontSizeSlider.addEventListener("input", () => {
  applyFontSize(fontSizeSlider.value);
});

document.querySelectorAll("[data-font-size]").forEach((button) => {
  button.addEventListener("click", () => {
    applyFontSize(button.dataset.fontSize);
  });
});

generateBtn.addEventListener("click", () => {
  const start = Number(rangeStart.value);
  const end = Number(rangeEnd.value);
  const count = Number(quizSize.value);

  if (start > end) {
    alert("Начало диапазона больше конца.");
    return;
  }

  const pool = state.questions.slice(start - 1, end);
  if (!pool.length) {
    alert("В выбранном диапазоне нет вопросов.");
    return;
  }

  if (!count || count < 1 || count > pool.length) {
    alert("Проверь количество вопросов в пробнике.");
    return;
  }

  state.quiz = shuffle(
    sample(pool, count).map((question) => ({
      number: question.number,
      text: question.text,
      options: shuffle(question.options),
    }))
  );
  state.answers = {};
  state.submitted = false;
  state.checkedQuestions = {};
  renderQuiz();
  summaryBox.textContent = "";
  summaryBox.classList.add("hidden");
  mistakeNav.classList.add("hidden");
  mistakeNav.innerHTML = "";
  checkBtn.disabled = false;
  checkBtnBottom.disabled = false;
});

async function handleCheck() {
  if (!state.quiz.length) {
    return;
  }

  applyQuizFeedback();
  const summary = renderSummary();
  state.submitted = true;

  if (bootstrap.currentUser) {
    try {
      await saveResult(summary);
    } catch (error) {
      alert(error.message);
    }
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

checkBtn.addEventListener("click", handleCheck);
checkBtnBottom.addEventListener("click", handleCheck);

function updatePublicLink() {
  publicLink.textContent = window.location.origin;
}

copyLink.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(publicLink.textContent);
    copyLink.textContent = "Скопировано";
    setTimeout(() => {
      copyLink.textContent = "Копировать";
    }, 1200);
  } catch (_error) {
    alert("Не удалось скопировать ссылку.");
  }
});

let savedRange = null;
let savedRoot = null;

function getHighlightRoot(node) {
  if (!node) {
    return null;
  }
  const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
  if (!element) {
    return null;
  }
  return element.closest(".hl-text");
}

document.addEventListener("selectionchange", () => {
  const selection = window.getSelection();
  if (!selection || selection.rangeCount === 0) {
    return;
  }
  const range = selection.getRangeAt(0);
  const root = getHighlightRoot(range.commonAncestorContainer);
  if (!root) {
    return;
  }
  savedRange = range.cloneRange();
  savedRoot = root;
});

function applyHighlight(color) {
  if (!savedRange || !savedRoot) {
    return;
  }
  if (
    !savedRoot.contains(savedRange.startContainer) ||
    !savedRoot.contains(savedRange.endContainer)
  ) {
    return;
  }
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(savedRange);
  document.execCommand("styleWithCSS", false, true);
  document.execCommand("hiliteColor", false, color);
  selection.removeAllRanges();
}

function clearHighlight() {
  if (!savedRange || !savedRoot) {
    return;
  }
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(savedRange);
  document.execCommand("styleWithCSS", false, true);
  document.execCommand("hiliteColor", false, "transparent");
  selection.removeAllRanges();
}

function hideHighlightMenu() {
  highlightMenu.classList.add("hidden");
}

function showHighlightMenu(x, y) {
  highlightMenu.style.left = `${x}px`;
  highlightMenu.style.top = `${y}px`;
  highlightMenu.classList.remove("hidden");
}

function onContextMenu(event) {
  if (isTouchDevice) {
    return;
  }
  const target = event.target.closest(".hl-text");
  if (!target) {
    return;
  }
  event.preventDefault();
  showHighlightMenu(event.pageX, event.pageY);
}

quizArea.addEventListener("contextmenu", onContextMenu);
summaryBox.addEventListener("contextmenu", onContextMenu);

highlightMenu.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) {
    return;
  }
  if (button.dataset.clear === "true") {
    clearHighlight();
  } else {
    applyHighlight(button.dataset.color);
  }
  hideHighlightMenu();
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".hl-menu")) {
    hideHighlightMenu();
  }
});

applyFontSize(localStorage.getItem("quizFontSize") || 100);
updatePublicLink();
updateControlsState();
