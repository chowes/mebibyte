import argparse
import sys

from .expression import Expression
from .converter import ConverterFactory
from .units import Units


def split_expression(input: str) -> tuple[str, str]:
    split = input.split("in")

    if not split or len(split) > 2:
        raise ValueError(f"Invalid expression: '{input}'")

    expr = split[0]
    if len(split) == 2:
        unit = split[1].strip()
        return expr, unit

    for token in split[0].split():
        if Units.is_unit(token):
            unit = token
            return expr, unit

    return expr, "bit"


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

    if not Units.is_unit(unit):
        print(f"'{unit}' is not a valid unit.'", file=sys.stderr)
        print("Supported units:", file=sys.stderr)
        print(f"{', '.join(Units.unit_vals.keys())}", file=sys.stderr)
        sys.exit(1)

    expression = Expression(expr)
    result = expression.evaluate()

    converter = ConverterFactory.get_converter("bit", unit)
    result = converter.convert(result)

    print(f"{result} {unit}")


if __name__ == "__main__":
    main()
