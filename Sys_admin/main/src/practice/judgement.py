import re
import os
import sys
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercise.exercise import Exercise


class Judgement:
    def __init__(self):
        self.correct = 0
        self.wrong = 0
        self.checking_list = []
    
    def read_csv_practice(self, file_path):
        if not os.path.exists(file_path):
            print(f"错误：文件 {file_path} 不存在")
            return None
        
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(r'[^\d\-,\n]', '', content)
                parts = re.split(r'[,|\n]+', content)
                
                for part in parts:
                    part = part.strip()
                    if part:
                        try:
                            results.append(int(part))
                        except ValueError:
                            print(f"警告：无法解析 '{part}'，已跳过")
            
            print(f"成功从文件 {file_path} 读取 {len(results)} 个练习结果")
            return results
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return None
    
    def judge(self, exercise: Exercise, practice_results: List[int]):
        if exercise.scale != len(practice_results):
            print(f"错误：练习题数量 ({exercise.scale}) 与练习结果数量 ({len(practice_results)}) 不一致")
            return False
        
        self.correct = 0
        self.wrong = 0
        self.checking_list = []
        
        for i, (eq, result) in enumerate(zip(exercise.operations, practice_results)):
            if result == -1:
                self.wrong += 1
                self.checking_list.append(-1)
            elif result == eq.calculate_result():
                self.correct += 1
                self.checking_list.append(1)
            else:
                self.wrong += 1
                self.checking_list.append(-1)
        
        return True
    
    def display_result(self):
        total = self.correct + self.wrong
        if total == 0:
            score = 0
        else:
            score = int((self.correct / total) * 100)
        
        print("\n===== 批改结果 =====")
        print(f"算式总数：{total}")
        print(f"正确：{self.correct}")
        print(f"错误：{self.wrong}")
        print(f"得分：{score}")
        print("=====================")
        
        return {
            'total': total,
            'correct': self.correct,
            'wrong': self.wrong,
            'score': score
        }
    
    def write_result_to_csv(self, exercise_file, practice_file):
        total = self.correct + self.wrong
        if total == 0:
            score = 0
        else:
            score = int((self.correct / total) * 100)
        
        output_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_checking"
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(practice_file))[0]
        result_filename = os.path.join(output_dir, f"checking_result_{base_name}.csv")
        
        try:
            with open(result_filename, 'w', encoding='utf-8') as f:
                f.write(f"答案：{base_name}\n")
                f.write(f"算式总数：{total}\n")
                f.write(f"正确：{self.correct}\n")
                f.write(f"错误：{self.wrong}\n")
                f.write(f"得分：{score}\n")
            
            print(f"批改结果已保存到文件: {result_filename}")
            return True
        except Exception as e:
            print(f"写入文件时发生错误: {e}")
            return False
