// ----------------------------
// DOM Elements
// ----------------------------
const inputBox = document.getElementById("calculator-display");
const historyBox = document.getElementById("historyList");
const body = document.body; // for theme toggle

// ----------------------------
// Core Functions
// ----------------------------

// Insert value into the input box
function insertValue(v) {
    inputBox.value += v;
}

// Clear the input box
function clearInput() {
    inputBox.value = "";
}

// Remove the last character from input (disabled on error)
function backspace() {
    if (inputBox.value.startsWith("ERROR:")) return;
    inputBox.value = inputBox.value.slice(0, -1);
}

// Send expression to Flask backend and calculate result
async function calculate() {
    if (!inputBox.value) return;

    try {
        const response = await fetch("/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ expression: inputBox.value }),
        });

        const data = await response.json();
        inputBox.value = data.result;

        loadHistory();
        createRippleEffect(inputBox);

    } catch (err) {
        console.error("Error calculating:", err);
        inputBox.value = "ERROR: Could not calculate";
    }
}

// ----------------------------
// History Functions
// ----------------------------
function loadHistory() {
    fetch("/history")
    .then(res => res.json())
    .then(data => {
        historyBox.innerHTML = "";

        data.forEach(item => {
            const div = document.createElement("div");
            div.classList.add("history-item");
            div.innerHTML = `<span>${item.expression} = ${item.result}</span>`;
            
            // Click history item to load it into input box
            div.addEventListener("click", () => {
                inputBox.value = item.expression;
            });

            historyBox.appendChild(div);
        });
    })
    .catch(err => console.error("Error loading history:", err));
}

function clearHistory() {
    if (!confirm("Are you sure? This will delete all history.")) return;

    fetch("/clear", { method: "POST" })
    .then(() => loadHistory())
    .catch(err => console.error("Error clearing history:", err));
}

// ----------------------------
// Premium JS Enhancements
// ----------------------------

// Ripple Effect
function createRippleEffect(element, event) {
    const ripple = document.createElement("span");
    ripple.className = "ripple-effect";
    element.appendChild(ripple);

    const x = event ? event.offsetX : element.offsetWidth / 2;
    const y = event ? event.offsetY : element.offsetHeight / 2;

    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    setTimeout(() => ripple.remove(), 600);
}

// Attach ripple effect to all buttons
document.querySelectorAll(".btn.ripple").forEach(button => {
    button.addEventListener("click", (e) => createRippleEffect(button, e));
});

// ----------------------------
// Phase 2 Enhancements
// ----------------------------

// 1. Keyboard Support
document.addEventListener("keydown", (e) => {
    const allowedKeys = "0123456789+-*/().";
    const funcKeys = {
        "Enter": calculate,
        "Backspace": backspace,
        "Delete": clearInput,
    };

    if (allowedKeys.includes(e.key)) insertValue(e.key);
    if (funcKeys[e.key]) funcKeys[e.key]();
});

// 2. Auto-focus Input Box on page load
window.onload = () => {
    inputBox.focus();
    loadHistory();
    applySavedTheme();
};

// 3. Dark/Light Theme Toggle
function toggleTheme() {
    body.classList.toggle("dark-theme");

    // Save preference in localStorage
    if (body.classList.contains("dark-theme")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

function applySavedTheme() {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") body.classList.add("dark-theme");
    else body.classList.remove("dark-theme");
}

// ----------------------------
// Dark / Light Theme Toggle
// ----------------------------
const themeToggleBtn = document.getElementById("theme-toggle");

themeToggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    
    // Change icon based on theme
    if (document.body.classList.contains("dark-theme")) {
        themeToggleBtn.textContent = "☀️";
    } else {
        themeToggleBtn.textContent = "🌙";
    }
});
