import random
import re
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.operation_base import OperationBase
from core.addition import Addition
from core.equation import Equation
from core.subtraction import Subtraction

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

    def write_csv_addition_exercise(self, count, file_index=1):
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"addition_exercise_{count}_{file_index:03d}.csv")
        equations = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_addition_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_addition_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"加法习题已保存到文件: {filename}")

    def write_csv_subtraction_exercise(self, count, file_index=1):
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"subtraction_exercise_{count}_{file_index:03d}.csv")
        equations = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_subtraction_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_substraction_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"减法习题已保存到文件: {filename}")

    def write_csv_mixed_exercise(self, count, file_index=1):
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"mixed_exercise_{count}_{file_index:03d}.csv")
        equations = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_mixed_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"混合习题已保存到文件: {filename}")

    def read_csv_addition_exercise(self, csv_file):
        if not os.path.exists(csv_file):
            print(f"错误：文件 {csv_file} 不存在")
            return None
        
        equations = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(r'[^\d+\-,\n]', '', content)
                parts = re.split(r'[,|\n]+', content)
                
                for part in parts:
                    part = part.strip()
                    if part:
                        match = re.match(r'(\d+)\s*\+\s*(\d+)', part)
                        if match:
                            first = int(match.group(1))
                            second = int(match.group(2))
                            eq = Addition(first, second, self.upper_restriction, self.lower_restriction)
                            equations.append(eq)
        
            self.operations = equations
            self.scale = len(equations)
            self.results = [eq.calculate_result() for eq in self.operations]
            print(f"成功从文件 {csv_file} 读取 {self.scale} 道加法习题")
            return self
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return None

    def read_csv_subtraction_exercise(self, csv_file):
        if not os.path.exists(csv_file):
            print(f"错误：文件 {csv_file} 不存在")
            return None
        
        equations = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(r'[^\d\-,\n]', '', content)
                parts = re.split(r'[,|\n]+', content)
                
                for part in parts:
                    part = part.strip()
                    if part:
                        match = re.match(r'(\d+)\s*-\s*(\d+)', part)
                        if match:
                            first = int(match.group(1))
                            second = int(match.group(2))
                            eq = Subtraction(first, second, self.upper_restriction, self.lower_restriction)
                            equations.append(eq)
        
            self.operations = equations
            self.scale = len(equations)
            self.results = [eq.calculate_result() for eq in self.operations]
            print(f"成功从文件 {csv_file} 读取 {self.scale} 道减法习题")
            return self
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return None

    def read_csv_mixed_exercise(self, csv_file):
        if not os.path.exists(csv_file):
            print(f"错误：文件 {csv_file} 不存在")
            return None
        
        equations = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(r'[^\d+\-,\n]', '', content)
                parts = re.split(r'[,|\n]+', content)
                
                for part in parts:
                    part = part.strip()
                    if part:
                        match_add = re.match(r'(\d+)\s*\+\s*(\d+)', part)
                        match_sub = re.match(r'(\d+)\s*-\s*(\d+)', part)
                        if match_add:
                            first = int(match_add.group(1))
                            second = int(match_add.group(2))
                            eq = Addition(first, second, self.upper_restriction, self.lower_restriction)
                            equations.append(eq)
                        elif match_sub:
                            first = int(match_sub.group(1))
                            second = int(match_sub.group(2))
                            eq = Subtraction(first, second, self.upper_restriction, self.lower_restriction)
                            equations.append(eq)
        
            self.operations = equations
            self.scale = len(equations)
            self.results = [eq.calculate_result() for eq in self.operations]
            print(f"成功从文件 {csv_file} 读取 {self.scale} 道混合习题")
            return self
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return None

    def write_csv_addition_exercises(self, number, count):
        for i in range(1, number + 1):
            self.write_csv_addition_exercise(count, i)

    def write_csv_subtraction_exercises(self, number, count):
        for i in range(1, number + 1):
            self.write_csv_subtraction_exercise(count, i)

    def write_csv_mixed_exercises(self, number, count):
        for i in range(1, number + 1):
            self.write_csv_mixed_exercise(count, i)


if __name__ == "__main__":
    # exercise = Exercise(100)
    # exercise.generate_exercise(100)
    # exercise.format_and_display(5)

    ob = OperationBase(100)
    ob.produce_mixed_base()
    exercise = Exercise(100)
    exercise.generate_exercise(ob,100)
    exercise.format_and_display(5)

