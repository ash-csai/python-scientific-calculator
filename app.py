import os

from flask import Flask, jsonify, render_template, request

from backend.calculator_core import CalculatorError, evaluate_expression
from backend.history_manager import add_history, clear_history, get_all_history, init_db, search_history


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["JSON_SORT_KEYS"] = False

    init_db()

    def json_error(message: str, status_code: int = 400, code: str = "bad_request"):
        payload = {"status": "error", "message": message}
        if code:
            payload["code"] = code
        return jsonify(payload), status_code

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/calculate", methods=["POST"])
    def calculate():
        payload = request.get_json(silent=True) or {}
        expression = (payload.get("expression") or "").strip()
        angle_mode = (payload.get("angle_mode") or "deg").lower()

        if not expression:
            return json_error("Expression is required", 400, "missing_expression")

        if angle_mode not in {"deg", "rad"}:
            return json_error("Angle mode must be either deg or rad", 422, "invalid_angle_mode")

        try:
            result = evaluate_expression(expression, angle_mode=angle_mode)
        except CalculatorError as exc:
            return json_error(str(exc), 422, "invalid_expression")
        except Exception:  # pragma: no cover - defensive fallback
            return json_error("Calculation failed", 500, "internal_error")

        add_history(expression, result)
        return jsonify({"status": "ok", "result": result, "display": str(result)})

    @app.route("/history", methods=["GET"])
    def history():
        rows = get_all_history()
        data = [
            {"id": row[0], "expression": row[1], "result": row[2], "timestamp": row[3], "is_favorite": bool(row[4]) if len(row) > 4 else False}
            for row in rows
        ]
        return jsonify(data)

    @app.route("/search", methods=["POST"])
    def search():
        payload = request.get_json(silent=True) or {}
        keyword = (payload.get("query") or "").strip()
        results = search_history(keyword)
        data = [
            {"id": row[0], "expression": row[1], "result": row[2], "timestamp": row[3], "is_favorite": bool(row[4]) if len(row) > 4 else False}
            for row in results
        ]
        return jsonify(data)

    @app.route("/clear", methods=["POST"])
    def clear():
        clear_history()
        return jsonify({"status": "cleared"})

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
