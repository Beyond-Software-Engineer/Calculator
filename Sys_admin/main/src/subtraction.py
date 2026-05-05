import random
import sys

from Sys_admin.main.src.equation import Equation


class Subtraction(Equation):
    def __init__(self,first_param = None,second_param = None,restriction = None):
        super().__init__(first_param,'-',second_param,restriction)

    def calculate_result(self):
        return self.first_param - self.second_param

    def check_restriction(self):
        if self.first_param >= self.restriction:
            return False
        if self.second_param >= self.restriction:
            return False
        if self.calculate_result() >= self.restriction:
            return False
        return True

    def generate_equation(self,restriction):

        self.restriction = restriction
        self.operator = '-'
        min_val = -sys.maxsize

        if min_val >= self.restriction:
            raise ValueError

        self.first_param = random.randint(min_val, self.restriction)
        self.second_param = random.randint(min_val, self.restriction)

        return self

    # def output_equation(self):
    #     super().output_equation()


if __name__ == "__main__":
    exercise_collection = Subtraction()
    exercise_collection.generate_equation(100)
    exercise_collection.output_equation()