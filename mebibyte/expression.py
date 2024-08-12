from .units import Units
from .operator import OperatorFactory, Operator
from .operand import Operand


class Expression:
    expression: str
    tokens: list
    postfix_tokens: list

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.tokens = []
        self.postfix_tokens = []

    def tokenize_operand(self, t: str) -> Operand:
        try:
            next_token = Operand(float(t))
            return next_token
        except ValueError:
            pass

        split = t.split("^")
        if len(split) == 2:
            base = float(split[0])
            exp = float(split[1])
            return Operand(base ** exp)

        raise ValueError

    def tokenize(self) -> None:
        last_token = None

        for t in self.expression.split():
            next_token = None
            if Units.is_unit(t):
                try:
                    last_token *= Operand(1, t)
                    self.tokens.append(last_token)
                    last_token = None
                except (ValueError, TypeError) as e:
                    raise ValueError(
                        f"Unit {t} associated with non-scalar {last_token}") from e
                continue
            elif OperatorFactory.is_operator(t):
                next_token = OperatorFactory.new_operator(t)
            else:
                try:
                    next_token = self.tokenize_operand(t)
                except ValueError:
                    raise ValueError(
                        f"Token {t} is not a valid token.")

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
            elif isinstance(t, Operand):
                self.postfix_tokens.append(t)
            else:
                raise ValueError(f"Invalid token: '{t}'")

        while operators:
            self.postfix_tokens.append(operators.pop())

    def evaluate(self) -> Operand:
        self.postfix()
        operands: list[Operand] = []

        if not self.postfix_tokens:
            return Operand(0.0)

        for t in self.postfix_tokens:
            if isinstance(t, Operator):
                try:
                    r_operand = operands.pop()
                    l_operand = operands.pop()
                    result = t.compute(l_operand, r_operand)
                    operands.append(result)
                except IndexError:
                    raise ValueError(
                        f"Malformed expression.")
                except ZeroDivisionError:
                    raise ValueError(
                        f"Evaluating expression results in zero divsion.")
            elif isinstance(t, Operand):
                operands.append(t)
            else:
                raise ValueError(f"Invalid token: '{t}'")

        if len(operands) != 1:
            raise ValueError(
                f"Malformed expression.")

        return operands[0]
