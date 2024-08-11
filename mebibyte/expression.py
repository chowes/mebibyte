from .units import Units
from .operator import OperatorFactory, Operator


class Expression:
    expression: str
    tokens: list
    postfix_tokens: list

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.tokens = []
        self.postfix_tokens = []

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
            if isinstance(t, Operator):
                while operators and operators[-1] >= t:
                    self.postfix_tokens.append(operators.pop())
                operators.append(t)
            elif isinstance(t, float):
                self.postfix_tokens.append(t)
            else:
                raise ValueError(f"Invalid token: '{t}'")

        while operators:
            self.postfix_tokens.append(operators.pop())

    def evaluate(self) -> float:
        self.postfix()
        operands: list[float] = []

        if not self.postfix_tokens:
            return 0.0

        for t in self.postfix_tokens:
            if isinstance(t, Operator):
                try:
                    r_operand = operands.pop()
                    l_operand = operands.pop()
                    result = t.compute(l_operand, r_operand)
                    operands.append(result)
                except IndexError:
                    raise ValueError(
                        f"Invalid expression: '{self.expression}'")
            elif isinstance(t, float):
                operands.append(t)
            else:
                raise ValueError(f"Invalid token: '{t}'")

        if len(operands) != 1:
            raise ValueError(
                f"Invalid expression: '{self.expression}'")

        return operands[0]
