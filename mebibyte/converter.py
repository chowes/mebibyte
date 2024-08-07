from .constants import *


class Converter:
    from_bit_val: int
    to_bit_val: int

    def __init__(self, from_bit_val: int, to_bit_val: int) -> None:
        self.from_bit_val = from_bit_val
        self.to_bit_val = to_bit_val

    def convert(self, value: float) -> float:
        bit_val: float = value * self.from_bit_val
        return bit_val / self.to_bit_val


class ConverterFactory:
    def _bit_val(self, unit: str) -> int:
        unit = unit.lower()

        match unit:
            case "bit":
                return BIT
            case "byte" | "b":
                return BYTE
            case "kibibit":
                return KIBIBIT
            case "mebibit":
                return MEBIBIT
            case "gibibit":
                return GIBIBIT
            case "tebibit":
                return TEBIBIT
            case "pebibit":
                return PEBIBIT
            case "exbibit":
                return EXBIBIT
            case "kibibyte" | "kib":
                return KIBIBYTE
            case "mebibyte" | "mib":
                return MEBIBYTE
            case "gibibyte" | "gib":
                return GIBIBYTE
            case "tibibyte" | "tib":
                return TEBIBYTE
            case "pebibyte" | "pib":
                return PEBIBYTE
            case "exbibyte" | "eib":
                return EXBIBYTE
            case "kilobit":
                return KILOBIT
            case "megabit":
                return MEGABIT
            case "gigabit":
                return GIGABIT
            case "terabit":
                return TERABIT
            case "petabit":
                return PETABIT
            case "exabit":
                return EXABIT
            case "kilobyte" | "kb":
                return KILOBYTE
            case "megabyte" | "mb":
                return MEGABYTE
            case "gigabyte" | "gb":
                return GIGABYTE
            case "terabyte" | "tb":
                return TERABYTE
            case "petabyte" | "pb":
                return PETABYTE
            case "exabyte" | "eb":
                return EXABYTE
            case _:
                raise ValueError(f"Invalid unit type: '{unit}'")

    def get_converter(self, from_unit: str, to_unit: str) -> Converter:
        from_bit_val: int = self._bit_val(from_unit)
        to_bit_val: int = self._bit_val(to_unit)

        return Converter(from_bit_val, to_bit_val)
