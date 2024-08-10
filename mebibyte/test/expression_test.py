import unittest
from ..expression import Expression


class TestExpression(unittest.TestCase):
    def test_tokenize(self):
        test_cases = [
            {"expression": "4 mib * 2 kib",
                "want": ["33554432.0", "*", "16384.0"]},
            {"expression": "4 + 2", "want": ["4", "+", "2"]},
            {"expression": "4 mib * 8", "want": ["33554432.0", "*", "8"]},
            {"expression": "4 mib", "want": ["33554432.0"]},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            tokens = e.tokenize()
            self.assertListEqual(tokens, tc["want"])

    def test_tokenize_error(self):
        test_cases = [
            {"expression": "mib 4 * 2 kib"},
            {"expression": "4 mib mib * 2 kib"},
            {"expression": "4 mib * foo kib"},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            self.assertRaises(ValueError, e.tokenize)
