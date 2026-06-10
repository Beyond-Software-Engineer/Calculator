from typing import List, Optional

from .addition import Addition
from .equation import Equation
from .subtraction import Subtraction


class OperationBase:
    def __init__(self,upper_restriction = 100,lower_restriction = 0):
        self.upper_restriction = upper_restriction
        self.lower_restriction = lower_restriction
        self.addition_base: List[List[Optional[Addition]]] = [[None for _ in range(self.upper_restriction + 1)] for _ in range(self.upper_restriction + 1)]
        self.subtraction_base: List[List[Optional[Subtraction]]] = [[None for _ in range(self.upper_restriction + 1)] for _ in range(self.upper_restriction + 1)]
        self.mixed_base: List[List[Optional[Equation]]] = [[None for _ in range(self.upper_restriction + 1)] for _ in range(self.upper_restriction + 1)]

    def produce_addition_base(self):
        for i in range(self.upper_restriction + 1):
            for j in range(self.upper_restriction + 1):
                if i + j <= self.upper_restriction:
                    ao = Addition(i,j,self.upper_restriction)
                    self.addition_base[i][j] = ao

    def produce_subtraction_base(self):
        for i in range(self.upper_restriction + 1):
            for j in range(self.upper_restriction + 1):
                if i - j >= self.lower_restriction:
                    so = Subtraction(i,j,self.upper_restriction)
                    self.subtraction_base[i][j] = so

    def produce_mixed_base(self):
        for i in range(self.upper_restriction + 1):
            for j in range(self.upper_restriction + 1):
                if i >= j:
                    if i + j <= self.upper_restriction:
                        ao = Addition(i,j,self.upper_restriction)
                        self.mixed_base[i][j] = ao
                    else:
                        pass
                else:
                    if i - (self.upper_restriction - j) >= self.lower_restriction:
                        so = Subtraction(i,(self.upper_restriction - j),self.upper_restriction)
                        self.mixed_base[i][j] = so

