from abc import ABC, abstractmethod


class Operator(ABC):
    precedence: int

    def __lt__(self, other):
        return self.precedence < other.precedence

    def __gt__(self, other):
        return self.precedence > other.precedence

    def __eq__(self, other):
        return self.precedence == other.precedence

    @abstractmethod
    def compute(self, l_operand: float, r_operand: float) -> float:
        pass


class Add(Operator):
    precedence: int = 0

    def compute(self, l_operand: float, r_operand: float) -> float:
        return l_operand + r_operand


class Subtract(Operator):
    precedence: int = 0

    def compute(self, l_operand: float, r_operand: float) -> float:
        return l_operand - r_operand


class Multiply(Operator):
    precedence: int = 1

    def compute(self, l_operand: float, r_operand: float) -> float:
        return l_operand * r_operand


class Divide(Operator):
    precedence: int = 1

    def compute(self, l_operand: float, r_operand: float) -> float:
        return l_operand / r_operand


class OperatorFactory:
    valid = set(["+", "-", "*", "/"])

    @staticmethod
    def is_operator(operator: str) -> bool:
        return operator in OperatorFactory.valid

    @staticmethod
    def new_operator(operator: str) -> Operator:
        match operator:
            case "+":
                return Add()
            case "-":
                return Subtract()
            case "*":
                return Multiply()
            case "/":
                return Divide()
            case _:
                raise ValueError(f"{operator} is not a valid operator")
