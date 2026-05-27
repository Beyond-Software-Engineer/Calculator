import random
from typing import List, Optional

from Sys_admin.main.src.operation_base import OperationBase
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

        operations = []
        results = []

        while len(operations) < scale:
            choice = random.randint(0,1)
            if choice == 0:
                equation:Equation = Addition(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            elif choice == 1:
                equation:Equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            else:
                pass

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            results.append(self.operations[i].calculate_result())

        self.operations = operations
        self.results = results



    def generate_addition_exercise(self,scale = None):
        if scale is None:
            scale = self.scale

        operations = []
        results = []

        while len(operations) < scale:
            equation:Equation = Addition(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            results.append(self.operations[i].calculate_result())

        self.operations = operations
        self.results = results

    def generate_substraction_exercise(self,scale = None):
        if scale is None:
            scale = self.scale

        operations = []
        results = []

        while len(operations) < scale:
            equation:Equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass


        for i in range(0,scale):
            results.append(self.operations[i].calculate_result())

        self.operations = operations
        self.results = results

    def generate_exercise(self,operation_base: OperationBase,scale = None):
        if scale is None:
            scale = self.scale

        operations = []
        results = []

        while len(operations) < scale:
            row = random.randint(self.lower_restriction,self.upper_restriction)
            column = random.randint(self.lower_restriction,self.upper_restriction)
            equation:Equation = operation_base.mixed_base[row][column]

            if equation is None:
                continue

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0,scale):
            results.append(operations[i].calculate_result())

        self.operations = operations
        self.results = results

    def generate_addition_exercise(self,operation_base: OperationBase, scale=None):
        if scale is None:
            scale = self.scale

        operations = []
        results = []

        while len(operations) < scale:
            row = random.randint(self.lower_restriction, self.upper_restriction)
            column = random.randint(self.lower_restriction, self.upper_restriction)
            equation: Equation = operation_base.addition_base[row][column]

            if equation is None:
                continue

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0, scale):
            results.append(operations[i].calculate_result())

        self.operations = operations
        self.results = results

    def generate_substraction_exercise(self,operation_base: OperationBase, scale=None):
        if scale is None:
            scale = self.scale

        operations = []
        results = []

        while len(operations) < scale:
            row = random.randint(self.lower_restriction, self.upper_restriction)
            column = random.randint(self.lower_restriction, self.upper_restriction)
            equation: Equation = operation_base.subtraction_base[row][column]

            if equation is None:
                continue

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    operations.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0, scale):
            results.append(operations[i].calculate_result())

        self.operations = operations
        self.results = results

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
    # exercise = Exercise(100)
    # exercise.generate_exercise(100)
    # exercise.format_and_display(5)

    ob = OperationBase(100)
    ob.produce_mixed_base()
    exercise = Exercise(100)
    exercise.generate_exercise(ob,100)
    exercise.format_and_display(5)

