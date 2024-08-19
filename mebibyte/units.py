from .constants import *


class Units:
    unit_vals = {
        "bit": BIT,
        "bits": BIT,
        "byte": BYTE,
        "bytes": BYTE,
        "b": BYTE,
        "kibibit": KIBIBIT,
        "kibibits": KIBIBIT,
        "mebibit": MEBIBIT,
        "mebibits": MEBIBIT,
        "gibibit": GIBIBIT,
        "gibibits": GIBIBIT,
        "tebibit": TEBIBIT,
        "tebibits": TEBIBIT,
        "pebibit": PEBIBIT,
        "pebibits": PEBIBIT,
        "exbibit": EXBIBIT,
        "exbibits": EXBIBIT,
        "kibibyte": KIBIBYTE,
        "kibibytes": KIBIBYTE,
        "kib": KIBIBYTE,
        "mebibyte": MEBIBYTE,
        "mebibytes": MEBIBYTE,
        "mib": MEBIBYTE,
        "gibibyte": GIBIBYTE,
        "gibibytes": GIBIBYTE,
        "gib": GIBIBYTE,
        "tibibyte": TEBIBYTE,
        "tibibytes": TEBIBYTE,
        "tib": TEBIBYTE,
        "pebibyte": PEBIBYTE,
        "pebibytes": PEBIBYTE,
        "pib": PEBIBYTE,
        "exbibyte": EXBIBYTE,
        "exbibytes": EXBIBYTE,
        "eib": EXBIBYTE,
        "kilobit": KILOBIT,
        "kilobits": KILOBIT,
        "megabit": MEGABIT,
        "megabits": MEGABIT,
        "gigabit": GIGABIT,
        "gigabits": GIGABIT,
        "terabit": TERABIT,
        "terabits": TERABIT,
        "petabit": PETABIT,
        "petabits": PETABIT,
        "exabit": EXABIT,
        "exabits": EXABIT,
        "kilobyte": KILOBYTE,
        "kilobytes": KILOBYTE,
        "kb": KILOBYTE,
        "megabyte": MEGABYTE,
        "megabytes": MEGABYTE,
        "mb": MEGABYTE,
        "gigabyte": GIGABYTE,
        "gigabytes": GIGABYTE,
        "gb": GIGABYTE,
        "terabyte": TERABYTE,
        "terabytes": TERABYTE,
        "tb": TERABYTE,
        "petabyte": PETABYTE,
        "petabytes": PETABYTE,
        "pb": PETABYTE,
        "exabyte": EXABYTE,
        "exabytes": EXABYTE,
        "eb": EXABYTE,
    }

    @staticmethod
    def bit_val(unit: str) -> int:
        if not Units.is_unit(unit):
            raise ValueError(f"Invalid unit: '{unit}'")
        return Units.unit_vals[unit]

    @staticmethod
    def is_unit(unit: str) -> int:
        return unit in Units.unit_vals

    @staticmethod
    def prettify(unit: str) -> str:
        if not Units.is_unit(unit):
            raise ValueError(f"Invalid unit: '{unit}'")

        if unit == "b" or unit == "bit":
            return unit
        if len(unit) > 3:
            return unit

        result = unit[0].upper() + unit[1:]
        result = result[0:-1] + result[-1].upper()

        return result
