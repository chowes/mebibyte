import argparse
import sys

from flask import Flask, request, jsonify

from .service import MebibyteService

app = Flask(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='mebibyte-service',
        description='Service that evaluates expressions and converts between units of storage')

    parser.add_argument(
        "--debug",
        nargs=1,
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--port",
        nargs=1,
        type=int,
        default=5050,
    )

    args = parser.parse_args()

    app = Flask(__name__)

    service = MebibyteService(app, args.debug, args.port)
    service.start()


if __name__ == "__main__":
    main()
