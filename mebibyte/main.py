import argparse
import sys

from .expression import Expression
from .converter import ConverterFactory
from .units import Units


def split_expression(input: str) -> tuple[str, str]:
    split = input.split("in")

    if not split:
        raise ValueError(f"Expression '{input}' is malformed.")
    if len(split) > 2:
        raise ValueError(f"Expression '{input}' has multiple 'in' directives.")

    expr = split[0]
    if len(split) == 1:
        return expr, None

    unit = split[1].strip()
    return expr, unit


def main():
    parser = argparse.ArgumentParser(
        prog='mebibyte', description='Convert between units of storage')

    parser.add_argument("expression",
                        nargs=1,
                        type=str)

    args = parser.parse_args()

    if len(args.expression) != 1:
        print("You must provide exactly one expression to evaluate.",
              file=sys.stderr)
        sys.exit(1)

    try:
        expr, unit = split_expression(args.expression[0])
    except ValueError:
        print(
            f"The expression '{args.expression[0]}' is not valid. Format: '<expression> in <output units>'",
            file=sys.stderr)
        sys.exit(1)

    if unit and not Units.is_unit(unit):
        print(f"'{unit}' is not a valid unit.'", file=sys.stderr)
        print("Supported units:", file=sys.stderr)
        print(f"{', '.join(Units.unit_vals.keys())}", file=sys.stderr)
        sys.exit(1)

    expression = Expression(expr)
    try:
        result = expression.evaluate()
    except ValueError as e:
        print(f"Expression '{expr}' is not valid: {e}", file=sys.stderr)
        sys.exit(1)

    if result.unit_power > 0:
        if not unit:
            unit = "bit"
            for token in expr.split():
                if Units.is_unit(token):
                    unit = token
                    break

        converter = ConverterFactory.get_converter("bit", unit)
        val = converter.convert(result.value)
    else:
        if unit:
            print(
                f"Cannot convert dimensionless result '{result.value}' to '{unit}'.'", file=sys.stderr)
            sys.exit(1)
        val = result.value

    if val.is_integer():
        val = int(val)

    if unit:
        print(f"{val} {unit}")
    else:
        print(f"{val}")


if __name__ == "__main__":
    main()
