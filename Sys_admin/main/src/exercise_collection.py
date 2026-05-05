import random

from Sys_admin.main.src.addition import Addition
from Sys_admin.main.src.equation import Equation
from Sys_admin.main.src.subtraction import Subtraction


class ExerciseCollection:
    def __init__(self,scale,restriction):
        self.scale = scale
        self.restriction = restriction
        self.exercise_collection = []
        self.result_set = []


    def generate_exercise_collection(self):

        equation = Equation()

        while len(self.exercise_collection) < self.scale:
            choice = random.randint(0,1)
            if choice == 0:
                equation = Addition()
            elif choice == 1:
                equation = Subtraction()
            else:
                print("没有对应的等式")

            equation.generate_equation(self.restriction)
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

            equation = Addition()
            equation.generate_equation(self.restriction)

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

            equation = Subtraction()
            equation.generate_equation(self.restriction)

            if equation.check_restriction():
                if self.dedupe_collection(equation):
                    self.exercise_collection.append(equation)
                else:
                    pass
            else:
                pass

        for i in range(0,self.scale):
            self.result_set.append(self.exercise_collection[i].calculate_result())


    def output_exercise_collection(self):
        for i in range(0,self.scale):
            print(self.exercise_collection[i].output_equation())


    def output_result_set(self):
        for i in range(0,self.scale):
            print(self.exercise_collection[i].output_equation() + f"{self.result_set[i]}")


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


