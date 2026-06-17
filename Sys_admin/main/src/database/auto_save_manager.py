"""
自动存储管理器
功能：监测文件变化并自动存储至数据库
"""
import os
import time
import threading
from typing import Callable, Optional, Dict, List
from datetime import datetime

class AutoSaveManager:
    """文件自动存储管理器"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AutoSaveManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._monitoring = False
        self._monitor_thread = None
        self._file_records: Dict[str, float] = {}  # 文件路径: 最后修改时间
        self._callbacks: List[Callable] = []
        self._db_callbacks: List[Callable] = []  # 数据库操作回调
        self._monitored_dirs = [
            r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice",
            r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer",
            r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result",
            r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\checking_result"
        ]
        self._last_scan_time = time.time()
        print(f"[AutoSaveManager] 自动存储管理器初始化完成")
        print(f"[AutoSaveManager] 监测目录: {len(self._monitored_dirs)} 个")
    
    def add_callback(self, callback: Callable[[str, str], None]):
        """添加文件变化回调函数
        
        Args:
            callback: 回调函数，参数为 (file_type, file_path)
                     file_type: 'exercise', 'answer', 'practice', 'checking'
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            print(f"[AutoSaveManager] 已添加回调函数")
    
    def add_db_callback(self, callback: Callable[[str, str], None]):
        """添加数据库操作回调函数
        
        Args:
            callback: 回调函数，参数为 (file_type, file_path)
                     file_type: 'exercise', 'answer', 'practice', 'checking'
        """
        if callback not in self._db_callbacks:
            self._db_callbacks.append(callback)
            print(f"[AutoSaveManager] 已添加数据库回调函数")
    
    def remove_callback(self, callback: Callable):
        """移除回调函数"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def _get_file_type(self, file_path: str) -> Optional[str]:
        """根据文件路径判断文件类型"""
        if 'practice_answer' in file_path:
            return 'answer'
        elif 'practice_result' in file_path:
            return 'practice'
        elif 'checking_result' in file_path:
            return 'checking'
        elif 'practice' in file_path:
            return 'exercise'
        return None
    
    def _scan_directory(self, directory: str) -> List[Dict]:
        """扫描目录下的所有文件"""
        files = []
        if not os.path.exists(directory):
            return files
            
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.csv'):
                    file_path = os.path.join(directory, filename)
                    try:
                        mtime = os.path.getmtime(file_path)
                        files.append({
                            'path': file_path,
                            'name': filename,
                            'mtime': mtime,
                            'type': self._get_file_type(file_path)
                        })
                    except Exception as e:
                        print(f"[AutoSaveManager] 获取文件信息失败 {file_path}: {e}")
        except Exception as e:
            print(f"[AutoSaveManager] 扫描目录失败 {directory}: {e}")
            
        return files
    
    def _notify_callbacks(self, file_type: str, file_path: str):
        """通知所有回调函数"""
        # 通知通用回调
        for callback in self._callbacks:
            try:
                callback(file_type, file_path)
            except Exception as e:
                print(f"[AutoSaveManager] 回调函数执行失败: {e}")
        
        # 通知数据库回调
        for callback in self._db_callbacks:
            try:
                callback(file_type, file_path)
            except Exception as e:
                print(f"[AutoSaveManager] 数据库回调函数执行失败: {e}")
    
    def _default_db_callback(self, file_type: str, file_path: str):
        """默认的数据库回调函数，自动存储文件到数据库"""
        try:
            from database.db_manager import db_manager
            
            # 检查数据库连接
            if not db_manager.is_connected():
                return
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path)
            
            if file_type == 'exercise':
                # 习题文件
                file_type_db = 'mixed'
                if 'addition' in filename:
                    file_type_db = 'addition'
                elif 'subtraction' in filename:
                    file_type_db = 'subtraction'
                
                # 解析题目数量
                import re
                match = re.search(r'_(\d+)_', filename)
                question_count = int(match.group(1)) if match else 0
                
                file_id = db_manager.insert_exercise_file(
                    filename=filename,
                    file_type=file_type_db,
                    question_count=question_count,
                    file_suffix=str(question_count),
                    content=content,
                    file_path=file_path
                )
                
                if file_id > 0:
                    print(f"[自动存储] ✓ 习题文件已保存: {filename} (ID: {file_id})")
                    
            elif file_type == 'answer':
                # 答案文件
                # 查找对应的练习文件
                exercise_name = filename.replace('practice_answer', 'practice')
                exercise = db_manager.get_exercise_by_filename(exercise_name.replace('_answer', ''))
                
                if not exercise:
                    # 尝试其他匹配方式
                    exercises = db_manager.execute_query(
                        "SELECT id FROM exercise_files WHERE filename LIKE %s",
                        (f"%{filename.split('_')[-1].replace('.csv', '')}%",)
                    )
                    if exercises:
                        exercise_id = exercises[0]['id']
                    else:
                        print(f"[自动存储] ✗ 未找到对应的练习文件: {exercise_name}")
                        return
                else:
                    exercise_id = exercise['id']
                
                answer_id = db_manager.insert_answer_file(
                    exercise_id=exercise_id,
                    filename=filename,
                    content=content,
                    file_path=file_path
                )
                
                if answer_id > 0:
                    print(f"[自动存储] ✓ 答案文件已保存: {filename} (ID: {answer_id})")
                    
            elif file_type == 'practice':
                # 练习结果文件
                # 查找对应的练习文件
                exercise_name = filename.replace('practice', 'exercise')
                exercise = db_manager.get_exercise_by_filename(exercise_name)
                
                if not exercise:
                    exercises = db_manager.execute_query(
                        "SELECT id FROM exercise_files WHERE filename LIKE %s",
                        (f"%{filename.split('_')[-1].replace('.csv', '')}%",)
                    )
                    if exercises:
                        exercise_id = exercises[0]['id']
                    else:
                        print(f"[自动存储] ✗ 未找到对应的练习文件: {exercise_name}")
                        return
                else:
                    exercise_id = exercise['id']
                
                practice_id = db_manager.insert_practice_result(
                    exercise_id=exercise_id,
                    filename=filename,
                    content=content,
                    file_path=file_path
                )
                
                if practice_id > 0:
                    print(f"[自动存储] ✓ 练习结果已保存: {filename} (ID: {practice_id})")
                    
            elif file_type == 'checking':
                # 批改结果文件
                # 解析批改结果信息
                import re
                total = correct = wrong = score = 0
                
                try:
                    # 简单解析文件内容获取批改信息
                    for line in content.split('\n'):
                        if '算式总数' in line:
                            match = re.search(r'(\d+)', line)
                            if match:
                                total = int(match.group(1))
                        elif '正确' in line:
                            match = re.search(r'(\d+)', line)
                            if match:
                                correct = int(match.group(1))
                        elif '错误' in line:
                            match = re.search(r'(\d+)', line)
                            if match:
                                wrong = int(match.group(1))
                        elif '得分' in line:
                            match = re.search(r'(\d+)', line)
                            if match:
                                score = int(match.group(1))
                except:
                    pass
                
                # 查找对应的练习结果
                practice_name = filename.replace('checking_result_', '')
                practices = db_manager.execute_query(
                    "SELECT id FROM practice_results WHERE filename LIKE %s",
                    (f"%{practice_name.split('_')[-1].replace('.csv', '')}%",)
                )
                
                practice_id = practices[0]['id'] if practices else 0
                
                checking_id = db_manager.insert_checking_result(
                    practice_id=practice_id,
                    filename=filename,
                    total_count=total,
                    correct_count=correct,
                    wrong_count=wrong,
                    score=score,
                    content=content,
                    file_path=file_path
                )
                
                if checking_id > 0:
                    print(f"[自动存储] ✓ 批改结果已保存: {filename} (ID: {checking_id})")
                    
        except Exception as e:
            print(f"[自动存储] ✗ 保存失败 {file_path}: {e}")
    
    def scan_and_notify(self):
        """扫描所有监测目录，检测新文件或修改的文件"""
        all_files = []
        
        for directory in self._monitored_dirs:
            files = self._scan_directory(directory)
            all_files.extend(files)
        
        # 检测新文件或修改的文件
        new_files = []
        for file_info in all_files:
            file_path = file_info['path']
            mtime = file_info['mtime']
            
            if file_path not in self._file_records:
                # 新文件
                new_files.append(file_info)
                self._file_records[file_path] = mtime
            elif mtime > self._file_records[file_path]:
                # 已修改的文件
                new_files.append(file_info)
                self._file_records[file_path] = mtime
        
        # 通知回调函数
        for file_info in new_files:
            if file_info['type']:
                print(f"[AutoSaveManager] 检测到文件变化: {file_info['type']} - {file_info['name']}")
                self._notify_callbacks(file_info['type'], file_info['path'])
        
        # 清理已删除的文件记录
        current_paths = {f['path'] for f in all_files}
        deleted_paths = set(self._file_records.keys()) - current_paths
        for path in deleted_paths:
            del self._file_records[path]
        
        return len(new_files)
    
    def start_monitoring(self, interval: float = 1.0):
        """开始文件监测
        
        Args:
            interval: 监测间隔（秒）
        """
        if self._monitoring:
            print("[AutoSaveManager] 已经在监测中")
            return
            
        # 添加默认的数据库回调函数
        self.add_db_callback(self._default_db_callback)
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self._monitor_thread.start()
        print(f"[AutoSaveManager] 开始文件监测，间隔: {interval}秒")
    
    def stop_monitoring(self):
        """停止文件监测"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
            self._monitor_thread = None
        print("[AutoSaveManager] 已停止文件监测")
    
    def _monitor_loop(self, interval: float):
        """监测循环"""
        # 初始化扫描
        self.scan_and_notify()
        
        while self._monitoring:
            time.sleep(interval)
            self.scan_and_notify()
    
    def is_monitoring(self) -> bool:
        """是否正在监测"""
        return self._monitoring
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'monitoring': self._monitoring,
            'monitored_dirs': len(self._monitored_dirs),
            'tracked_files': len(self._file_records)
        }


# 全局单例实例
auto_save_manager = AutoSaveManager()
