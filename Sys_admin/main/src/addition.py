from .equation import Equation
import random
import sys

class Addition(Equation):
    def __init__(self, first_param = None, second_param = None,upper_restriction = 100,lower_restriction = 0):
        super().__init__(first_param,'+',second_param,upper_restriction,lower_restriction)

    def calculate_result(self):
        return self.first_param + self.second_param

    def generate_equation(self):

        self.operator = '+'

        self.first_param = random.randint(self.lower_restriction,self.upper_restriction)
        self.second_param = random.randint(self.lower_restriction,self.upper_restriction)

        return self



if __name__ == "__main__":
    exercise_collection = Addition(upper_restriction=100,lower_restriction=0)
    exercise_collection.generate_equation()
    print(exercise_collection.as_string())