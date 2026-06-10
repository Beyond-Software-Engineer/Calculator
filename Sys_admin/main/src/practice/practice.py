import re
import os
import sys
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Practice:
    def __init__(self):
        pass
    
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
