import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.calculator_core import evaluate_expression
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


if __name__ == "__main__":
    unittest.main()
