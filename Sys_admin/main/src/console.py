import cmd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Instance.Sys_admin.main.src.operation_base import OperationBase
from Instance.Sys_admin.main.src.exercise import Exercise
from Instance.Sys_admin.main.src.exercise_collection import ExerciseCollection



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
    # intro = '\n你选择了功能0，执行：批量产生习题\n\n100以内口算练习程序-批量产生习题\n\n输入数字选择功能，按回车键'
    
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)


class RandomGenerateMenu(SubMenu):
    # intro = '\n你选择了功能1，执行：随机产生习题\n\n100以内口算练习程序-随机产生习题\n\n输入数字选择功能，按回车键'
    
    def __init__(self, parent):
        operation_base = OperationBase(100)
        operation_base.produce_addition_base()
        operation_base.produce_subtraction_base()
        operation_base.produce_mixed_base()
        super().__init__(parent, operation_base)


class OfflinePracticeMenu(SubMenu):
    # intro = '\n你选择了功能2，执行：离线操练习题\n\n100以内口算练习程序-离线操练习题\n\n输入数字选择功能，按回车键'
    
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
                user_answer = input(f"{i+1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct/scale*100:.1f}%)")
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
                user_answer = input(f"{i+1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct/scale*100:.1f}%)")
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
                user_answer = input(f"{i+1}. {eq.as_string()}")
                try:
                    if int(user_answer) == eq.calculate_result():
                        print("回答正确！")
                        correct += 1
                    else:
                        print(f"回答错误！正确答案是 {eq.calculate_result()}")
                except ValueError:
                    print(f"输入无效！正确答案是 {eq.calculate_result()}")
            print(f"\n练习完成！正确率：{correct}/{scale} ({correct/scale*100:.1f}%)")
        except ValueError:
            print("请输入有效的数字")


class OnlinePracticeMenu(SubMenu):
    # intro = '\n你选择了功能4，执行：联机操练习题\n\n100以内口算练习程序-联机操练习题\n\n输入数字选择功能，按回车键'

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
        print("功能开发中...")
    
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


if __name__ == '__main__':
    MainMenu().cmdloop()