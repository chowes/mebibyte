import unittest

from ..handler import ExpressionHandler, MalformedExpressionError, InvalidUnitError


class TestExpressionHandler(unittest.TestCase):
    def test_handle(self):
        h = ExpressionHandler()
        result, unit = h.handle("4 kib in bytes")
        self.assertAlmostEqual(result, 4096)
        self.assertEqual(unit, "bytes")

        h = ExpressionHandler()
        result, unit = h.handle("2 mib + 2048 kib in mib")
        self.assertAlmostEqual(result, 4)
        self.assertEqual(unit, "MiB")

        h = ExpressionHandler()
        result, unit = h.handle("2 mib + 2048 kib")
        self.assertAlmostEqual(result, 4)
        self.assertEqual(unit, "MiB")

        h = ExpressionHandler()
        result, unit = h.handle("2 + 3")
        self.assertAlmostEqual(result, 5)
        self.assertEqual(unit, None)

        h = ExpressionHandler()
        result, unit = h.handle("")
        self.assertAlmostEqual(result, 0)
        self.assertEqual(unit, None)

        h = ExpressionHandler()
        self.assertRaises(MalformedExpressionError,
                          h.handle, "2 mib in bytes in mib")

        h = ExpressionHandler()
        self.assertRaises(MalformedExpressionError, h.handle, "2 + 2 in bytes")

        h = ExpressionHandler()
        self.assertRaises(InvalidUnitError, h.handle, "2 mib in foo")
