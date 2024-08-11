from .units import Units
from typing import Optional


class Operand:
    value: float
    unit_power: int

    def __init__(self, value: float, unit: Optional[str] = None, unit_power: int = 0):
        if unit and unit_power:
            raise ValueError(
                "You cannot specify both a unit and a unit power.")

        if unit:
            if not Units.is_unit(unit):
                raise ValueError(f"{unit} is not a valid unit.")
            value = value * Units.bit_val(unit)
            self.unit_power = 1
        else:
            self.unit_power = unit_power

        self.value = value

    def __repr__(self) -> str:
        if self.unit_power == 0:
            return f"Operand(value={self.value})"
        if self.unit_power == 1:
            return f"Operand(value={self.value}, unit=bits)"
        return f"Operand(value={self.value}, unit=bits^{self.unit_power})"

    def __add__(self, other):
        if not isinstance(other, Operand):
            raise TypeError("Cannot add Operand with non-Operand.")
        if self.unit_power != other.unit_power:
            raise ValueError("Cannot add operands with different units.")
        return Operand(self.value + other.value, unit_power=self.unit_power)

    def __sub__(self, other):
        if not isinstance(other, Operand):
            raise TypeError("Cannot subtract Operand with non-Operand.")
        if self.unit_power != other.unit_power:
            raise ValueError("Cannot subtract operands with different units.")
        return Operand(self.value - other.value, unit_power=self.unit_power)

    def __mul__(self, other):
        if not isinstance(other, Operand):
            raise TypeError("Cannot multiply Operand with non-Operand.")
        if self.unit_power > 0 and other.unit_power > 0:
            raise ValueError(
                "Storage units can only be multiplied by scalars.")
        return Operand(self.value * other.value, unit_power=self.unit_power + other.unit_power)

    def __truediv__(self, other):
        if not isinstance(other, Operand):
            raise TypeError("Cannot divide Operand with non-Operand.")
        unit_power = self.unit_power - other.unit_power
        if unit_power < 0:
            raise ValueError(
                "Division would result in a unit with negative power.")
        return Operand(self.value / other.value, unit_power=unit_power)
