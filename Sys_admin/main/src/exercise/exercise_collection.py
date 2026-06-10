import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.addition import Addition
from core.equation import Equation
from core.subtraction import Subtraction


class ExerciseCollection:
    def __init__(self,scale,upper_restriction = 100,lower_restriction = 0):
        self.scale = scale
        self.upper_restriction = upper_restriction
        self.lower_restriction = lower_restriction
        self.exercise_collection = []
        self.result_set = []


    def generate_exercise_collection(self):

        equation = Equation()

        while len(self.exercise_collection) < self.scale:
            choice = random.randint(0,1)
            if choice == 0:
                equation = Addition(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            elif choice == 1:
                equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            else:
                print("没有对应的等式")

            equation.generate_equation()
            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.exercise_collection.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0,self.scale):
            self.result_set.append(self.exercise_collection[i].calculate_result())


    def generate_addition_collection(self):

        while len(self.exercise_collection) < self.scale:

            equation = Addition(upper_restriction= self.upper_restriction,lower_restriction= self.lower_restriction)
            equation.generate_equation()

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.exercise_collection.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0,self.scale):
            self.result_set.append(self.exercise_collection[i].calculate_result())


    def generate_substraction_collection(self):

        while len(self.exercise_collection) < self.scale:

            equation = Subtraction(upper_restriction=self.upper_restriction,lower_restriction=self.lower_restriction)
            equation.generate_equation()

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.exercise_collection.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0,self.scale):
            self.result_set.append(self.exercise_collection[i].calculate_result())



    def output_exercise_collection_to_string(self):
        for i in range(0,self.scale):
            self.exercise_collection[i].to_string()

    def output_exercise_collection_as_string(self):
        for i in range(0,self.scale):
            self.exercise_collection[i].as_string()

    def output_result_set(self):
        for i in range(0,self.scale):
            self.exercise_collection[i].full_string()


    def dedupe_collection(self,equation):
        scale = len(self.exercise_collection)

        for i in range(0,scale):
            if equation.check_same_equation(self.exercise_collection[i]):
                return False

        return True



if __name__ == "__main__":
    exercise_collection = ExerciseCollection(50,100)
    exercise_collection.generate_exercise_collection()
    # exercise_collection.output_exercise_collection()
    exercise_collection.output_result_set()


