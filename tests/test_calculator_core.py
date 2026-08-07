import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.calculator_core import CalculatorError, evaluate_expression
from backend.history_manager import init_db, add_history, get_all_history, clear_history


class CalculatorCoreTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(evaluate_expression("2 + 2"), 4)
        self.assertEqual(evaluate_expression("10 / 2"), 5)
        self.assertEqual(evaluate_expression("3 % 2"), 1)

    def test_scientific_functions(self):
        self.assertAlmostEqual(evaluate_expression("sin(0)"), 0.0, places=10)
        self.assertAlmostEqual(evaluate_expression("sqrt(4)"), 2.0, places=10)
        self.assertEqual(evaluate_expression("2^3"), 8)

    def test_constant_and_inverse(self):
        self.assertAlmostEqual(evaluate_expression("pi"), 3.141592653589793, places=12)
        self.assertAlmostEqual(evaluate_expression("1/2"), 0.5, places=12)

    def test_history_manager(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "history.db")
            init_db(db_path=db_path)
            add_history("1+1", 2, db_path=db_path)
            rows = get_all_history(db_path=db_path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][1], "1+1")
            clear_history(db_path=db_path)
            self.assertEqual(len(get_all_history(db_path=db_path)), 0)


class CalculatorCoreErrorPathTests(unittest.TestCase):
    def test_domain_errors_raise_calculator_error(self):
        for expr in ["sqrt(-1)", "ln(-1)", "log(-1)", "log(0)"]:
            with self.subTest(expr=expr):
                with self.assertRaises(CalculatorError):
                    evaluate_expression(expr)

    def test_negative_cbrt_returns_real_value(self):
        self.assertEqual(evaluate_expression("cbrt(-1)"), -1)

    def test_division_by_zero_raises_calculator_error(self):
        with self.assertRaises(CalculatorError):
            evaluate_expression("1/0")

    def test_malformed_syntax_raises_calculator_error(self):
        for expr in ["2 + * 3", "sin(", "2 + (3"]:
            with self.subTest(expr=expr):
                with self.assertRaises(CalculatorError):
                    evaluate_expression(expr)


if __name__ == "__main__":
    unittest.main()
