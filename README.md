# Scientific Calculator (Python + Flask)

## Overview
This project is a production-ready scientific calculator web app built with Python, Flask, SQLite, HTML, CSS, and JavaScript. It supports arithmetic, scientific functions, keyboard input, and calculation history with a polished iOS-inspired interface.

## Features
- Basic arithmetic: addition, subtraction, multiplication, division, modulo, and percentage
- Scientific operations: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, log, ln, exp, sqrt, cbrt, factorial, absolute value, powers, and constants such as pi and e
- Responsive UI with scientific controls and a dark/light theme
- History tracking with click-to-reuse support and clear-history actions
- Safe evaluation through Python AST parsing, avoiding raw eval usage
- Structured JSON error handling for API requests

## Project structure
```text
Scientific Calculator_Python/
├── app.py
├── wsgi.py
├── requirements.txt
├── Procfile
├── README.md
├── calculator_history.db
├── backend/
│   ├── __init__.py
│   ├── calculator_core.py
│   ├── calculator_history.db
│   ├── command_line_interface.py
│   ├── history_manager.py
│   └── __pycache__/
├── static/
│   ├── scripts/
│   │   └── calculator.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_calculator_core.py
└── __pycache__/
```

## Local development
### 1. Prerequisites
- Python 3.10+
- pip
- A browser

### 2. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run the app locally
```bash
python app.py
```

Then open:
```text
http://127.0.0.1:5000/
```

## Production deployment
### Gunicorn
The app is ready to run behind Gunicorn:
```bash
gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

### Platform examples
- Render: set the start command to `gunicorn --bind 0.0.0.0:$PORT wsgi:app`
- Heroku: the included Procfile will start the app automatically
- Any container-based platform: expose port `5000` or use the `PORT` environment variable

## API endpoints
- `GET /health` returns service health
- `POST /calculate` evaluates an expression and stores it in history
- `GET /history` returns past calculations
- `POST /clear` clears history

## Notes
- History is stored in a SQLite file at the project root.
- Invalid input returns structured API errors instead of crashing the UI.
- The calculator supports both degree and radian mode for trig functions.
- Runtime SQLite database files such as `calculator_history.db` are ignored by git.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author
ASH | Problem Solver


