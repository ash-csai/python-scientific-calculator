const inputBox = document.getElementById("calculator-display");
const previewBox = document.getElementById("expression-preview");
const historyList = document.getElementById("history-list");
const themeToggle = document.getElementById("theme-toggle");
const angleToggle = document.getElementById("angle-toggle");
const scientificToggle = document.getElementById("scientific-toggle");
const clearHistoryButton = document.getElementById("clear-history");
const body = document.body;

let angleMode = "deg";
let memoryValue = 0;

function appendValue(value) {
  const existing = inputBox.value;
  if (existing === "0" && ![".", "+", "-", "*", "/", "(", ")"].includes(value)) {
    inputBox.value = value;
  } else {
    inputBox.value += value;
  }
  syncPreview();
}

function clearInput() {
  inputBox.value = "";
  previewBox.textContent = "0";
}

function backspace() {
  inputBox.value = inputBox.value.slice(0, -1);
  syncPreview();
}

function toggleSign() {
  const current = inputBox.value.trim();
  if (!current) {
    return;
  }
  if (current.startsWith("-")) {
    inputBox.value = current.slice(1);
  } else {
    inputBox.value = `-${current}`;
  }
  syncPreview();
}

function applyPercentage() {
  const current = inputBox.value.trim();
  if (!current) {
    return;
  }
  inputBox.value = `(${current})/100`;
  syncPreview();
}

function syncPreview() {
  const value = inputBox.value.trim();
  previewBox.textContent = value || "0";
  resizeDisplay();
}

function resizeDisplay() {
  const value = inputBox.value || "0";
  const length = value.length;
  if (length > 14) {
    inputBox.style.fontSize = "1.35rem";
  } else if (length > 10) {
    inputBox.style.fontSize = "1.6rem";
  } else {
    inputBox.style.fontSize = "clamp(1.8rem, 4.4vw, 2.6rem)";
  }
}

async function calculate() {
  const expression = inputBox.value.trim();
  if (!expression) {
    return;
  }

  try {
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression, angle_mode: angleMode }),
    });
    const data = await response.json();
    if (!response.ok || data.status === "error") {
      throw new Error(data.message || "Unable to evaluate expression");
    }
    inputBox.value = data.display;
    previewBox.textContent = expression;
    await loadHistory();
  } catch (error) {
    inputBox.value = error.message;
    previewBox.textContent = "Error";
  }
}

async function loadHistory() {
  try {
    const response = await fetch("/history");
    const data = await response.json();
    historyList.innerHTML = "";
    if (!data.length) {
      const emptyState = document.createElement("li");
      emptyState.className = "history-item";
      emptyState.innerHTML = "<strong>No calculations yet</strong><span>Your recent work will appear here.</span>";
      historyList.appendChild(emptyState);
      return;
    }

    data.forEach((item) => {
      const row = document.createElement("li");
      row.className = "history-item";
      row.innerHTML = `<strong>${item.expression}</strong><span>${item.result}</span>`;
      row.addEventListener("click", () => {
        inputBox.value = item.expression;
        syncPreview();
      });
      historyList.appendChild(row);
    });
  } catch (error) {
    console.error("Unable to load history", error);
  }
}

async function clearHistory() {
  if (!window.confirm("Clear all history?")) {
    return;
  }
  try {
    await fetch("/clear", { method: "POST" });
    await loadHistory();
  } catch (error) {
    console.error("Unable to clear history", error);
  }
}

function handleMemory(action) {
  if (action === "MC") {
    memoryValue = 0;
    return;
  }
  const current = inputBox.value.trim();
  if (!current) {
    return;
  }
  const numericValue = Number(current);
  if (Number.isNaN(numericValue)) {
    return;
  }
  if (action === "MR") {
    inputBox.value = String(memoryValue);
  } else if (action === "M+") {
    memoryValue += numericValue;
  } else if (action === "M-") {
    memoryValue -= numericValue;
  }
  syncPreview();
}

function toggleAngleMode() {
  angleMode = angleMode === "deg" ? "rad" : "deg";
  angleToggle.textContent = angleMode.toUpperCase();
}

function toggleTheme() {
  const isLight = body.classList.toggle("light-theme");
  localStorage.setItem("theme", isLight ? "light" : "dark");
  themeToggle.textContent = isLight ? "🌙" : "☀️";
}

function applySavedTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "light") {
    body.classList.add("light-theme");
    themeToggle.textContent = "🌙";
  } else {
    body.classList.remove("light-theme");
    themeToggle.textContent = "☀️";
  }
}

function handleButtonClick(event) {
  const button = event.target.closest("button");
  if (!button) {
    return;
  }

  const { action, value } = button.dataset;
  if (action === "insert") {
    appendValue(value);
  } else if (action === "clear") {
    clearInput();
  } else if (action === "backspace") {
    backspace();
  } else if (action === "evaluate") {
    calculate();
  } else if (action === "toggle-sign") {
    toggleSign();
  } else if (action === "percent") {
    applyPercentage();
  } else if (action === "memory") {
    handleMemory(value);
  }
}

document.getElementById("button-grid").addEventListener("click", handleButtonClick);
document.querySelector(".scientific-panel").addEventListener("click", handleButtonClick);

themeToggle.addEventListener("click", toggleTheme);
angleToggle.addEventListener("click", toggleAngleMode);
scientificToggle.addEventListener("click", () => {
  body.classList.toggle("scientific-hidden");
});
clearHistoryButton.addEventListener("click", clearHistory);

inputBox.addEventListener("input", syncPreview);
inputBox.addEventListener("focus", resizeDisplay);

document.addEventListener("keydown", (event) => {
  const allowed = /[0-9.+\-*/()]/;
  if (allowed.test(event.key)) {
    event.preventDefault();
    appendValue(event.key);
  }
  if (event.key === "Enter") {
    event.preventDefault();
    calculate();
  }
  if (event.key === "Backspace") {
    event.preventDefault();
    backspace();
  }
  if (event.key === "Escape") {
    event.preventDefault();
    clearInput();
  }
});

window.addEventListener("DOMContentLoaded", () => {
  applySavedTheme();
  angleToggle.textContent = angleMode.toUpperCase();
  resizeDisplay();
  loadHistory();
  inputBox.focus();
});
