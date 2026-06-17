#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将Practices_OL文件夹中的数据规范化处理并插入数据库
"""

import os
import sys
import re
from collections import defaultdict

# 添加数据库模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'main', 'src'))
from database.db_manager import db_manager

class DataImporter:
    """数据导入器"""
    
    def __init__(self, base_path):
        self.base_path = base_path
        self.practice_dir = os.path.join(base_path, 'practice')
        self.answer_dir = os.path.join(base_path, 'practice_answer')
        self.result_dir = os.path.join(base_path, 'practice_result')
        self.checking_dir = os.path.join(base_path, 'practice_checking')
        
        # 记录统计信息
        self.stats = {
            'total_files': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        # 文件类型映射
        self.file_type_map = {
            'addition': 'addition',
            'subtraction': 'subtraction',
            'mixed': 'mixed'
        }
    
    def parse_filename(self, filename):
        """解析文件名，提取关键信息"""
        # 匹配模式：{type}_exercise_{count}_{num}.csv 或 {type}_practice_{count}_{num}.csv
        patterns = [
            r'^(\w+)_exercise_(\d+)_(\d+)\.csv$',
            r'^(\w+)_practice_(\d+)_(\d+)\.csv$',
            r'^(\w+)_exercise_(\d+)_test\.csv$',
            r'^(\w+)_exercise_(\d+)\.csv$',
            r'^(\w+)_practice_(\d+)\.csv$',
            r'^checking_result_(\w+)_practice_(\d+)_(\d+)\.csv$',
            r'^online_result_(\w+)_exercise_(\d+)_(\d+)\.csv$',
            r'^online_result_(\w+)_exercise_(\d+)_test\.csv$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    file_type = groups[0]
                    question_count = int(groups[1])
                    num = groups[2] if len(groups) > 2 else '000'
                    return {
                        'type': self.file_type_map.get(file_type, 'mixed'),
                        'question_count': question_count,
                        'num': num,
                        'original_type': file_type
                    }
        
        # 默认返回
        return {
            'type': 'mixed',
            'question_count': 0,
            'num': '000',
            'original_type': 'unknown'
        }
    
    def parse_checking_filename(self, filename):
        """解析检查结果文件名"""
        patterns = [
            r'^checking_result_(\w+)_practice_(\d+)_(\d+)\.csv$',
            r'^online_result_(\w+)_exercise_(\d+)_(\d+)\.csv$',
            r'^online_result_(\w+)_exercise_(\d+)_test\.csv$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                groups = match.groups()
                return {
                    'type': self.file_type_map.get(groups[0], 'mixed'),
                    'question_count': int(groups[1]),
                    'num': groups[2] if len(groups) > 2 else 'test',
                    'is_online': filename.startswith('online_')
                }
        
        return None
    
    def read_file_content(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                return content
            except Exception as e2:
                self.log_error(f"读取文件失败 {file_path}: {str(e2)}")
                return None
    
    def log_error(self, message):
        """记录错误信息"""
        self.stats['errors'].append(message)
        print(f"❌ {message}")
    
    def log_success(self, message):
        """记录成功信息"""
        print(f"✅ {message}")
    
    def import_practice_files(self):
        """导入练习文件"""
        print("\n" + "="*60)
        print("导入练习文件 (practice)")
        print("="*60)
        
        if not os.path.exists(self.practice_dir):
            self.log_error(f"目录不存在: {self.practice_dir}")
            return
        
        files = [f for f in os.listdir(self.practice_dir) if f.endswith('.csv')]
        print(f"发现 {len(files)} 个练习文件")
        
        for filename in files:
            self.stats['total_files'] += 1
            file_path = os.path.join(self.practice_dir, filename)
            
            try:
                # 解析文件名
                info = self.parse_filename(filename)
                
                # 读取文件内容
                content = self.read_file_content(file_path)
                if content is None:
                    self.stats['failed'] += 1
                    continue
                
                # 提取题目数量（如果解析失败，从内容中估算）
                if info['question_count'] == 0:
                    lines = content.strip().split('\n')
                    info['question_count'] = len([l for l in lines if l.strip()])
                
                # 插入数据库
                file_id = db_manager.insert_exercise_file(
                    filename=filename,
                    file_type=info['type'],
                    question_count=info['question_count'],
                    file_suffix='csv',
                    content=content,
                    file_path=file_path
                )
                
                if file_id > 0:
                    self.stats['success'] += 1
                    self.log_success(f"插入练习文件: {filename} (ID: {file_id})")
                else:
                    self.stats['failed'] += 1
                    self.log_error(f"插入练习文件失败: {filename}")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.log_error(f"处理练习文件异常 {filename}: {str(e)}")
    
    def import_answer_files(self):
        """导入答案文件"""
        print("\n" + "="*60)
        print("导入答案文件 (practice_answer)")
        print("="*60)
        
        if not os.path.exists(self.answer_dir):
            self.log_error(f"目录不存在: {self.answer_dir}")
            return
        
        files = [f for f in os.listdir(self.answer_dir) if f.endswith('.csv')]
        print(f"发现 {len(files)} 个答案文件")
        
        # 获取所有练习文件用于关联
        exercises = db_manager.get_all_exercises()
        exercise_map = {e['filename']: e['id'] for e in exercises}
        
        # 获取已存在的答案文件
        existing_answers = db_manager.execute_query("SELECT filename FROM answer_files")
        existing_set = {a['filename'] for a in existing_answers}
        
        for filename in files:
            self.stats['total_files'] += 1
            file_path = os.path.join(self.answer_dir, filename)
            
            try:
                # 读取文件内容
                content = self.read_file_content(file_path)
                if content is None:
                    self.stats['failed'] += 1
                    continue
                
                # 尝试找到关联的练习ID
                # 答案文件名和练习文件名相同
                exercise_id = exercise_map.get(filename)
                
                if exercise_id is None:
                    # 尝试根据文件名模式匹配
                    base_name = filename.replace('_answer', '').replace('answer_', '')
                    exercise_id = exercise_map.get(base_name)
                
                if exercise_id is None:
                    # 如果找不到关联，尝试插入不关联的记录
                    exercise_id = 0
                    self.log_error(f"无法找到关联的练习文件: {filename}")
                
                # 插入数据库
                file_id = db_manager.insert_answer_file(
                    exercise_id=exercise_id,
                    filename=filename,
                    content=content,
                    file_path=file_path
                )
                
                # 检查是否已存在或成功插入
                if filename in existing_set:
                    self.stats['success'] += 1
                    self.log_success(f"答案文件已存在（已更新）: {filename}")
                elif file_id > 0:
                    self.stats['success'] += 1
                    self.log_success(f"插入答案文件: {filename} (ID: {file_id}, 关联练习ID: {exercise_id})")
                else:
                    self.stats['failed'] += 1
                    self.log_error(f"插入答案文件失败: {filename}")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.log_error(f"处理答案文件异常 {filename}: {str(e)}")
    
    def import_result_files(self):
        """导入练习结果文件"""
        print("\n" + "="*60)
        print("导入练习结果文件 (practice_result)")
        print("="*60)
        
        if not os.path.exists(self.result_dir):
            self.log_error(f"目录不存在: {self.result_dir}")
            return
        
        files = [f for f in os.listdir(self.result_dir) if f.endswith('.csv')]
        print(f"发现 {len(files)} 个练习结果文件")
        
        # 获取所有练习文件用于关联
        exercises = db_manager.get_all_exercises()
        exercise_map = {e['filename']: e['id'] for e in exercises}
        
        # 获取已存在的练习结果文件
        existing_results = db_manager.execute_query("SELECT filename FROM practice_results")
        existing_set = {r['filename'] for r in existing_results}
        
        for filename in files:
            self.stats['total_files'] += 1
            file_path = os.path.join(self.result_dir, filename)
            
            try:
                # 读取文件内容
                content = self.read_file_content(file_path)
                if content is None:
                    self.stats['failed'] += 1
                    continue
                
                # 尝试找到关联的练习ID
                # 将practice替换为exercise
                exercise_filename = filename.replace('practice', 'exercise')
                exercise_id = exercise_map.get(exercise_filename)
                
                if exercise_id is None:
                    # 尝试精确匹配
                    exercise_id = exercise_map.get(filename)
                
                if exercise_id is None:
                    # 创建虚拟练习记录
                    self.log_error(f"无法找到关联的练习文件，创建虚拟记录: {filename}")
                    info = self.parse_filename(filename)
                    virtual_id = db_manager.insert_exercise_file(
                        filename=f"virtual_{filename}",
                        file_type=info['type'],
                        question_count=info['question_count'],
                        file_suffix='csv',
                        content='',
                        file_path=''
                    )
                    exercise_id = virtual_id
                    exercise_map[exercise_filename] = virtual_id
                
                # 插入数据库
                file_id = db_manager.insert_practice_result(
                    exercise_id=exercise_id,
                    filename=filename,
                    content=content,
                    file_path=file_path
                )
                
                # 检查是否已存在或成功插入
                if filename in existing_set:
                    self.stats['success'] += 1
                    self.log_success(f"练习结果文件已存在（已更新）: {filename}")
                elif file_id > 0:
                    self.stats['success'] += 1
                    self.log_success(f"插入练习结果文件: {filename} (ID: {file_id}, 关联练习ID: {exercise_id})")
                else:
                    self.stats['failed'] += 1
                    self.log_error(f"插入练习结果文件失败: {filename}")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.log_error(f"处理练习结果文件异常 {filename}: {str(e)}")
    
    def import_checking_files(self):
        """导入检查结果文件"""
        print("\n" + "="*60)
        print("导入检查结果文件 (practice_checking)")
        print("="*60)
        
        if not os.path.exists(self.checking_dir):
            self.log_error(f"目录不存在: {self.checking_dir}")
            return
        
        files = [f for f in os.listdir(self.checking_dir) if f.endswith('.csv')]
        print(f"发现 {len(files)} 个检查结果文件")
        
        # 获取所有练习结果文件用于关联
        results = db_manager.execute_query("SELECT id, filename FROM practice_results")
        result_map = {r['filename']: r['id'] for r in results}
        
        # 获取所有练习文件（用于创建虚拟练习结果）
        exercises = db_manager.get_all_exercises()
        exercise_map = {e['filename']: e['id'] for e in exercises}
        
        for filename in files:
            self.stats['total_files'] += 1
            file_path = os.path.join(self.checking_dir, filename)
            
            try:
                # 读取文件内容
                content = self.read_file_content(file_path)
                if content is None:
                    self.stats['failed'] += 1
                    continue
                
                # 解析检查结果文件名
                info = self.parse_checking_filename(filename)
                
                # 尝试找到关联的练习结果ID
                practice_filename = None
                if info:
                    # 构建对应的practice文件名
                    if filename.startswith('checking_result_'):
                        practice_filename = filename.replace('checking_result_', '')
                    elif filename.startswith('online_result_'):
                        practice_filename = filename.replace('online_result_', '').replace('exercise', 'practice')
                
                practice_id = None
                if practice_filename:
                    practice_id = result_map.get(practice_filename)
                
                if practice_id is None:
                    # 尝试其他匹配方式
                    base_name = filename.replace('checking_result_', '').replace('online_result_', '')
                    practice_filename_candidate = base_name.replace('exercise', 'practice')
                    practice_id = result_map.get(practice_filename_candidate)
                
                if practice_id is None:
                    # 创建虚拟练习结果记录
                    self.log_error(f"无法找到关联的练习结果文件，创建虚拟记录: {filename}")
                    # 先尝试找到练习ID
                    base_name = filename.replace('checking_result_', '').replace('online_result_', '')
                    exercise_filename = base_name.replace('practice', 'exercise')
                    exercise_id = exercise_map.get(exercise_filename)
                    
                    if exercise_id is None:
                        # 创建虚拟练习记录
                        parse_info = self.parse_filename(base_name)
                        virtual_exercise_id = db_manager.insert_exercise_file(
                            filename=f"virtual_exercise_{base_name}",
                            file_type=parse_info['type'],
                            question_count=parse_info['question_count'],
                            file_suffix='csv',
                            content='',
                            file_path=''
                        )
                        exercise_id = virtual_exercise_id
                        exercise_map[exercise_filename] = virtual_exercise_id
                    
                    # 创建虚拟练习结果记录
                    virtual_practice_id = db_manager.insert_practice_result(
                        exercise_id=exercise_id,
                        filename=f"virtual_{practice_filename}" if practice_filename else f"virtual_{filename}",
                        content='',
                        file_path=''
                    )
                    practice_id = virtual_practice_id
                    result_map[practice_filename] = virtual_practice_id
                
                # 从内容中解析统计信息
                total_count = 0
                correct_count = 0
                wrong_count = 0
                score = 0
                
                try:
                    lines = content.strip().split('\n')
                    total_count = len([l for l in lines if l.strip()])
                    # 简单统计（假设每行是一个答题结果）
                    for line in lines:
                        if line.strip():
                            parts = line.strip().split(',')
                            if len(parts) >= 2:
                                try:
                                    if parts[-1] == '正确' or parts[-1] == '1' or int(parts[-1]) > 0:
                                        correct_count += 1
                                    else:
                                        wrong_count += 1
                                except:
                                    pass
                    score = int((correct_count / max(total_count, 1)) * 100)
                except Exception as e:
                    self.log_error(f"解析检查结果统计信息失败 {filename}: {str(e)}")
                
                # 插入数据库

                file_id = db_manager.insert_checking_result(
                    practice_id=practice_id,
                    filename=filename,
                    total_count=total_count,
                    correct_count=correct_count,
                    wrong_count=wrong_count,
                    score=score,
                    content=content,
                    file_path=file_path
                )
                
                if file_id > 0:
                    self.stats['success'] += 1
                    self.log_success(f"插入检查结果文件: {filename} (ID: {file_id}, 关联结果ID: {practice_id})")
                else:
                    self.stats['failed'] += 1
                    self.log_error(f"插入检查结果文件失败: {filename}")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.log_error(f"处理检查结果文件异常 {filename}: {str(e)}")
    
    def validate_data(self):
        """验证数据完整性和准确性"""
        print("\n" + "="*60)
        print("验证数据完整性和准确性")
        print("="*60)
        
        # 统计数据库中的记录数
        tables = [
            ('exercise_files', '练习文件'),
            ('answer_files', '答案文件'),
            ('practice_results', '练习结果文件'),
            ('checking_results', '检查结果文件')
        ]
        
        total_records = 0
        for table, desc in tables:
            try:
                result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                count = result[0]['count'] if result else 0
                total_records += count
                print(f"✅ {desc} 表记录数: {count}")
            except Exception as e:
                print(f"❌ 查询 {desc} 表失败: {str(e)}")
        
        # 检查数据完整性约束
        print("\n检查数据完整性约束:")
        
        # 检查练习文件是否都有file_path
        try:
            result = db_manager.execute_query("SELECT COUNT(*) as count FROM exercise_files WHERE file_path IS NULL")
            count = result[0]['count'] if result else 0
            if count == 0:
                print("✅ 所有练习文件都有文件路径")
            else:
                print(f"⚠️  {count} 个练习文件缺少文件路径")
        except Exception as e:
            print(f"❌ 检查练习文件路径失败: {str(e)}")
        
        # 检查关联完整性
        try:
            result = db_manager.execute_query("SELECT COUNT(*) as count FROM answer_files WHERE exercise_id = 0")
            count = result[0]['count'] if result else 0
            if count == 0:
                print("✅ 所有答案文件都正确关联到练习")
            else:
                print(f"⚠️  {count} 个答案文件未关联到练习")
        except Exception as e:
            print(f"❌ 检查答案文件关联失败: {str(e)}")
        
        print(f"\n📊 数据库总记录数: {total_records}")
        
        return True
    
    def run(self):
        """执行完整的导入流程"""
        print("="*60)
        print("开始导入Practices_OL文件夹数据")
        print("="*60)
        print(f"基础路径: {self.base_path}")
        
        # 确保数据库表存在
        print("\n初始化数据库表...")
        if db_manager.create_tables():
            print("✅ 数据库表初始化成功")
        else:
            print("❌ 数据库表初始化失败")
            return False
        
        # 导入各类文件
        self.import_practice_files()
        self.import_answer_files()
        self.import_result_files()
        self.import_checking_files()
        
        # 验证数据
        self.validate_data()
        
        # 输出统计报告
        print("\n" + "="*60)
        print("导入统计报告")
        print("="*60)
        print(f"📁 处理文件总数: {self.stats['total_files']}")
        print(f"✅ 成功插入: {self.stats['success']}")
        print(f"❌ 插入失败: {self.stats['failed']}")
        print(f"📊 成功率: {((self.stats['success'] / max(self.stats['total_files'], 1)) * 100):.2f}%")
        
        if self.stats['errors']:
            print("\n❌ 错误详情:")
            for i, error in enumerate(self.stats['errors'], 1):
                print(f"  {i}. {error}")
        
        print("\n" + "="*60)
        print("数据导入完成")
        print("="*60)
        
        return self.stats['failed'] == 0

def main():
    """主函数"""
    base_path = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL"
    
    if not os.path.exists(base_path):
        print(f"错误: 路径不存在: {base_path}")
        sys.exit(1)
    
    # 检查数据库连接
    if not db_manager.is_connected():
        print("错误: 数据库未连接，请检查数据库配置")
        sys.exit(1)
    
    print("✅ 数据库连接成功")
    
    # 创建导入器并执行
    importer = DataImporter(base_path)
    success = importer.run()
    
    if success:
        print("\n🎉 数据导入全部成功！")
        sys.exit(0)
    else:
        print("\n⚠️  数据导入完成，但存在失败记录")
        sys.exit(1)

if __name__ == "__main__":
    main()