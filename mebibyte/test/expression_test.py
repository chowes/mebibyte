import unittest
from ..expression import Expression
from ..operator import Add, Multiply, Divide


class TestExpression(unittest.TestCase):
    def test_tokenize(self):
        test_cases = [
            {"expression": "4 mib * 2 kib",
                "want": [33554432.0, Multiply(), 16384.0]},
            {"expression": "4 + 2", "want": [4, Add(), 2]},
            {"expression": "4 mib * 8", "want": [33554432.0, Divide(), 8]},
            {"expression": "4 mib", "want": [33554432.0]},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            e.tokenize()
            self.assertListEqual(e.tokens, tc["want"])

    def test_tokenize_error(self):
        test_cases = [
            {"expression": "mib 4 * 2 kib"},
            {"expression": "4 mib mib * 2 kib"},
            {"expression": "4 mib * foo kib"},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            self.assertRaises(ValueError, e.tokenize)
