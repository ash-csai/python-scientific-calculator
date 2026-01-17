# Scientific Calculator (Python + Flask)

## Project Overview
This is a **Scientific Calculator Web Application** built with **Python** (backend), **Flask** (web framework), **HTML/CSS/JavaScript** (frontend), and **SQLite** (history management).  
It supports **basic arithmetic**, **scientific functions** (sin, cos, tan, log, sqrt, factorial, powers), multiple operators in one expression, and maintains a **calculation history**.


## Features
- **Basic Arithmetic:** Addition, Subtraction, Multiplication, Division, Modulus.
- **Scientific Functions:** `sin()`, `cos()`, `tan()`, `log()`, `sqrt()`, `x^y`, `factorial()`.
- **Multiple Operators:** Evaluate complex expressions with proper precedence.
- **History Management:**  
  - View full history of calculations.  
  - Search history by keywords or expressions.  
  - Clear entire history.  
- **Responsive UI:** Google Calculator-inspired clean interface with ripple effects, animations, and intuitive buttons.
- **Error Handling:** Handles division by zero, invalid input, and unknown operators.


## Project Structure
Scientific-Calculator/
│
├── backend/
│ ├── calculator_core.py # Python backend: expression evaluation
│ ├── command_line_interface.py # Python CLI: Integrates Core Calculator + History Manager
│ └── history_manager.py # Python backend: SQLite history functions
│
├── static/
│ ├── style.css # CSS for calculator UI
│ └── scripts/
│ └── calculator.js # JavaScript for frontend interactions
│
├── templates/
│ └── index.html # HTML frontend
│
├── app.py # Flask main application
└── README.md # Project documentation


## Setup Instructions

### Prerequisites
- Python 3.x
- Flask
- SQLite (built-in with Python)
- Web browser (Chrome, Firefox, Edge, etc.)

### Installation
1. **Clone the repository:**
```bash```
git clone <repository-url>
cd Scientific-Calculator

2. **Install dependencies:**
pip install flask

3. **Run the Flask application:**
python app.py

4. **Open the application in your browser:**
http://127.0.0.1:5000/


### Usage
1. Enter expressions using the calculator buttons or keyboard.
2. Press = to evaluate the expression.
3. View previous calculations in the History panel.
4. Search for a past calculation or clear all history using the respective buttons.

**Example Expressions:**
5 + 7 * 2
sin(45)
log(100)
sqrt(144)
5^3
factorial(6)


### Notes
1. Expressions support nested parentheses and follow operator precedence.
2. History is stored in a local SQLite database calculator_history.db.
3. Any invalid operation (like division by zero) will show a clear error message.

### Future Enhancements
1. Add user authentication for multiple users.
2. Export history as CSV or PDF.
3. Implement themes for UI customization.
4. Add graphing features for functions.

### Authors
Palak Malik (ASH) & Charvi Pundir
School Computer Science Project | Backend & Frontend Developer




