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
        filename = os.path.join(output_dir, f"addition_exercise_{count}_{file_index}.csv")
        equations = []
        answers = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_addition_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_addition_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
            answers.append(str(eq.calculate_result()))
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"加法习题已保存到文件: {filename}")
        
        # 自动存储到数据库
        self._save_to_database(filename, 'addition', count, str(file_index))
        
        # 自动生成对应的答案文件
        answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
        os.makedirs(answer_dir, exist_ok=True)
        answer_filename = os.path.join(answer_dir, f"addition_exercise_{count}_{file_index}.csv")
        with open(answer_filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(answers), columns):
                line = ','.join(answers[i:i+columns])
                f.write(line + '\n')
        print(f"加法答案已保存到文件: {answer_filename}")
        
        # 自动存储答案文件到数据库
        self._save_answer_to_database(answer_filename, filename, answers)

    def write_csv_subtraction_exercise(self, count, file_index=1):
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"subtraction_exercise_{count}_{file_index}.csv")
        equations = []
        answers = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_subtraction_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_substraction_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
            answers.append(str(eq.calculate_result()))
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"减法习题已保存到文件: {filename}")
        
        # 自动存储到数据库
        self._save_to_database(filename, 'subtraction', count, str(file_index))
        
        # 自动生成对应的答案文件
        answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
        os.makedirs(answer_dir, exist_ok=True)
        answer_filename = os.path.join(answer_dir, f"subtraction_exercise_{count}_{file_index}.csv")
        with open(answer_filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(answers), columns):
                line = ','.join(answers[i:i+columns])
                f.write(line + '\n')
        print(f"减法答案已保存到文件: {answer_filename}")
        
        # 自动存储答案文件到数据库
        self._save_answer_to_database(answer_filename, filename, answers)

    def write_csv_mixed_exercise(self, count, file_index=1):
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"mixed_exercise_{count}_{file_index}.csv")
        equations = []
        answers = []
        
        ob = OperationBase(self.upper_restriction)
        ob.produce_mixed_base()
        
        temp_exercise = Exercise(count, self.upper_restriction, self.lower_restriction)
        temp_exercise.generate_exercise(ob, count)
        
        for eq in temp_exercise.operations:
            equations.append(eq.to_string().strip())
            answers.append(str(eq.calculate_result()))
        
        with open(filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(equations), columns):
                line = ','.join(equations[i:i+columns])
                f.write(line + '\n')
        
        print(f"混合习题已保存到文件: {filename}")
        
        # 自动存储到数据库
        self._save_to_database(filename, 'mixed', count, str(file_index))
        
        # 自动生成对应的答案文件
        answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
        os.makedirs(answer_dir, exist_ok=True)
        answer_filename = os.path.join(answer_dir, f"mixed_exercise_{count}_{file_index}.csv")
        with open(answer_filename, 'w', encoding='utf-8') as f:
            columns = 5
            for i in range(0, len(answers), columns):
                line = ','.join(answers[i:i+columns])
                f.write(line + '\n')
        print(f"混合答案已保存到文件: {answer_filename}")
        
        # 自动存储答案文件到数据库
        self._save_answer_to_database(answer_filename, filename, answers)

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
    
    def _save_to_database(self, filename, file_type, question_count, file_suffix):
        """自动存储练习文件到数据库
        
        Args:
            filename: 文件名
            file_type: 习题类型 ('addition', 'subtraction', 'mixed')
            question_count: 题目数量
            file_suffix: 文件序号
        """
        try:
            from database.db_manager import db_manager
            
            # 读取文件内容
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 插入数据库
            file_id = db_manager.insert_exercise_file(
                filename=os.path.basename(filename),
                file_type=file_type,
                question_count=question_count,
                file_suffix=file_suffix,
                content=content,
                file_path=filename
            )
            
            if file_id > 0:
                print(f"[自动存储] 习题文件已保存到数据库: {filename} (ID: {file_id})")
                return file_id
            else:
                print(f"[自动存储] 习题文件保存失败: {filename}")
                return 0
                
        except Exception as e:
            print(f"[自动存储] 习题文件保存异常: {filename} - {e}")
            return 0
    
    def _save_answer_to_database(self, answer_filename, exercise_filename, answers):
        """自动存储答案文件到数据库
        
        Args:
            answer_filename: 答案文件名
            exercise_filename: 对应的练习文件名
            answers: 答案列表
        """
        try:
            from database.db_manager import db_manager
            
            # 获取对应的练习文件ID
            exercise = db_manager.get_exercise_by_filename(os.path.basename(exercise_filename))
            if not exercise:
                print(f"[自动存储] 未找到对应的练习文件: {exercise_filename}")
                # 创建练习记录
                file_type = 'mixed'
                if 'addition' in exercise_filename:
                    file_type = 'addition'
                elif 'subtraction' in exercise_filename:
                    file_type = 'subtraction'
                    
                exercise_id = self._save_to_database(exercise_filename, file_type, len(answers), 'auto')
                if exercise_id == 0:
                    return 0
            else:
                exercise_id = exercise['id']
            
            # 读取答案文件内容
            with open(answer_filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 插入数据库
            answer_id = db_manager.insert_answer_file(
                exercise_id=exercise_id,
                filename=os.path.basename(answer_filename),
                content=content,
                file_path=answer_filename
            )
            
            if answer_id > 0:
                print(f"[自动存储] 答案文件已保存到数据库: {answer_filename} (ID: {answer_id})")
                return answer_id
            else:
                print(f"[自动存储] 答案文件保存失败: {answer_filename}")
                return 0
                
        except Exception as e:
            print(f"[自动存储] 答案文件保存异常: {answer_filename} - {e}")
            return 0


if __name__ == "__main__":
    # exercise = Exercise(100)
    # exercise.generate_exercise(100)
    # exercise.format_and_display(5)

    ob = OperationBase(100)
    ob.produce_mixed_base()
    exercise = Exercise(100)
    exercise.generate_exercise(ob,100)
    exercise.format_and_display(5)

