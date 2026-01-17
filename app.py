from flask import Flask, render_template, request, jsonify
from backend.calculator_core import evaluate_expression
from backend.history_manager import (
    init_db, add_history, get_all_history, search_history, clear_history
)

app = Flask(__name__)

# Initialize database on startup
init_db()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expr = data.get("expression", "")

    try:
        result = evaluate_expression(expr)
        add_history(expr, result)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"ERROR: {str(e)}"})

@app.route("/history", methods=["GET"])
def history():
    rows = get_all_history()
    json_history = [
        {"id": r[0], "expression": r[1], "result": r[2], "timestamp": r[3]}
        for r in rows
    ]
    return jsonify(json_history)

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keyword = data.get("query", "")
    results = search_history(keyword)
    json_results = [
        {"id": r[0], "expression": r[1], "result": r[2], "timestamp": r[3]}
        for r in results
    ]
    return jsonify(json_results)

@app.route("/clear", methods=["POST"])
def clear():
    clear_history()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
