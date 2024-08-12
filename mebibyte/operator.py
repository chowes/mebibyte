from abc import ABC, abstractmethod
from .operand import Operand


class Operator(ABC):
    precedence: int

    def __lt__(self, other):
        return self.precedence < other.precedence

    def __gt__(self, other):
        return self.precedence > other.precedence

    def __le__(self, other):
        return self.precedence <= other.precedence

    def __ge__(self, other):
        return self.precedence >= other.precedence

    def __eq__(self, other):
        return self.precedence == other.precedence

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def compute(self, l_operand: Operand, r_operand: Operand) -> float:
        pass


class Add(Operator):
    precedence: int = 0

    def compute(self, l_operand: Operand, r_operand: Operand) -> Operand:
        return l_operand + r_operand


class Subtract(Operator):
    precedence: int = 0

    def compute(self, l_operand: Operand, r_operand: Operand) -> Operand:
        return l_operand - r_operand


class Multiply(Operator):
    precedence: int = 1

    def compute(self, l_operand: Operand, r_operand: Operand) -> Operand:
        return l_operand * r_operand


class Divide(Operator):
    precedence: int = 1

    def compute(self, l_operand: Operand, r_operand: Operand) -> Operand:
        return l_operand / r_operand


class LeftParen(Operator):
    precedence: int = 3

    def compute(self, l_operand: Operand = None, r_operand: Operand = None) -> Operand:
        raise TypeError


class RightParen(Operator):
    precedence: int = 3

    def compute(self, l_operand: Operand = None, r_operand: Operand = None) -> Operand:
        raise TypeError


class OperatorFactory:
    valid = set(["+", "-", "*", "/", "(", ")"])

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
            case "(":
                return LeftParen()
            case ")":
                return RightParen()
            case _:
                raise ValueError(f"{operator} is not a valid operator")
