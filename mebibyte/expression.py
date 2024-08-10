from .units import Units


class Expression:
    expression: str

    def __init__(self, expression: str) -> None:
        self.expression = expression

    def tokenize(self) -> list[str]:
        tokens: list[str] = []
        last_token: str = ""

        for t in self.expression.split():
            if Units.is_unit(t):
                if not last_token:
                    raise ValueError(
                        f"Invalid expression: '{self.expression}'")

                try:
                    val = float(last_token)
                    val *= Units.bit_val(t)
                    tokens.append(str(val))
                    last_token = ""
                except Exception as e:
                    raise ValueError(
                        f"Invalid expression: '{self.expression}'") from e
            else:
                if last_token:
                    tokens.append(last_token)
                last_token = t

        if last_token:
            tokens.append(last_token)

        return tokens

    def evaluate(self) -> float:
        tokens = self.tokenize()
