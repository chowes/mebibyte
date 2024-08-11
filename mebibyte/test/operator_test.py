import unittest
from ..operator import OperatorFactory, Add, Subtract, Multiply, Divide


class TestOperator(unittest.TestCase):
    def test_precedence(self):
        add = Add()
        sub = Subtract()
        mult = Multiply()
        div = Divide()

        self.assertEquals(add, sub)
        self.assertEquals(mult, div)
        self.assertLess(add, mult)
        self.assertLess(sub, div)


class TestOperatorFactory(unittest.TestCase):
    def test_is_operator(self):
        test_cases = [
            {"input": "+", "want": True},
            {"input": "-", "want": True},
            {"input": "*", "want": True},
            {"input": "/", "want": True},
            {"input": "foo", "want": False},
            {"input": "", "want": False},
            {"input": None, "want": False},
        ]

        for tc in test_cases:
            self.assertEqual(
                OperatorFactory.is_operator(tc["input"]), tc["want"])

    def test_new_operator(self):
        test_cases = [
            {"input": "+", "want": Add()},
            {"input": "-", "want": Subtract()},
            {"input": "*", "want": Multiply()},
            {"input": "/", "want": Divide()},
        ]

        for tc in test_cases:
            op = OperatorFactory.new_operator(tc["input"])
            self.assertEqual(type(op), type(tc["want"]))

    def test_new_operator_error(self):
        test_cases = [
            {"input": ""},
            {"input": "foo"},
            {"input": None},
        ]

        for tc in test_cases:
            self.assertRaises(
                ValueError, OperatorFactory.new_operator, tc["input"])


class TestAdd(unittest.TestCase):
    def test_compute(self):
        op = OperatorFactory.new_operator("+")
        self.assertAlmostEqual(op.compute(0, 0), 0)
        self.assertAlmostEqual(op.compute(1, 2), 3)
        self.assertAlmostEqual(op.compute(1.5, 2.1), 3.6)
        self.assertAlmostEqual(op.compute(2.5, -1.0), 1.5)
        self.assertAlmostEqual(op.compute(-2.0, -1.5), -3.5)


class TestSubtract(unittest.TestCase):
    def test_compute(self):
        op = OperatorFactory.new_operator("-")
        self.assertAlmostEqual(op.compute(0, 0), 0)
        self.assertAlmostEqual(op.compute(1, 2), -1)
        self.assertAlmostEqual(op.compute(1.5, 2.1), -0.6)
        self.assertAlmostEqual(op.compute(2.5, -1.0), 3.5)
        self.assertAlmostEqual(op.compute(-2.0, -3.5), 1.5)


class TestMultiply(unittest.TestCase):
    def test_compute(self):
        op = OperatorFactory.new_operator("*")
        self.assertAlmostEqual(op.compute(1.5, 0), 0)
        self.assertAlmostEqual(op.compute(1, 2), 2)
        self.assertAlmostEqual(op.compute(1.5, 2.1), 3.15)
        self.assertAlmostEqual(op.compute(2.5, -1.0), -2.5)
        self.assertAlmostEqual(op.compute(-2.0, -1.5), 3.0)


class TestDivide(unittest.TestCase):
    def test_compute(self):
        op = OperatorFactory.new_operator("/")
        self.assertAlmostEqual(op.compute(1, 2), 0.5)
        self.assertAlmostEqual(op.compute(1.5, 0.5), 3.0)
        self.assertAlmostEqual(op.compute(0, 1.0), 0)
        self.assertAlmostEqual(op.compute(2.0, -1.0), -2.0)
        self.assertRaises(ZeroDivisionError, op.compute, 1.0, 0.0)
