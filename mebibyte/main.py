import argparse
import sys

from .units import Units
from .handler import InputHandler, MalformedExpressionError, InvalidUnitError


def main():
    parser = argparse.ArgumentParser(
        prog='mebibyte', description='Evaluate expressions and convert between units of storage')

    parser.add_argument("expression",
                        nargs=1,
                        type=str)

    args = parser.parse_args()

    if len(args.expression) != 1:
        print("You must provide exactly one expression to evaluate.",
              file=sys.stderr)
        sys.exit(1)
    expression = args.expression[0]

    handler = InputHandler(expression)
    try:
        value, unit = handler.handle()
    except InvalidUnitError as e:
        print(f"{e}", file=sys.stderr)
        print("Supported units:", file=sys.stderr)
        print(f"{', '.join(Units.unit_vals.keys())}", file=sys.stderr)
        sys.exit(1)
    except MalformedExpressionError as e:
        print(f"Expression {expression} is invalid: {e}", file=sys.stderr)
        sys.exit(1)

    if value.is_integer():
        value = int(value)

    if unit:
        print(f"{value} {unit}")
    else:
        print(f"{value}")


if __name__ == "__main__":
    main()
