from werkzeug.exceptions import BadRequest
from flask import Flask, request, jsonify, Response

from mebibyte.handler import ExpressionHandler, MalformedExpressionError, InvalidUnitError


class MebibyteService:
    expression_handler: ExpressionHandler
    debug: bool
    port: int
    app: Flask

    def __init__(self, app: Flask, debug: bool = False, port: int = 5050) -> None:
        self.expression_handler = ExpressionHandler()
        self.app = app
        self.debug = debug
        self.port = port
        self.setup_routes()

    def setup_routes(self) -> None:
        self.app.add_url_rule("/expression", view_func=self.expression, methods=['POST'])

    def start(self) -> None:
        self.app.run(
            debug=self.debug,
            port=self.port,
        )

    def format_result(self, value: float, unit: str) -> str:
        if value.is_integer():
            value = int(value)

        if not unit:
            return f"{value}"
        
        return f"{value} {unit}"

    def expression(self) -> Response:
        try:
            req_data = request.get_json()
            expression = req_data['expression']
        except Exception as e:
            print(f"Failed to get expression from request JSON: {e}")
            raise BadRequest("Invalid request.")

        print(f"Handling request for expression '{expression}'")

        try:
            value, unit = self.expression_handler.handle(expression)
        except InvalidUnitError as e:
            print(
                f"Expression {expression} has an invalid unit conversion: {e}")
            raise BadRequest(str(e)) from e
        except MalformedExpressionError as e:
            print(f"Expression {expression} is invalid: {e}")
            raise BadRequest(str(e)) from e

        result = self.format_result(value, unit)
        response = jsonify({
            "result": result,
        })

        return response
