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
    
    def _get_file_suffix(self):
        while True:
            suffix = input("请输入文件结尾（默认none，不包含中文）：").strip()
            if not suffix:
                return "none"
            if any('\u4e00' <= c <= '\u9fff' for c in suffix):
                print("文件结尾不允许包含中文，请重新输入")
                continue
            return suffix
    
    def do_0(self, arg):
        """产生减法习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_suffix = self._get_file_suffix()
            exercise = Exercise(scale)
            exercise.write_csv_subtraction_exercise(scale, file_suffix)
        except ValueError:
            print("请输入有效的数字")
    
    def do_1(self, arg):
        """产生加法习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_suffix = self._get_file_suffix()
            exercise = Exercise(scale)
            exercise.write_csv_addition_exercise(scale, file_suffix)
        except ValueError:
            print("请输入有效的数字")
    
    def do_2(self, arg):
        """产生混合习题并保存"""
        try:
            scale = int(input("请输入题目数量："))
            file_suffix = self._get_file_suffix()
            exercise = Exercise(scale)
            exercise.write_csv_mixed_exercise(scale, file_suffix)
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
            
            # 生成答案文件
            answers = [str(eq.calculate_result()) for eq in exercise.operations]
            answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
            os.makedirs(answer_dir, exist_ok=True)
            answer_filename = os.path.join(answer_dir, f"subtraction_exercise_{scale}_{file_index:03d}.csv")
            with open(answer_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(answers), columns):
                    line = ','.join(answers[i:i+columns])
                    f.write(line + '\n')
            print(f"减法答案已保存到文件: {answer_filename}")
            
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
            
            # 生成答案文件
            answers = [str(eq.calculate_result()) for eq in exercise.operations]
            answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
            os.makedirs(answer_dir, exist_ok=True)
            answer_filename = os.path.join(answer_dir, f"addition_exercise_{scale}_{file_index:03d}.csv")
            with open(answer_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(answers), columns):
                    line = ','.join(answers[i:i+columns])
                    f.write(line + '\n')
            print(f"加法答案已保存到文件: {answer_filename}")
            
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
            
            # 生成答案文件
            answers = [str(eq.calculate_result()) for eq in exercise.operations]
            answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
            os.makedirs(answer_dir, exist_ok=True)
            answer_filename = os.path.join(answer_dir, f"mixed_exercise_{scale}_{file_index:03d}.csv")
            with open(answer_filename, 'w', encoding='utf-8') as f:
                columns = 5
                for i in range(0, len(answers), columns):
                    line = ','.join(answers[i:i+columns])
                    f.write(line + '\n')
            print(f"混合答案已保存到文件: {answer_filename}")
            
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


class JudgementMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)
    
    def show_sub_menu(self):
        print("功能列表：")
        print("0. 批改练习")
        print("3. 返回上层")
    
    def _get_practice_files(self):
        """扫描 practice_result 目录下的所有用户答题结果文件"""
        practice_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result"
        os.makedirs(practice_dir, exist_ok=True)
        
        files = []
        for f in os.listdir(practice_dir):
            if f.endswith('.csv'):
                files.append(f)
        
        # 按类型和序号排序
        def sort_key(filename):
            if 'addition' in filename.lower():
                prefix = '0'
            elif 'subtraction' in filename.lower():
                prefix = '1'
            else:
                prefix = '2'
            return prefix + filename
        
        files.sort(key=sort_key)
        return files
    
    def _get_answer_file(self, practice_filename):
        """根据用户答题文件名查找对应的答案文件"""
        answer_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer"
        
        # 将 _practice_ 替换为 _exercise_
        answer_filename = practice_filename.replace('_practice_', '_exercise_')
        answer_path = os.path.join(answer_dir, answer_filename)
        
        if os.path.exists(answer_path):
            return answer_path
        return None
    
    def _get_exercise_file(self, practice_filename):
        """根据用户答题文件名查找对应的习题文件"""
        exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        
        # 将 _practice_ 替换为 _exercise_
        exercise_filename = practice_filename.replace('_practice_', '_exercise_')
        exercise_path = os.path.join(exercise_dir, exercise_filename)
        
        if os.path.exists(exercise_path):
            return exercise_path
        return None
    
    def _select_practice_file(self):
        """显示用户答题文件列表并让用户选择"""
        files = self._get_practice_files()
        
        if not files:
            print("\n错误：practice_result 目录下没有用户答题文件")
            return None
        
        print("\n=== 可批改的用户答题文件列表 ===")
        for i, f in enumerate(files, 1):
            # 检查是否有对应的习题文件和答案文件
            exercise_file = self._get_exercise_file(f)
            answer_file = self._get_answer_file(f)
            exercise_status = "✓" if exercise_file else "✗"
            answer_status = "✓" if answer_file else "✗"
            print(f"{i}. {f}")
            print(f"   [习题:{exercise_status}] [答案:{answer_status}]")
        
        while True:
            choice = input("\n请输入用户答题文件序号（输入0返回）：").strip()
            try:
                idx = int(choice)
                if idx == 0:
                    return None
                if 1 <= idx <= len(files):
                    practice_file = os.path.join(
                        r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result",
                        files[idx - 1]
                    )
                    return practice_file, files[idx - 1]
            except ValueError:
                pass
            print("无效选择，请重新输入")
    
    def do_0(self, arg):
        """批改练习"""
        print("\n=== 批量批改操练 ===")
        
        # 选择用户答题文件
        result = self._select_practice_file()
        if result is None:
            return
        
        practice_file, practice_filename = result
        
        # 查找对应的习题文件
        exercise_file = self._get_exercise_file(practice_filename)
        if exercise_file is None:
            print(f"\n错误：未找到习题文件 {practice_filename.replace('_practice_', '_exercise_')}")
            return
        
        # 查找对应的答案文件
        answer_file = self._get_answer_file(practice_filename)
        if answer_file is None:
            print(f"\n错误：未找到答案文件 {practice_filename.replace('_practice_', '_exercise_')}")
            return
        
        print(f"\n已自动关联：")
        print(f"  习题文件: {os.path.basename(exercise_file)}")
        print(f"  答案文件: {os.path.basename(answer_file)}")
        print(f"  答题文件: {os.path.basename(practice_file)}")
        
        # 读取习题
        exercise = Exercise()
        
        if 'addition' in exercise_file.lower():
            exercise.read_csv_addition_exercise(exercise_file)
        elif 'subtraction' in exercise_file.lower():
            exercise.read_csv_subtraction_exercise(exercise_file)
        elif 'mixed' in exercise_file.lower():
            exercise.read_csv_mixed_exercise(exercise_file)
        else:
            print("无法确定习题类型")
            return
        
        # 读取用户答题结果
        judgement = Judgement()
        practice_results = judgement.read_csv_practice(practice_file)
        
        if practice_results is None:
            return
        
        # 批改
        if judgement.judge(exercise, practice_results):
            judgement.display_result()
            save_option = input("是否保存批改结果到文件？(y/n)：").strip().lower()
            if save_option == 'y':
                judgement.write_result_to_csv(exercise_file, practice_file)


class OnlinePracticeMenu(SubMenu):
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)
    
    def show_sub_menu(self):
        print("功能列表：")
        print("0. 开始联机操练")
        print("3. 返回上层")

    def _select_exercise_type(self):
        while True:
            print("\n请选择练习题类型：")
            print("0. 减法习题")
            print("1. 加法习题")
            print("2. 混合习题")
            choice = input("请输入选择（0-2）：")
            if choice in ['0', '1', '2']:
                return int(choice)
            print("无效选择，请重新输入")

    def _select_exercise_file(self, exercise_type):
        exercise_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
        os.makedirs(exercise_dir, exist_ok=True)
        
        type_prefix = {0: "subtraction", 1: "addition", 2: "mixed"}
        prefix = type_prefix[exercise_type]
        
        files = [f for f in os.listdir(exercise_dir) if f.startswith(f"{prefix}_exercise_")]
        
        if not files:
            print(f"未找到{['减法', '加法', '混合'][exercise_type]}习题文件")
            return None
        
        print(f"\n可用的{['减法', '加法', '混合'][exercise_type]}习题文件：")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        
        while True:
            choice = input("请输入文件序号（输入0返回重新选题）：")
            try:
                idx = int(choice)
                if idx == 0:
                    return None
                if 1 <= idx <= len(files):
                    return os.path.join(exercise_dir, files[idx-1])
            except ValueError:
                pass
            print("无效选择，请重新输入")

    def _load_exercise_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        equations = []
        for line in content.strip().split('\n'):
            for eq_str in line.split(','):
                eq_str = eq_str.strip()
                if eq_str:
                    equations.append(eq_str)
        
        return equations

    def do_0(self, arg):
        """联机操练"""
        while True:
            exercise_type = self._select_exercise_type()
            
            while True:
                file_path = self._select_exercise_file(exercise_type)
                if file_path is None:
                    break
                
                try:
                    equations = self._load_exercise_from_file(file_path)
                    print(f"\n成功打开文件：{os.path.basename(file_path)}")
                    break
                except Exception as e:
                    print(f"无法打开文件：{e}")
                    retry = input("是否重试？(y/n)：").lower()
                    if retry != 'y':
                        file_path = None
                        break
            
            if file_path is None:
                continue
            
            while True:
                ready = input("\n准备答题吗？(y/n)：").lower()
                if ready == 'y':
                    break
                elif ready == 'n':
                    reselect = input("重新选题吗？(y/n)：").lower()
                    if reselect == 'y':
                        break
                    else:
                        return
                else:
                    print("请输入 y 或 n")
            else:
                continue
            
            print(f"\n=== 联机练习（共{len(equations)}道）===")
            print("每行显示一个算式等待用户输入算式答案数字，回车，进入下一个，直至题目全部完成。")
            
            user_answers = []
            correct_count = 0
            
            for i, eq_str in enumerate(equations):
                eq_str = eq_str.strip()
                
                if '+' in eq_str:
                    nums = eq_str.split('+')
                    num1 = int(nums[0].strip())
                    num2 = int(nums[1].strip())
                    correct_answer = num1 + num2
                elif '-' in eq_str:
                    nums = eq_str.split('-')
                    num1 = int(nums[0].strip())
                    num2 = int(nums[1].strip())
                    correct_answer = num1 - num2
                else:
                    correct_answer = 0
                
                while True:
                    user_answer = input(f"{i+1}. {eq_str} = ")
                    try:
                        int(user_answer)
                        break
                    except ValueError:
                        print("请输入有效的数字答案！")
                
                user_answers.append(user_answer)
                
                full_eq = f"{eq_str} = {correct_answer}"
                print(f"显示：\"{full_eq}\"")
                
                if int(user_answer) == correct_answer:
                    print("回答正确！")
                    correct_count += 1
                else:
                    print(f"回答错误！正确答案是 {correct_answer}")
            
            result_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_checking"
            os.makedirs(result_dir, exist_ok=True)
            filename = os.path.join(result_dir, f"online_result_{os.path.basename(file_path)}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"总题数: {len(equations)}\n")
                f.write(f"正确数: {correct_count}\n")
                f.write(f"错误数: {len(equations) - correct_count}\n")
                f.write(f"得分: {correct_count / len(equations) * 100:.1f}\n")
                f.write("\n详细结果:\n")
                for i, (eq_str, answer) in enumerate(zip(equations, user_answers)):
                    parts = eq_str.split('=')
                    correct_answer = int(parts[1].strip()) if len(parts) == 2 else "未知"
                    is_correct = int(answer) == correct_answer
                    f.write(f"{i+1}. {eq_str} 你的答案:{answer} {'正确' if is_correct else f'错误(正确答案:{correct_answer})'}\n")
            
            print(f"\n=== 练习完成 ===")
            print(f"总题数: {len(equations)}")
            print(f"正确数: {correct_count}")
            print(f"错误数: {len(equations) - correct_count}")
            print(f"得分: {correct_count / len(equations) * 100:.1f}")
            print(f"结果已保存到文件: {filename}")
            
            while True:
                end = input("\n结束吗？(y/n)：").lower()
                if end == 'y':
                    return
                elif end == 'n':
                    break
                else:
                    print("请输入 y 或 n")


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
        print("\n你选择了功能3，执行：批量批改操练\n\n100以内口算练习程序-批量批改操练\n\n输入数字选择功能，按回车键")
        JudgementMenu(self).cmdloop()
        self.show_menu()
    
    def do_4(self, arg):
        """联机操练习题"""
        print("\n你选择了功能4，执行：联机操练习题\n\n100以内口算练习程序-联机操练习题\n\n输入数字选择功能，按回车键")
        OnlinePracticeMenu(self).cmdloop()
        self.show_menu()
    
    def do_5(self, arg):
        """退出程序"""
        while True:
            confirm = input("确定要退出吗？(y/n)：").strip().lower()
            if confirm == 'y':
                print("退出程序，再见！")
                return True
            elif confirm == 'n':
                print("返回主菜单")
                self.show_menu()
                return
            else:
                print("请输入 y 或 n")
    
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


if __name__ == '__main__':
    MainMenu().cmdloop()
