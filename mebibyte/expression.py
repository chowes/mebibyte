from .units import Units
from .operator import OperatorFactory, Operator


class Expression:
    expression: str
    tokens: list
    postfix: list

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.tokens = []
        self.postfix = []

    def tokenize(self) -> None:
        next_token = None
        last_token = None

        for t in self.expression.split():
            if Units.is_unit(t):
                if not last_token or not isinstance(last_token, float):
                    raise ValueError(
                        f"Invalid expression: '{self.expression}'")

                last_token *= Units.bit_val(t)
                self.tokens.append(last_token)
                last_token = None
                continue

            elif OperatorFactory.is_operator(t):
                next_token = OperatorFactory.new_operator(t)

            else:
                try:
                    next_token = float(t)
                except ValueError as e:
                    raise ValueError(
                        f"Invalid expression: '{self.expression}'") from e

            if last_token:
                self.tokens.append(last_token)
            last_token = next_token

        if last_token:
            self.tokens.append(last_token)

    def postfix(self) -> None:
        self.tokenize()
        operators: list[Operator] = []

        for t in self.tokens:
            pass

    def evaluate(self) -> float:
        self.postfix()
