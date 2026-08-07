import ast
import math
import re


class CalculatorError(ValueError):
    """Raised when an expression is invalid or unsupported."""


def _normalize_expression(expression: str) -> str:
    if expression is None:
        raise CalculatorError("Expression is empty")

    expr = str(expression).strip()
    if not expr:
        raise CalculatorError("Expression is empty")

    expr = expr.replace("π", "pi").replace("×", "*").replace("÷", "/")
    expr = expr.replace("−", "-").replace("^", "**")
    expr = expr.replace("²", "**2").replace("³", "**3")
    expr = expr.replace("√", "sqrt(")
    expr = re.sub(r"([0-9.]+)!", r"factorial(\1)", expr)
    return expr


def _round_result(value: float) -> float | int:
    if isinstance(value, bool):
        return value
    if abs(value) < 1e-12:
        return 0.0
    rounded = round(float(value), 12)
    if rounded.is_integer():
        return int(rounded)
    return rounded


def _apply_angle_mode(value: float, angle_mode: str) -> float:
    if angle_mode == "rad":
        return value
    return math.radians(value)


def _evaluate_node(node: ast.AST, angle_mode: str) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body, angle_mode)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)

    if isinstance(node, ast.Name):
        if node.id == "pi":
            return math.pi
        if node.id == "e":
            return math.e
        raise CalculatorError(f"Unknown constant: {node.id}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand, angle_mode)
        if isinstance(node.op, ast.UAdd):
            return operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise CalculatorError("Unsupported unary operator")

    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left, angle_mode)
        right = _evaluate_node(node.right, angle_mode)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise CalculatorError("Division by zero")
            return left / right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right
        raise CalculatorError("Unsupported operator")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise CalculatorError("Unsupported function call")

        func_name = node.func.id
        if len(node.args) != 1:
            raise CalculatorError(f"{func_name} expects exactly one argument")
        value = _evaluate_node(node.args[0], angle_mode)

        if func_name in {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh"}:
            if func_name == "sin":
                return math.sin(_apply_angle_mode(value, angle_mode))
            if func_name == "cos":
                return math.cos(_apply_angle_mode(value, angle_mode))
            if func_name == "tan":
                return math.tan(_apply_angle_mode(value, angle_mode))
            if func_name == "asin":
                return math.asin(value)
            if func_name == "acos":
                return math.acos(value)
            if func_name == "atan":
                return math.atan(value)
            if func_name == "sinh":
                return math.sinh(value)
            if func_name == "cosh":
                return math.cosh(value)
            if func_name == "tanh":
                return math.tanh(value)

        if func_name == "log":
            if value <= 0:
                raise CalculatorError("Logarithm requires a positive value")
            return math.log10(value)
        if func_name == "ln":
            if value <= 0:
                raise CalculatorError("Natural logarithm requires a positive value")
            return math.log(value)
        if func_name == "exp":
            return math.exp(value)
        if func_name == "sqrt":
            if value < 0:
                raise CalculatorError("Square root of a negative number is undefined")
            return math.sqrt(value)
        if func_name == "cbrt":
            if value < 0:
                return -abs(value) ** (1 / 3)
            return value ** (1 / 3)
        if func_name == "abs":
            return abs(value)
        if func_name == "factorial":
            if value < 0 or not float(value).is_integer():
                raise CalculatorError("Factorial requires a non-negative integer")
            return float(math.factorial(int(value)))
        raise CalculatorError(f"Unsupported function: {func_name}")

    raise CalculatorError("Unsupported expression")


def evaluate_expression(expression: str, angle_mode: str = "deg") -> float | int:
    """Safely evaluate an expression using Python's AST parser."""
    normalized = _normalize_expression(expression)
    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError("Invalid syntax") from exc

    try:
        result = _evaluate_node(tree, angle_mode)
        return _round_result(result)
    except ZeroDivisionError as exc:
        raise CalculatorError("Division by zero") from exc
    except CalculatorError:
        raise
    except Exception as exc:
        raise CalculatorError("Unable to evaluate that expression") from exc
