import random
from typing import List

from Sys_admin.main.src.addition import Addition
from Sys_admin.main.src.equation import Equation
from Sys_admin.main.src.subtraction import Subtraction

class Exercise:
    def __init__(self,scale = 0,upper_restriction = 100,lower_restriction = 0):
        self.scale = scale
        self.upper_restriction = upper_restriction
        self.lower_restriction = lower_restriction
        self.operations: List[Equation] = []
        self.results = []

    def generate_exercise(self,scale = None):
        if scale is None:
            scale = self.scale

        self.operations = []
        self.results = []

        while len(self.operations) < scale:
            choice = random.randint(0,1)
            if choice == 0:
                equation:Equation = Addition(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            elif choice == 1:
                equation:Equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            else:
                equation = Equation(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            self.results.append(self.operations[i].calculate_result())

    def generate_addition_exercise(self,scale = None):
        if scale is None:
            scale = self.scale

        self.operations = []
        self.results = []

        while len(self.operations) < scale:
            equation:Equation = Addition(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            self.results.append(self.operations[i].calculate_result())

    def generate_substraction_exercise(self,scale = None):
        if scale is None:
            scale = self.scale

        self.operations = []
        self.results = []

        while len(self.operations) < scale:
            equation:Equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            self.results.append(self.operations[i].calculate_result())


    def dedupe_collection(self, equation):
        scale = len(self.operations)

        for i in range(0, scale):
            if equation.check_same_equation(self.operations[i]):
                return False

        return True

    def format_and_display(self,column_per_row):
        for i in range(0,self.scale):
            if ((i+1) % column_per_row) != 0:
                print(f"{self.operations[i].full_string():<16}",end="")
            else:
                print(f"{self.operations[i].full_string():<16}",end="\n")

        print("\n")

if __name__ == "__main__":
    exercise = Exercise(100)
    exercise.generate_exercise(100)
    exercise.format_and_display(5)