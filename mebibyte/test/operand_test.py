import unittest
from ..operand import Operand


class TestOperator(unittest.TestCase):
    def test_operand(self):
        operand = Operand(1.0)
        self.assertAlmostEqual(operand.value, 1.0)
        self.assertEqual(operand.unit_power, 0)

        operand = Operand(1.0, "mib")
        self.assertAlmostEqual(operand.value, 8388608.0)
        self.assertEqual(operand.unit_power, 1)

        operand = Operand(1.5, "kib")
        self.assertAlmostEqual(operand.value, 12288.0)
        self.assertEqual(operand.unit_power, 1)

    def test_add(self):
        l_operand = Operand(1.0)
        r_operand = Operand(2.0)
        result = l_operand + r_operand
        self.assertAlmostEqual(result.value, 3.0)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(1.5, "mib")
        r_operand = Operand(2.5, "kib")
        result = l_operand + r_operand
        self.assertAlmostEqual(result.value, 12603392.0)
        self.assertEqual(result.unit_power, 1)

        l_operand = Operand(1.0, "mib")
        r_operand = Operand(1.0)
        self.assertRaises(ValueError, lambda: l_operand + r_operand)

        l_operand = Operand(1.0)
        r_operand = "foo"
        self.assertRaises(TypeError, lambda: l_operand + r_operand)

        l_operand = "foo"
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand + r_operand)

        l_operand = Operand(1.0)
        r_operand = None
        self.assertRaises(TypeError, lambda: l_operand + r_operand)

        l_operand = None
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand + r_operand)

    def test_sub(self):
        l_operand = Operand(1.0)
        r_operand = Operand(2.0)
        result = l_operand - r_operand
        self.assertAlmostEqual(result.value, -1.0)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(1.5, "mib")
        r_operand = Operand(2.5, "kib")
        result = l_operand - r_operand
        self.assertAlmostEqual(result.value, 12562432.0)
        self.assertEqual(result.unit_power, 1)

        l_operand = Operand(1.0, "mib")
        r_operand = Operand(1.0)
        self.assertRaises(ValueError, lambda: l_operand - r_operand)

        l_operand = Operand(1.0)
        r_operand = "foo"
        self.assertRaises(TypeError, lambda: l_operand - r_operand)

        l_operand = "foo"
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand - r_operand)

        l_operand = Operand(1.0)
        r_operand = None
        self.assertRaises(TypeError, lambda: l_operand - r_operand)

        l_operand = None
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand - r_operand)

    def test_mul(self):
        l_operand = Operand(1.0)
        r_operand = Operand(2.0)
        result = l_operand * r_operand
        self.assertAlmostEqual(result.value, 2.0)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(1.5, "bytes")
        r_operand = Operand(2.0)
        result = l_operand * r_operand
        self.assertAlmostEqual(result.value, 24.0)
        self.assertEqual(result.unit_power, 1)

        l_operand = Operand(0.5)
        r_operand = Operand(1.5, "mb")
        result = l_operand * r_operand
        self.assertAlmostEqual(result.value, 6000000.0)
        self.assertEqual(result.unit_power, 1)

        l_operand = Operand(1.0, "mib")
        r_operand = Operand(1.0, "kib")
        self.assertRaises(ValueError, lambda: l_operand * r_operand)

        l_operand = Operand(1.0)
        r_operand = "foo"
        self.assertRaises(TypeError, lambda: l_operand * r_operand)

        l_operand = "foo"
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand * r_operand)

        l_operand = Operand(1.0)
        r_operand = None
        self.assertRaises(TypeError, lambda: l_operand * r_operand)

        l_operand = None
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand * r_operand)

    def test_div(self):
        l_operand = Operand(1.0)
        r_operand = Operand(2.0)
        result = l_operand / r_operand
        self.assertAlmostEqual(result.value, 0.5)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(4.0, "bytes")
        r_operand = Operand(2.0)
        result = l_operand / r_operand
        self.assertAlmostEqual(result.value, 16.0)
        self.assertEqual(result.unit_power, 1)

        l_operand = Operand(2, "mb")
        r_operand = Operand(2, "mb")
        result = l_operand / r_operand
        self.assertAlmostEqual(result.value, 1.0)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(1.0, "mib")
        r_operand = Operand(1.0, "kib")
        result = l_operand / r_operand
        self.assertAlmostEqual(result.value, 1024.0)
        self.assertEqual(result.unit_power, 0)

        l_operand = Operand(2.0)
        r_operand = Operand(1.0, "bit")
        self.assertRaises(ValueError, lambda: l_operand / r_operand)

        l_operand = Operand(2.0, "mib")
        r_operand = Operand(0.0, "bit")
        self.assertRaises(ZeroDivisionError, lambda: l_operand / r_operand)

        l_operand = Operand(1.0)
        r_operand = "foo"
        self.assertRaises(TypeError, lambda: l_operand / r_operand)

        l_operand = "foo"
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand / r_operand)

        l_operand = Operand(1.0)
        r_operand = None
        self.assertRaises(TypeError, lambda: l_operand / r_operand)

        l_operand = None
        r_operand = Operand(1.0)
        self.assertRaises(TypeError, lambda: l_operand / r_operand)
