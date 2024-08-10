from .constants import *


class Units:
    unit_vals = {
        "bit": BIT,
        "byte": BYTE,
        "b": BYTE,
        "kibibit": KIBIBIT,
        "mebibit": MEBIBIT,
        "gibibit": GIBIBIT,
        "tebibit": TEBIBIT,
        "pebibit": PEBIBIT,
        "exbibit": EXBIBIT,
        "kibibyte": KIBIBYTE,
        "kib": KIBIBYTE,
        "mebibyte": MEBIBYTE,
        "mib": MEBIBYTE,
        "gibibyte": GIBIBYTE,
        "gib": GIBIBYTE,
        "tibibyte": TEBIBYTE,
        "tib": TEBIBYTE,
        "pebibyte": PEBIBYTE,
        "pib": PEBIBYTE,
        "exbibyte": EXBIBYTE,
        "eib": EXBIBYTE,
        "kilobit": KILOBIT,
        "megabit": MEGABIT,
        "gigabit": GIGABIT,
        "terabit": TERABIT,
        "petabit": PETABIT,
        "exabit": EXABIT,
        "kilobyte": KILOBYTE,
        "kb": KILOBYTE,
        "megabyte": MEGABYTE,
        "mb": MEGABYTE,
        "gigabyte": GIGABYTE,
        "gb": GIGABYTE,
        "terabyte": TERABYTE,
        "tb": TERABYTE,
        "petabyte": PETABYTE,
        "pb": PETABYTE,
        "exabyte": EXABYTE,
        "eb": EXABYTE,
    }

    @staticmethod
    def bit_val(unit: str) -> int:
        if unit not in Units.unit_vals:
            raise ValueError(f"Invalid unit type: '{unit}'")
        return Units.unit_vals[unit]

    @staticmethod
    def is_unit(unit: str) -> int:
        return unit in Units.unit_vals
