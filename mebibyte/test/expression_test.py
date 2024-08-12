import unittest
from ..expression import Expression
from ..operator import LeftParen, RightParen, Add, Multiply, Divide, Subtract, Operator
from ..operand import Operand


class TestExpression(unittest.TestCase):
    def assertOperandsEqual(self, op1, op2):
        msg = f"Operands {op1} and {op2} differ."
        if op1.value != op2.value:
            self.fail(msg)
        if op1.unit_power != op2.unit_power:
            self.fail(msg)

    def assertOperatorsEqual(self, op1, op2):
        if type(op1) != type(op2):
            self.fail(f"Operators {op1} and {op2} have different types.")

    def assertTokenListEqual(self, tokens1: list, tokens2: list):
        if len(tokens1) != len(tokens2):
            self.fail(f"{tokens1} and {tokens2} have different lengths.")

        for t1, t2 in zip(tokens1, tokens2):
            if type(t1) != type(t2):
                self.fail(f"Tokens {t1} and {t2} have different types.")
            if isinstance(t1, Operand):
                self.assertOperandsEqual(t1, t2)
            elif isinstance(t1, Operator):
                self.assertOperatorsEqual(t1, t2)
            else:
                self.fail(f"Tokens {t1} and {t2} have invalid types.")

    def test_tokenize(self):
        e = Expression("4 mib * 2")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [Operand(4.0, "mib"), Multiply(), Operand(2.0)])

        e = Expression("4 + 2")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [Operand(4.0), Add(), Operand(2.0)])

        e = Expression("(4 + 2)")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [LeftParen(), Operand(4.0), Add(), Operand(2.0), RightParen()])

        e = Expression("4 mib / 8 mib")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [Operand(4.0, "mib"), Divide(), Operand(8.0, "mib")])

        e = Expression("4 mib")
        e.tokenize()
        self.assertTokenListEqual(e.tokens, [Operand(4.0, "mib")])

        e = Expression("2^30 bytes")
        e.tokenize()
        self.assertTokenListEqual(e.tokens, [Operand(1, "gib")])

        e = Expression("4 mib * 2 / 8 + 16")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [Operand(4.0, "mib"), Multiply(), Operand(2.0), Divide(), Operand(8.0), Add(), Operand(16.0)])

        e = Expression(
            "4 mib + 3 * 2.5 gb / 1.5 mib - 1 + 8 kib * 1 + 3 / 2 b - 16 / 4 + 2 * 3 eb")
        e.tokenize()
        self.assertTokenListEqual(
            e.tokens, [
                Operand(4.0, "mib"),
                Add(),
                Operand(3.0),
                Multiply(),
                Operand(2.5, "gb"),
                Divide(),
                Operand(1.5, "mib"),
                Subtract(),
                Operand(1.0),
                Add(),
                Operand(8.0, "kib"),
                Multiply(),
                Operand(1.0),
                Add(),
                Operand(3.0),
                Divide(),
                Operand(2.0, "b"),
                Subtract(),
                Operand(16.0),
                Divide(),
                Operand(4.0),
                Add(),
                Operand(2.0),
                Multiply(),
                Operand(3.0, "eb")
            ]
        )

        e = Expression("")
        e.tokenize()
        self.assertTokenListEqual(e.tokens, [])

        e = Expression(" ")
        e.tokenize()
        self.assertTokenListEqual(e.tokens, [])

    def test_tokenize_error(self):
        e = Expression("mib 4 * 2")
        self.assertRaises(ValueError, e.tokenize)

        e = Expression("4 mib mib * 2")
        self.assertRaises(ValueError, e.tokenize)

        e = Expression("4 mib * foo kib")
        self.assertRaises(ValueError, e.tokenize)

        e = Expression("2^^30 bytes")
        self.assertRaises(ValueError, e.tokenize)

    def test_postfix(self):
        e = Expression("4 mib")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens, [Operand(4, "mib")])

        e = Expression("")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens, [])

        e = Expression("4 mib * 2 kib")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens,
                                  [Operand(4, "mib"), Operand(2, "kib"), Multiply()])

        e = Expression("4 + 2 * 8 + 4")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens,
                                  [Operand(4),
                                   Operand(2),
                                   Operand(8),
                                   Multiply(),
                                   Add(),
                                   Operand(4),
                                   Add()])

        e = Expression("4 - 2 + 1 * 9 / 9 + 4 - 2")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens,
                                  [Operand(4),
                                   Operand(2),
                                   Subtract(),
                                   Operand(1),
                                   Operand(9),
                                   Multiply(),
                                   Operand(9),
                                   Divide(),
                                   Add(),
                                   Operand(4),
                                   Add(),
                                   Operand(2),
                                   Subtract()])

        e = Expression("(2^30 bytes + 4 gib) / (2 * 2 gib)")
        e.postfix()
        self.assertTokenListEqual(e.postfix_tokens, [
            Operand(1, "gib"),
            Operand(4, "gib"),
            Add(),
            Operand(2),
            Operand(2, "gib"),
            Multiply(),
            Divide()])

        e = Expression("foo")
        self.assertRaises(ValueError, e.postfix)

        e = Expression(")(")
        self.assertRaises(ValueError, e.postfix)

        e = Expression("(()")
        self.assertRaises(ValueError, e.postfix)

        e = Expression("(1 + (2)")
        self.assertRaises(ValueError, e.postfix)

        e = Expression("(1 + (2))(")
        self.assertRaises(ValueError, e.postfix)

    def test_evaluate(self):
        e = Expression("4 mib * 2")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(8, unit="mib"))

        e = Expression("4 mib / 2 mib")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(2))

        e = Expression("4 + 2 * 8 + 4 / 2 / 2")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(21))

        e = Expression("4 - 2 + 1 * 9 / 9 + 4 - 2")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(5))

        e = Expression("")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(0))

        e = Expression("4")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(4))

        e = Expression("4 mib")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(4, "mib"))

        e = Expression("0 mib / 1 mib")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(0))

        e = Expression("0 mib * 1")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(0, "mib"))

        e = Expression("0 mib / 1")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(0, "mib"))

        e = Expression("(2^30 bytes + 4 gib) / (2 * 2 gib)")
        result = e.evaluate()
        self.assertOperandsEqual(result, Operand(1.25))

        e = Expression("4 foo")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("4 / 1 mib")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("4 + 1 mib")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("4 mib - 1")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("4 mib * 1 mib")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("4 / 0")
        self.assertRaises(ValueError, e.evaluate)

        e = Expression("0 / 0")
        self.assertRaises(ValueError, e.evaluate)
