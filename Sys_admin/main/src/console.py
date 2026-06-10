import cmd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.operation_base import OperationBase
from exercise.exercise import Exercise
from exercise.exercise_collection import ExerciseCollection
from practice.practice import Practice
from practice.judgement import Judgement


class SubMenu(cmd.Cmd):
    prompt = '请选择...... '
    
    def __init__(self, parent, operation_base):
        super().__init__()
        self.parent = parent
        self.operation_base = operation_base
        
    def do_0(self, arg):
        """产生减法习题"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_substraction_exercise(self.operation_base, scale)
            print(f"\n=== 减法习题（共{scale}道）===")
            exercise.format_and_display(5)
        except ValueError:
            print("请输入有效的数字")
    
    def do_1(self, arg):
        """产生加法习题"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_addition_exercise(self.operation_base, scale)
            print(f"\n=== 加法习题（共{scale}道）===")
            exercise.format_and_display(5)
        except ValueError:
            print("请输入有效的数字")
    
    def do_2(self, arg):
        """产生混合习题"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_exercise(self.operation_base, scale)
            print(f"\n=== 混合习题（共{scale}道）===")
            exercise.format_and_display(5)
        except ValueError:
            print("请输入有效的数字")
    
    def do_3(self, arg):
        """返回上层"""
        return True
    
    def default(self, line):
        if line.strip() in ['0', '1', '2', '3']:
            self.onecmd(line)
        else:
            print("输入无效，请输入0-3之间的数字")
    
    def emptyline(self):
        pass
    
    def preloop(self):
        self.show_sub_menu()
    
    def show_sub_menu(self):
        print("功能列表：")
        print("0. 产生减法习题")
        print("1. 产生加法习题")
        print("2. 产生混合习题")
        print("3. 返回上层")


class BatchGenerateMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)
    
    def do_0(self, arg):
        """产生减法习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_index = int(input("请输入文件序号（默认1）：") or 1)
            exercise = Exercise(scale)
            exercise.write_csv_subtraction_exercise(scale, file_index)
        except ValueError:
            print("请输入有效的数字")
    
    def do_1(self, arg):
        """产生加法习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_index = int(input("请输入文件序号（默认1）：") or 1)
            exercise = Exercise(scale)
            exercise.write_csv_addition_exercise(scale, file_index)
        except ValueError:
            print("请输入有效的数字")
    
    def do_2(self, arg):
        """产生混合习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_index = int(input("请输入文件序号（默认1）：") or 1)
            exercise = Exercise(scale)
            exercise.write_csv_mixed_exercise(scale, file_index)
        except ValueError:
            print("请输入有效的数字")
    
    def show_sub_menu(self):
        print("功能列表：")
        print("0. 产生减法习题（保存到文件）")
        print("1. 产生加法习题（保存到文件）")
        print("2. 产生混合习题（保存到文件）")
        print("3. 返回上层")


class RandomGenerateMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)


class OfflinePracticeMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)
    
    def _get_next_file_index(self, exercise_type):
        exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(exercise_dir, exist_ok=True)
        files = os.listdir(exercise_dir)
        max_index = 0
        for f in files:
            if f.startswith(f"{exercise_type}_exercise_"):
                try:
                    index = int(f.split('_')[-1].split('.')[0])
                    max_index = max(max_index, index)
                except:
                    pass
        return max_index + 1
    
    def do_0(self, arg):
        """产生减法习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_substraction_exercise(self.operation_base, scale)
            
            file_index = self._get_next_file_index("subtraction")
            
            exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
            exercise_filename = os.path.join(exercise_dir, f"subtraction_exercise_{scale}_{file_index:03d}.csv")
            equations = [eq.to_string().strip() for eq in exercise.operations]
            with open(exercise_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(equations), columns):
                    line = ','.join(equations[i:i+columns])
                    f.write(line + '\n')
            print(f"减法习题已保存到文件: {exercise_filename}")
            
            print(f"\n=== 减法练习（共{scale}道）===")
            user_answers = []
            for i, eq in enumerate(exercise.operations):
                while True:
                    user_answer = input(f"{i+1}. {eq.as_string()}")
                    try:
                        int(user_answer)
                        break
                    except ValueError:
                        print("请输入有效的数字答案！")
                user_answers.append(user_answer)
                if int(user_answer) == eq.calculate_result():
                    print("回答正确！")
                else:
                    print(f"回答错误！正确答案是 {eq.calculate_result()}")
            
            output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"subtraction_practice_{scale}_{file_index:03d}.csv")
            with open(filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(user_answers), columns):
                    line = ','.join(user_answers[i:i+columns])
                    f.write(line + '\n')
            print(f"\n练习完成！答案已保存到文件: {filename}")
        except ValueError:
            print("请输入有效的数字")
    
    def do_1(self, arg):
        """产生加法习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_addition_exercise(self.operation_base, scale)
            
            file_index = self._get_next_file_index("addition")
            
            exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
            exercise_filename = os.path.join(exercise_dir, f"addition_exercise_{scale}_{file_index:03d}.csv")
            equations = [eq.to_string().strip() for eq in exercise.operations]
            with open(exercise_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(equations), columns):
                    line = ','.join(equations[i:i+columns])
                    f.write(line + '\n')
            print(f"加法习题已保存到文件: {exercise_filename}")
            
            print(f"\n=== 加法练习（共{scale}道）===")
            user_answers = []
            for i, eq in enumerate(exercise.operations):
                while True:
                    user_answer = input(f"{i+1}. {eq.as_string()}")
                    try:
                        int(user_answer)
                        break
                    except ValueError:
                        print("请输入有效的数字答案！")
                user_answers.append(user_answer)
                if int(user_answer) == eq.calculate_result():
                    print("回答正确！")
                else:
                    print(f"回答错误！正确答案是 {eq.calculate_result()}")
            
            output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"addition_practice_{scale}_{file_index:03d}.csv")
            with open(filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(user_answers), columns):
                    line = ','.join(user_answers[i:i+columns])
                    f.write(line + '\n')
            print(f"\n练习完成！答案已保存到文件: {filename}")
        except ValueError:
            print("请输入有效的数字")
    
    def do_2(self, arg):
        """产生混合习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_exercise(self.operation_base, scale)
            
            file_index = self._get_next_file_index("mixed")
            
            exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
            exercise_filename = os.path.join(exercise_dir, f"mixed_exercise_{scale}_{file_index:03d}.csv")
            equations = [eq.to_string().strip() for eq in exercise.operations]
            with open(exercise_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(equations), columns):
                    line = ','.join(equations[i:i+columns])
                    f.write(line + '\n')
            print(f"混合习题已保存到文件: {exercise_filename}")
            
            print(f"\n=== 混合练习（共{scale}道）===")
            user_answers = []
            for i, eq in enumerate(exercise.operations):
                while True:
                    user_answer = input(f"{i+1}. {eq.as_string()}")
                    try:
                        int(user_answer)
                        break
                    except ValueError:
                        print("请输入有效的数字答案！")
                user_answers.append(user_answer)
                if int(user_answer) == eq.calculate_result():
                    print("回答正确！")
                else:
                    print(f"回答错误！正确答案是 {eq.calculate_result()}")
            
            output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"mixed_practice_{scale}_{file_index:03d}.csv")
            with open(filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(user_answers), columns):
                    line = ','.join(user_answers[i:i+columns])
                    f.write(line + '\n')
            print(f"\n练习完成！答案已保存到文件: {filename}")
        except ValueError:
            print("请输入有效的数字")


class OnlinePracticeMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)

    def do_0(self, arg):
        """产生减法习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_substraction_exercise(self.operation_base, scale)
            print(f"\n=== 减法练习（共{scale}道）===")
            correct = 0
            for i, eq in enumerate(exercise.operations):
                user_answer = input(f"{i + 1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct / scale * 100:.1f}%)")
        except ValueError:
            print("请输入有效的数字")

    def do_1(self, arg):
        """产生加法习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_addition_exercise(self.operation_base, scale)
            print(f"\n=== 加法练习（共{scale}道）===")
            correct = 0
            for i, eq in enumerate(exercise.operations):
                user_answer = input(f"{i + 1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct / scale * 100:.1f}%)")
        except ValueError:
            print("请输入有效的数字")

    def do_2(self, arg):
        """产生混合习题并练习"""
        try:
            scale = int(input("请输入题目数量："))
            exercise = Exercise(scale)
            exercise.generate_exercise(self.operation_base, scale)
            print(f"\n=== 混合练习（共{scale}道）===")
            correct = 0
            for i, eq in enumerate(exercise.operations):
                user_answer = input(f"{i + 1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct / scale * 100:.1f}%)")
        except ValueError:
            print("请输入有效的数字")


class MainMenu(cmd.Cmd):
    intro = '===== 100以内口算练习程序 =====\n\n输入数字选择功能，按回车键'
    prompt = '请选择...... '
    
    def __init__(self):
        super().__init__()
    
    def do_0(self, arg):
        """批量产生习题"""
        print('\n你选择了功能0，执行：批量产生习题\n\n100以内口算练习程序-批量产生习题\n\n输入数字选择功能，按回车键')
        BatchGenerateMenu(self).cmdloop()
        self.show_menu()
    
    def do_1(self, arg):
        """随机产生习题"""
        print('\n你选择了功能1，执行：随机产生习题\n\n100以内口算练习程序-随机产生习题\n\n输入数字选择功能，按回车键')
        RandomGenerateMenu(self).cmdloop()
        self.show_menu()
    
    def do_2(self, arg):
        """离线操练习题"""
        print('\n你选择了功能2，执行：离线操练习题\n\n100以内口算练习程序-离线操练习题\n\n输入数字选择功能，按回车键')
        OfflinePracticeMenu(self).cmdloop()
        self.show_menu()
    
    def do_3(self, arg):
        """批量批改操练"""
        print("\n你选择了功能3，执行：批量批改操练")
        self.judge_exercise()
    
    def do_4(self, arg):
        """联机操练习题"""
        print("\n你选择了功能4，执行：联机操练习题\n\n100以内口算练习程序-联机操练习题\n\n输入数字选择功能，按回车键")
        OnlinePracticeMenu(self).cmdloop()
        self.show_menu()
    
    def do_5(self, arg):
        """退出程序"""
        print("退出程序，再见！")
        return True
    
    def default(self, line):
        if line.strip() in ['0', '1', '2', '3', '4', '5']:
            self.onecmd(line)
        else:
            print("输入无效，请输入0-5之间的数字")
    
    def emptyline(self):
        pass
    
    def preloop(self):
        self.show_menu()
    
    def show_menu(self):
        print("功能列表：")
        print("0. 批量产生习题")
        print("1. 随机产生习题")
        print("2. 离线操练习题")
        print("3. 批量批改操练")
        print("4. 联机操练习题")
        print("5. 退出程序")
    
    def judge_exercise(self):
        print("\n=== 批量批改操练 ===")
        exercise_file = input("请输入习题文件路径：").strip()
        practice_file = input("请输入练习结果文件路径：").strip()
        
        if not os.path.exists(exercise_file):
            print(f"错误：习题文件 {exercise_file} 不存在")
            return
        
        if not os.path.exists(practice_file):
            print(f"错误：练习结果文件 {practice_file} 不存在")
            return
        
        exercise = Exercise()
        
        if 'addition' in exercise_file.lower():
            exercise.read_csv_addition_exercise(exercise_file)
        elif 'subtraction' in exercise_file.lower():
            exercise.read_csv_subtraction_exercise(exercise_file)
        elif 'mixed' in exercise_file.lower():
            exercise.read_csv_mixed_exercise(exercise_file)
        else:
            print("无法确定习题类型，请确保文件名包含 'addition'、'subtraction' 或 'mixed'")
            return
        
        judgement = Judgement()
        practice_results = judgement.read_csv_practice(practice_file)
        
        if practice_results is None:
            return
        
        if judgement.judge(exercise, practice_results):
            judgement.display_result()
            save_option = input("是否保存批改结果到文件？(y/n)：").strip().lower()
            if save_option == 'y':
                judgement.write_result_to_csv(exercise_file, practice_file)


if __name__ == '__main__':
    MainMenu().cmdloop()
