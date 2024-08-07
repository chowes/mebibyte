import unittest
from ..converter import Converter, ConverterFactory


class TestConverterFactory(unittest.TestCase):
    def test_get_converter(self):
        test_cases = [
            {"from": "bit", "to": "foo"},
            {"from": "foo", "to": "bit"},
        ]

        cf = ConverterFactory()
        for tc in test_cases:
            self.assertRaises(ValueError, cf.get_converter,
                              tc["from"], tc["to"])


class TestConverter(unittest.TestCase):
    def test_convert(self):
        test_cases = [
            {"value": 1, "from": "bit", "to": "byte", "want": 0.125},
            {"value": 1, "from": "byte", "to": "bit", "want": 8.0},
            {"value": 1, "from": "kibibit", "to": "kilobit", "want": 1.024},
            {"value": 1, "from": "kilobit", "to": "kibibit", "want": 0.9765625},
            {"value": 1, "from": "mebibit", "to": "megabit", "want": 1.048576},
            {"value": 1, "from": "megabit", "to": "mebibit", "want": 0.95367431640625},
            {"value": 1, "from": "gibibit", "to": "gigabit", "want": 1.073741824},
            {"value": 1, "from": "gigabit", "to": "gibibit", "want": 0.9313225746154},
            {"value": 1, "from": "tebibit", "to": "terabit", "want": 1.099511627776},
            {"value": 1, "from": "terabit", "to": "tebibit", "want": 0.90949470177292},
            {"value": 1, "from": "pebibit", "to": "petabit", "want": 1.12589990684262},
            {"value": 1, "from": "petabit", "to": "pebibit", "want": 0.88817841970012},
            {"value": 1, "from": "exbibit", "to": "exabit", "want": 1.1529215},
            {"value": 1, "from": "exabit", "to": "exbibit", "want": 0.8673617},
            {"value": 1, "from": "kibibit", "to": "mebibit", "want": 0.0009765625},
            {"value": 1, "from": "mebibit", "to": "kibibit", "want": 1024.0},
            {"value": 1, "from": "mebibit", "to": "gibibit", "want": 0.0009765625},
            {"value": 1, "from": "gibibit", "to": "mebibit", "want": 1024.0},
            {"value": 1, "from": "gibibit", "to": "tebibit", "want": 0.0009765625},
            {"value": 1, "from": "tebibit", "to": "gibibit", "want": 1024.0},
            {"value": 1, "from": "tebibit", "to": "pebibit", "want": 0.0009765625},
            {"value": 1, "from": "pebibit", "to": "tebibit", "want": 1024.0},
            {"value": 1, "from": "pebibit", "to": "exbibit", "want": 0.0009765625},
            {"value": 1, "from": "exbibit", "to": "pebibit", "want": 1024.0},
            {"value": 1, "from": "kib", "to": "kb", "want": 1.024},
            {"value": 1, "from": "kb", "to": "kib", "want": 0.9765625},
            {"value": 1, "from": "mib", "to": "mb", "want": 1.048576},
            {"value": 1, "from": "mb", "to": "mib", "want": 0.95367431640625},
            {"value": 1, "from": "gib", "to": "gb", "want": 1.073741824},
            {"value": 1, "from": "gb", "to": "gib", "want": 0.9313225746154785},
            {"value": 1, "from": "tib", "to": "tb", "want": 1.099511627776},
            {"value": 1, "from": "tb", "to": "tib", "want": 0.90949470},
            {"value": 1, "from": "pib", "to": "pb", "want": 1.125899906},
            {"value": 1, "from": "pb", "to": "pib", "want": 0.888178419},
            {"value": 1, "from": "eib", "to": "eb", "want": 1.152921504},
            {"value": 1, "from": "eb", "to": "eib", "want": 0.867361737},
            {"value": 1, "from": "kib", "to": "mib", "want": 0.0009765625},
            {"value": 1, "from": "mib", "to": "kib", "want": 1024.0},
            {"value": 1, "from": "mib", "to": "gib", "want": 0.0009765625},
            {"value": 1, "from": "gib", "to": "mib", "want": 1024.0},
            {"value": 1, "from": "gib", "to": "tib", "want": 0.0009765625},
            {"value": 1, "from": "tib", "to": "gib", "want": 1024.0},
            {"value": 1, "from": "tib", "to": "pib", "want": 0.0009765625},
            {"value": 1, "from": "pib", "to": "tib", "want": 1024.0},
            {"value": 1, "from": "pib", "to": "eib", "want": 0.0009765625},
            {"value": 1, "from": "eib", "to": "pib", "want": 1024.0},
            {"value": 50, "from": "gigabit", "to": "mib", "want": 5960.46447753},
            {"value": 0.5, "from": "tib", "to": "gib", "want": 512.0},
            {"value": 1.5, "from": "eib", "to": "pib", "want": 1536.0},

        ]

        cf = ConverterFactory()
        for tc in test_cases:
            c = cf.get_converter(tc["from"], tc["to"])
            result = c.convert(tc["value"])
            self.assertAlmostEqual(result, tc["want"],
                                   msg=f"Failed for value: {tc['value']} from: {tc['from']} to: {tc['to']} want: {tc['want']} got: {result}")
