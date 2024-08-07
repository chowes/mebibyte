import argparse
from .converter import ConverterFactory


def main():
    parser = argparse.ArgumentParser(
        prog='mebibyte', description='Convert between units of storage')

    parser.add_argument('--from',
                        dest='from_',
                        type=str,
                        required=True,
                        help='unit to convert from')
    parser.add_argument('--to',
                        type=str,
                        nargs='*',
                        required=True,
                        help='unit to convert to')
    parser.add_argument('--value',
                        default=1,
                        type=float,
                        help='value to convert')

    args = parser.parse_args()
    from_unit = args.from_
    to_units = args.to

    cf = ConverterFactory()
    for unit in to_units:
        c = cf.get_converter(from_unit, unit)
        v = c.convert(args.value)
        print(f"{args.value} {from_unit}={v} {unit}")


if __name__ == "__main__":
    main()
