import unittest

from ..handler import InputHandler, MalformedExpressionError, InvalidUnitError


class TestInputHandler(unittest.TestCase):
    def test_handle(self):
        h = InputHandler("4 kib in bytes")
        result, unit = h.handle()
        self.assertAlmostEqual(result, 4096)
        self.assertEqual(unit, "bytes")

        h = InputHandler("2 mib + 2048 kib in mib")
        result, unit = h.handle()
        self.assertAlmostEqual(result, 4)
        self.assertEqual(unit, "mib")

        h = InputHandler("2 mib + 2048 kib")
        result, unit = h.handle()
        self.assertAlmostEqual(result, 4)
        self.assertEqual(unit, "mib")

        h = InputHandler("2 + 3")
        result, unit = h.handle()
        self.assertAlmostEqual(result, 5)
        self.assertEqual(unit, None)

        h = InputHandler("")
        result, unit = h.handle()
        self.assertAlmostEqual(result, 0)
        self.assertEqual(unit, None)

        h = InputHandler("2 mib in bytes in mib")
        self.assertRaises(MalformedExpressionError, h.handle)

        h = InputHandler("2 + 2 in bytes")
        self.assertRaises(MalformedExpressionError, h.handle)

        h = InputHandler("2 mib in foo")
        self.assertRaises(InvalidUnitError, h.handle)
