from .operand import Operand
from .expression import Expression
from .converter import ConverterFactory
from .units import Units


class MalformedExpressionError(ValueError):
    pass


class InvalidUnitError(MalformedExpressionError):
    pass


class ExpressionHandler:
    def __init__(self):
        pass

    def handle(self, input_string: str) -> float:
        input_string = input_string.lower()
        expr, unit = self.split_expression(input_string)
        if unit and not Units.is_unit(unit):
            raise InvalidUnitError(
                f"'{unit}' is not a valid unit.")

        expression = Expression(expr)
        try:
            result = expression.evaluate()
        except ValueError as e:
            raise MalformedExpressionError(e)

        return self.convert_result(result, unit, expr)

    def split_expression(self, input: str) -> tuple[str, str]:
        split = input.split("in")

        if not split:
            raise MalformedExpressionError(
                f"Expression is malformed.")
        if len(split) > 2:
            raise MalformedExpressionError(
                f"Expression has multiple 'in' directives.")

        expr = split[0]
        if len(split) == 1:
            return expr, None

        unit = split[1].strip()
        return expr, unit

    def infer_unit(self, expr: str) -> str:
        for token in expr.split():
            if Units.is_unit(token):
                return token

        return None

    def convert_result(self, result: Operand, unit: str, expr: str) -> tuple[float, str]:
        if result.unit_power > 0:
            if not unit:
                unit = self.infer_unit(expr)

            # Should be impossible.
            if not unit:
                raise MalformedExpressionError(
                    f"Result has a unit, but no valid units in input string.")

            converter = ConverterFactory.get_converter("bit", unit)
            val = converter.convert(result.value)
        else:
            if unit:
                raise MalformedExpressionError(
                    f"Cannot convert dimensionless result '{result.value}' to '{unit}'.")
            val = result.value

        if unit:
            unit = Units.prettify(unit)

        return val, unit
