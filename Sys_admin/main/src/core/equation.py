from abc import ABC,abstractmethod
from dataclasses import dataclass


class Equation(ABC):
    def __init__(self,first_param = None,operator = None,second_param = None,upper_restriction = 0,lower_restriction = 100):
        self.first_param = first_param
        self.operator = operator
        self.second_param = second_param
        self.upper_restriction = upper_restriction
        self.lower_restriction = lower_restriction


    @abstractmethod
    def calculate_result(self):
        pass

    @abstractmethod
    def generate_equation(self):
        pass

    def check_restriction(self):
        if self.first_param > self.upper_restriction :
            return False
        if self.first_param < self.lower_restriction:
            return False
        if self.second_param > self.upper_restriction:
            return False
        if self.second_param < self.lower_restriction:
            return False
        if self.calculate_result() > self.upper_restriction:
            return False
        if self.calculate_result() < self.lower_restriction:
            return False
        return True

    def get_left_operand(self):
        return self.first_param

    def get_right_operand(self):
        return self.second_param

    def get_operator(self):
        return self.operator

    def to_string(self):
        return f"{self.first_param} {self.operator} {self.second_param} "

    def as_string(self):
        return f"{self.first_param} {self.operator} {self.second_param} = "

    def full_string(self):
        return f"{self.first_param} {self.operator} {self.second_param} = {self.calculate_result()}"


    def check_same_equation(self,equation):
        if self.operator != equation.operator:
            return False
        else:
            if self.first_param == equation.first_param :
                if self.second_param == equation.second_param:
                    return True
                else:
                    return False
            elif self.first_param == equation.second_param:
                if self.second_param == equation.first_param:
                    return True
                else:
                    return False
        return False




