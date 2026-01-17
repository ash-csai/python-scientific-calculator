# calculator_core.py

import math

# --------------------------
# Supported functions
# --------------------------
functions = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": lambda x: math.log(x),
    "sqrt": lambda x: math.sqrt(x),
    "factorial": lambda x: math.factorial(int(x)) if x >= 0 and x == int(x) else float('nan')
}

# --------------------------
# Operator precedence
# --------------------------
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3
}

# --------------------------
# Check if token is a number
# --------------------------
def is_number(token):
    try:
        float(token)
        return True
    except:
        return False

# --------------------------
# Convert infix to postfix (Shunting Yard)
# --------------------------
def infix_to_postfix(expr):
    expr = expr.replace(" ", "")
    tokens = []
    number = ""
    func = ""

    i = 0
    while i < len(expr):
        char = expr[i]

        # Build numbers
        if char.isdigit() or char == '.':
            number += char

        # Build function names
        elif char.isalpha():
            func += char

        else:
            if number:
                tokens.append(number)
                number = ""

            if func:
                tokens.append(func)
                func = ""

            # Handle unary minus
            if char == '-' and (i == 0 or expr[i-1] in "+-*/^("):
                number = '-'
            else:
                tokens.append(char)
        i += 1

    if number:
        tokens.append(number)
    if func:
        tokens.append(func)

    # Shunting Yard
    output = []
    stack = []

    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token in functions:
            stack.append(token)
        elif token in precedence:
            while (stack and stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()  # Remove '('
            if stack and stack[-1] in functions:
                output.append(stack.pop())
        else:
            raise ValueError(f"Unknown token: {token}")

    while stack:
        if stack[-1] in '()':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    return output

# --------------------------
# Evaluate postfix expression
# --------------------------
def eval_postfix(postfix):
    stack = []

    for token in postfix:
        if is_number(token):
            stack.append(float(token))
        elif token in functions:
            x = stack.pop()
            try:
                stack.append(functions[token](x))
            except Exception:
                return "ERROR: Invalid input"
        else:
            if len(stack) < 2:
                return "ERROR: Invalid expression"
            b = stack.pop()
            a = stack.pop()
            try:
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/':
                    if b == 0: return "ERROR: Division by zero"
                    stack.append(a / b)
                elif token == '%':
                    stack.append(a % b)
                elif token == '^': stack.append(a ** b)
                else: return f"ERROR: Unknown operator {token}"
            except Exception:
                return "ERROR: Invalid operation"

    if len(stack) != 1:
        return "ERROR: Invalid expression"

    return stack[0]

# --------------------------
# Evaluate expression
# --------------------------
def evaluate_expression(expr):
    try:
        postfix = infix_to_postfix(expr)
        return eval_postfix(postfix)
    except Exception as e:
        return f"ERROR: {str(e)}"
