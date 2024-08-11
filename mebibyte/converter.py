from .units import Units


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
    @staticmethod
    def _bit_val(unit: str) -> int:
        unit = unit.lower()
        return Units.bit_val(unit)

    @staticmethod
    def get_converter(from_unit: str, to_unit: str) -> Converter:
        from_bit_val: int = ConverterFactory._bit_val(from_unit)
        to_bit_val: int = ConverterFactory._bit_val(to_unit)

        return Converter(from_bit_val, to_bit_val)
