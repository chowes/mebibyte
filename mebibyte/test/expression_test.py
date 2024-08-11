import unittest
from ..expression import Expression
from ..operator import Add, Multiply, Divide, Subtract


class TestExpression(unittest.TestCase):
    def test_tokenize(self):
        test_cases = [
            {"expression": "4 mib * 2 kib",
                "want": [33554432.0, Divide(), 16384.0]},
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

    def test_postfix(self):
        test_cases = [
            {"expression": "4 mib * 2 kib",
                "want": [33554432.0, 16384.0, Multiply()]},
            {"expression": "4 + 2 * 8 + 4",
                "want": [4.0, 2.0, 8.0, Multiply(), Add(), 4.0, Add()]},
            {"expression": "4 - 2 + 1 * 9 / 9 + 4 - 2",
                "want": [4.0, 2.0, Subtract(), 1.0, 9.0, Multiply(), 9.0, Divide(), Add(), 4.0, Add(), 2.0, Subtract()]},
            {"expression": "",
                "want": []},
            {"expression": "4",
                "want": [4.0]},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            e.postfix()
            self.assertEqual(len(e.postfix_tokens), len(tc["want"]))
            for got, want in zip(e.postfix_tokens, tc["want"]):
                self.assertEqual(type(got), type(
                    want), f'got: {e.postfix_tokens}, want: {tc["want"]}')
                self.assertEqual(
                    got, want, f'got: {e.postfix_tokens}, want: {tc["want"]}')

    def test_postfix_error(self):
        test_cases = [
            {"expression": "foo"},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            self.assertRaises(ValueError, e.postfix)

    def test_evaluate(self):
        test_cases = [
            {"expression": "4 mib * 2 kib", "want": 549755813888.0},
            {"expression": "4 + 2 * 8 + 4", "want": 24.0},
            {"expression": "4 - 2 + 1 * 9 / 9 + 4 - 2", "want": 5.0},
            {"expression": "", "want": 0.0},
            {"expression": "4", "want": 4.0},
        ]

        for tc in test_cases:
            e = Expression(tc["expression"])
            result = e.evaluate()
            self.assertAlmostEqual(result, tc["want"])
