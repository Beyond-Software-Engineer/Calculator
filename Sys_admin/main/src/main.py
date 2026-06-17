import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.operation_base import OperationBase
from exercise.exercise import Exercise
from practice.judgement import Judgement
from database.db_manager import db_manager
from database.auto_save_manager import auto_save_manager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("100以内口算练习程序")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # 初始化数据库
        self._init_database()
        
        self.operation_base = OperationBase(100)
        self.operation_base.produce_addition_base()
        self.operation_base.produce_subtraction_base()
        self.operation_base.produce_mixed_base()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_styles()
        
        self.create_widgets()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """窗口关闭时的清理工作"""
        print("[MainApp] 正在停止文件自动存储监测...")
        auto_save_manager.stop_monitoring()
        self.root.destroy()
        
    def _init_database(self):
        """初始化数据库"""
        if db_manager.is_connected():
            db_manager.create_tables()
            print("[MainApp] 数据库初始化完成")
            
            # 启动自动存储管理器
            auto_save_manager.start_monitoring(interval=2.0)
            print("[MainApp] 文件自动存储监测已启动")
        else:
            print("[MainApp] 数据库未连接，自动存储功能不可用")
        
    def setup_styles(self):
        self.style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('SubTitle.TLabel', font=('微软雅黑', 12, 'bold'), foreground='#34495e')
        
        # 按钮样式 - 增强悬停和按下效果
        self.style.configure('Button.TButton', font=('微软雅黑', 11), padding=10, borderwidth=1)
        self.style.map('Button.TButton', 
                       background=[('active', '#3498db'), ('!active', '#2980b9'), ('hover', '#3a9fd6')],
                       foreground=[('active', 'white'), ('!active', 'white')],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # 输入框样式 - 增强焦点效果
        self.style.configure('Entry.TEntry', font=('微软雅黑', 12), padding=5)
        self.style.map('Entry.TEntry',
                       fieldbackground=[('focus', '#f0f8ff'), ('!focus', 'white')],
                       bordercolor=[('focus', '#3498db'), ('!focus', '#ccc')],
                       lightcolor=[('focus', '#3498db')],
                       darkcolor=[('focus', '#3498db')])
        
        self.style.configure('Treeview', font=('微软雅黑', 10))
        self.style.configure('Treeview.Heading', font=('微软雅黑', 11, 'bold'))
        
        # 标签框架样式
        self.style.configure('TLabelframe', borderwidth=2, relief=tk.GROOVE)
        self.style.configure('TLabelframe.Label', font=('微软雅黑', 12, 'bold'), foreground='#2c3e50')
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="100以内口算练习程序", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        buttons = [
            ("批量产生习题", self.open_batch_generate),
            ("随机产生习题", self.open_random_generate),
            ("离线操练习题", self.open_offline_practice),
            ("批量批改操练", self.open_judgement),
            ("联机操练习题", self.open_online_practice),
            ("数据管理", self.open_data_management)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style='Button.TButton')
            btn.pack(fill=tk.X, pady=5)
        
        # 状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        self.status_bar = ttk.Label(status_frame, text="准备就绪", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 自动存储状态标签
        self.auto_save_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN)
        self.auto_save_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 更新自动存储状态显示
        self._update_auto_save_status()
        
    def _update_auto_save_status(self):
        """更新自动存储状态显示"""
        if auto_save_manager.is_monitoring():
            stats = auto_save_manager.get_stats()
            self.auto_save_label.config(text=f"自动存储: ✓ ({stats['tracked_files']} 文件)")
        else:
            self.auto_save_label.config(text="自动存储: ✗")
        
        # 每5秒更新一次状态
        self.root.after(5000, self._update_auto_save_status)
        
    def update_status(self, text):
        self.status_bar.config(text=text)
        self.root.update_idletasks()
        
    def open_batch_generate(self):
        BatchGenerateDialog(self.root, self.operation_base, self.update_status)
        
    def open_random_generate(self):
        RandomGenerateDialog(self.root, self.operation_base, self.update_status)
        
    def open_offline_practice(self):
        OfflinePracticeDialog(self.root, self.operation_base, self.update_status)
        
    def open_judgement(self):
        JudgementDialog(self.root, self.update_status)
        
    def open_online_practice(self):
        OnlinePracticeDialog(self.root, self.update_status)
        
    def open_data_management(self):
        DataManagementDialog(self.root, self.update_status)

class BatchGenerateDialog:
    def __init__(self, parent, operation_base, update_status):
        self.parent = parent
        self.operation_base = operation_base
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("批量产生习题")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="批量产生习题", style='Title.TLabel').pack(pady=(0, 20))
        
        ttk.Label(frame, text="选择习题类型：", style='SubTitle.TLabel').pack(anchor=tk.W)
        self.exercise_type = ttk.Combobox(frame, values=["减法习题", "加法习题", "混合习题"], state="readonly")
        self.exercise_type.current(0)
        self.exercise_type.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="题目数量：", style='SubTitle.TLabel').pack(anchor=tk.W)
        self.question_count = ttk.Entry(frame)
        self.question_count.insert(0, "10")
        self.question_count.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="文件序号（不包含中文）：", style='SubTitle.TLabel').pack(anchor=tk.W)
        self.file_suffix = ttk.Entry(frame)
        self.file_suffix.insert(0, "001")
        self.file_suffix.pack(fill=tk.X, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="生成习题", command=self.generate, style='Button.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(button_frame, text="取消", command=self.dialog.destroy).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.result_text = tk.Text(frame, height=8, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def generate(self):
        try:
            count = int(self.question_count.get())
            suffix = self.file_suffix.get()
            
            if any('\u4e00' <= c <= '\u9fff' for c in suffix):
                messagebox.showerror("错误", "文件序号不允许包含中文")
                return
                
            exercise = Exercise(count)
            exercise_type = self.exercise_type.get()
            
            self.update_status("正在生成习题...")
            
            if exercise_type == "减法习题":
                exercise.write_csv_subtraction_exercise(count, suffix)
                self.result_text.insert(tk.END, f"已生成减法习题 {count} 道，文件序号: {suffix}\n")
            elif exercise_type == "加法习题":
                exercise.write_csv_addition_exercise(count, suffix)
                self.result_text.insert(tk.END, f"已生成加法习题 {count} 道，文件序号: {suffix}\n")
            else:
                exercise.write_csv_mixed_exercise(count, suffix)
                self.result_text.insert(tk.END, f"已生成混合习题 {count} 道，文件序号: {suffix}\n")
                
            self.result_text.insert(tk.END, "习题和答案文件已保存成功！\n")
            self.update_status("习题生成完成")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")

class RandomGenerateDialog:
    def __init__(self, parent, operation_base, update_status):
        self.parent = parent
        self.operation_base = operation_base
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("随机产生习题")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="随机产生习题", style='Title.TLabel').pack(pady=(0, 20))
        
        ttk.Label(frame, text="选择习题类型：", style='SubTitle.TLabel').pack(anchor=tk.W)
        self.exercise_type = ttk.Combobox(frame, values=["减法习题", "加法习题", "混合习题"], state="readonly")
        self.exercise_type.current(0)
        self.exercise_type.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="题目数量：", style='SubTitle.TLabel').pack(anchor=tk.W)
        self.question_count = ttk.Entry(frame)
        self.question_count.insert(0, "10")
        self.question_count.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame, text="生成习题", command=self.generate, style='Button.TButton').pack(fill=tk.X, pady=10)
        
        self.result_text = tk.Text(frame, height=20, wrap=tk.WORD, font=('微软雅黑', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="关闭", command=self.dialog.destroy).pack(fill=tk.X, pady=10)
        
    def generate(self):
        try:
            count = int(self.question_count.get())
            exercise = Exercise(count)
            exercise_type = self.exercise_type.get()
            
            self.update_status("正在随机生成习题...")
            
            if exercise_type == "减法习题":
                exercise.generate_substraction_exercise(self.operation_base, count)
            elif exercise_type == "加法习题":
                exercise.generate_addition_exercise(self.operation_base, count)
            else:
                exercise.generate_exercise(self.operation_base, count)
                
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"=== {exercise_type}（共{count}道）===\n\n")
            
            for i, eq in enumerate(exercise.operations, 1):
                self.result_text.insert(tk.END, f"{i}. {eq.as_string()}\n")
                
            self.update_status("随机习题生成完成")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")

class OfflinePracticeDialog:
    def __init__(self, parent, operation_base, update_status):
        self.parent = parent
        self.operation_base = operation_base
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("离线操练习题")
        self.dialog.geometry("700x700")  # 增加高度以支持全部显示模式
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.current_index = 0
        self.user_answers = []
        self.correct_count = 0
        self.start_time = 0
        self.timer_running = False
        self.elapsed_time = 0
        self.display_mode = 'single'  # 'single'=逐题显示, 'all'=全部显示
        self.answer_entries = []  # 全部显示模式的输入框列表
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="离线操练习题", style='Title.TLabel').pack(pady=(0, 20))
        
        # 配置区域
        config_frame = ttk.LabelFrame(frame, text="练习配置", padding="10")
        config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(config_frame, text="选择习题类型：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.exercise_type = ttk.Combobox(config_frame, values=["减法习题", "加法习题", "混合习题"], state="readonly", width=15)
        self.exercise_type.current(0)
        self.exercise_type.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="题目数量：").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.question_count = ttk.Entry(config_frame, width=15)
        self.question_count.insert(0, "10")
        self.question_count.grid(row=1, column=1, padx=5, pady=5)
        
        # 显示模式选择
        ttk.Label(config_frame, text="显示模式：").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.display_mode_var = tk.StringVar(value='single')
        display_mode_frame = ttk.Frame(config_frame)
        display_mode_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(display_mode_frame, text="逐题显示", variable=self.display_mode_var, value='single').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(display_mode_frame, text="全部显示", variable=self.display_mode_var, value='all').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(config_frame, text="开始练习", command=self.start_practice, style='Button.TButton').grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        # 练习区域（逐题显示模式）
        self.practice_frame_single = ttk.LabelFrame(frame, text="练习区域", padding="10")
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 状态栏
        status_frame = ttk.Frame(self.practice_frame_single)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(status_frame, text="进度: 0/0", font=('微软雅黑', 10))
        self.progress_label.pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(status_frame, text="用时: 00:00", font=('微软雅黑', 10))
        self.timer_label.pack(side=tk.RIGHT)
        
        # 题目显示
        self.question_label = ttk.Label(self.practice_frame_single, text="点击开始练习开始答题", font=('微软雅黑', 28), anchor=tk.CENTER)
        self.question_label.pack(pady=30, fill=tk.X)
        
        # 答案输入
        self.answer_entry = ttk.Entry(self.practice_frame_single, font=('微软雅黑', 24), justify=tk.CENTER)
        self.answer_entry.pack(fill=tk.X, pady=10, padx=50)
        self.answer_entry.bind('<Return>', self.check_answer)
        self.answer_entry.config(state=tk.DISABLED)
        
        # 结果反馈
        self.result_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 16))
        self.result_label.pack(pady=10)
        
        ttk.Button(self.practice_frame_single, text="提交答案", command=self.check_answer, style='Button.TButton').pack(fill=tk.X, pady=10, padx=50)
        
        # 结果汇总
        self.summary_text = tk.Text(self.practice_frame_single, height=8, wrap=tk.WORD, font=('微软雅黑', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # 全部显示模式的容器
        self.practice_frame_all = ttk.LabelFrame(frame, text="练习区域（全部显示）", padding="10")
        # 全部显示模式下的题目和答案容器（滚动）
        self.all_questions_frame = ttk.Frame(self.practice_frame_all)
        self.all_questions_frame.pack(fill=tk.BOTH, expand=True)
        
        # 重新练习按钮
        self.restart_button = ttk.Button(frame, text="重新练习", command=self.reset_practice, style='Button.TButton')
        self.restart_button.pack(fill=tk.X, pady=5)
        self.restart_button.config(state=tk.DISABLED)
        
    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"用时: {minutes:02d}:{seconds:02d}")
            self.dialog.after(1000, self.update_timer)
        
    def start_practice(self):
        try:
            count = int(self.question_count.get())
            if count <= 0 or count > 100:
                messagebox.showerror("错误", "题目数量应在1-100之间")
                return
                
            self.exercise = Exercise(count)
            exercise_type = self.exercise_type.get()
            self.display_mode = self.display_mode_var.get()
            
            self.update_status("正在生成习题...")
            
            if exercise_type == "减法习题":
                self.exercise.generate_substraction_exercise(self.operation_base, count)
            elif exercise_type == "加法习题":
                self.exercise.generate_addition_exercise(self.operation_base, count)
            else:
                self.exercise.generate_exercise(self.operation_base, count)
                
            self.current_index = 0
            self.user_answers = []
            self.correct_count = 0
            self.start_time = 0
            self.elapsed_time = 0
            self.timer_running = True
            self.update_timer()
            
            # 根据显示模式初始化不同的界面
            if self.display_mode == 'all':
                self._init_all_display_mode()
            else:
                self._init_single_display_mode()
            
            self.restart_button.config(state=tk.DISABLED)
            
            self.update_status("离线练习开始")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _init_single_display_mode(self):
        """初始化逐题显示模式 - 带平滑过渡效果"""
        # 隐藏全部显示模式，显示逐题显示模式
        self.practice_frame_all.pack_forget()
        
        # 重置练习区域内容
        for widget in self.practice_frame_single.winfo_children():
            widget.destroy()
        
        # 重新创建练习区域组件
        # 状态栏
        status_frame = ttk.Frame(self.practice_frame_single)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(status_frame, text="进度: 0/0", font=('微软雅黑', 10))
        self.progress_label.pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(status_frame, text="用时: 00:00", font=('微软雅黑', 10))
        self.timer_label.pack(side=tk.RIGHT)
        
        # 题目显示
        self.question_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 28), anchor=tk.CENTER)
        self.question_label.pack(pady=30, fill=tk.X)
        
        # 答案输入
        self.answer_entry = ttk.Entry(self.practice_frame_single, font=('微软雅黑', 24), justify=tk.CENTER, style='Entry.TEntry')
        self.answer_entry.pack(fill=tk.X, pady=10, padx=50)
        self.answer_entry.bind('<Return>', self.check_answer)
        
        # 结果反馈
        self.result_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 16))
        self.result_label.pack(pady=10)
        
        ttk.Button(self.practice_frame_single, text="提交答案", command=self.check_answer, style='Button.TButton').pack(fill=tk.X, pady=10, padx=50)
        
        # 结果汇总
        self.summary_text = tk.Text(self.practice_frame_single, height=8, wrap=tk.WORD, font=('微软雅黑', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # 平滑显示练习区域
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        self.practice_frame_single.update_idletasks()
        
        # 延迟显示，避免闪烁
        self.dialog.after(100, self.show_question)
    
    def _init_all_display_mode(self):
        """初始化全部显示模式 - 响应式布局"""
        # 隐藏逐题显示模式，显示全部显示模式
        self.practice_frame_single.pack_forget()
        self.practice_frame_all.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # 等待窗口初始化完成后再渲染
        self.dialog.update_idletasks()
        self.dialog.after(100, self._setup_all_mode_canvas)
    
    def _setup_all_mode_canvas(self):
        """设置全部显示模式的画布和题目渲染"""
        # 清空之前的题目和输入框
        for widget in self.all_questions_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 创建主容器
        container = ttk.Frame(self.all_questions_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # 创建带滚动条的画布
        canvas = tk.Canvas(container, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=5)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 保存scrollable_frame的引用，用于后续重绘
        self.all_scroll_frame = scrollable_frame
        self.all_canvas = canvas
        
        # 添加所有题目和输入框（响应式布局，每行根据窗口宽度自动调整）
        self._render_questions_grid_offline()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 记录初始宽度，用于检测窗口大小变化
        self._last_render_width = self.all_questions_frame.winfo_width()
        
        # 启动定时检查窗口大小的任务
        self._check_window_resize()
    
    def _check_window_resize(self):
        """定时检查窗口大小变化"""
        if not hasattr(self, 'all_questions_frame'):
            return
        
        # 获取当前容器宽度
        current_width = self.all_questions_frame.winfo_width()
        
        # 如果宽度变化超过阈值（50像素），则重绘
        if abs(current_width - getattr(self, '_last_render_width', 0)) > 50:
            # 只在容器真正可见且有效时才重绘
            if current_width > 50:
                self._last_render_width = current_width
                # 使用较长的延迟避免频繁重绘
                if not hasattr(self, '_resize_scheduled') or not self._resize_scheduled:
                    self._resize_scheduled = True
                    self.dialog.after(800, self._do_render_offline)
                return
        
        # 继续定时检查
        self.dialog.after(500, self._check_window_resize)
    
    def _do_render_offline(self):
        """执行离线模式题目渲染"""
        self._resize_scheduled = False
        self._render_questions_grid_offline()
        # 继续定时检查
        self.dialog.after(500, self._check_window_resize)
    
    def _render_questions_grid_offline(self):
        """渲染离线题目网格 - 根据窗口宽度自适应"""
        if not hasattr(self, 'all_scroll_frame') or not hasattr(self, 'exercise'):
            return
        
        # 检查 exercise 是否有效
        if not hasattr(self.exercise, 'operations') or not self.exercise.operations:
            return
        
        scrollable_frame = self.all_scroll_frame
        
        # 清空之前的题目
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 计算可用宽度（减去滚动条宽度和边距）
        # 使用 container 的宽度而不是窗口宽度
        container_width = self.all_questions_frame.winfo_width()
        if container_width < 100:
            container_width = 640  # 默认宽度
        
        # 减去内边距和滚动条占用的宽度
        available_width = container_width - 40  # 减去左右边距和滚动条
        
        # 每个题目单元最小宽度约150像素
        min_width_per_question = 150
        
        # 计算每行可以显示的题目数量
        questions_per_row = max(1, min(5, available_width // min_width_per_question))
        
        # 添加所有题目和输入框
        for i, op in enumerate(self.exercise.operations):
            # 计算行和列
            row = i // questions_per_row
            col = i % questions_per_row
            
            # 如果是新的一行，创建行框架
            if col == 0:
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, pady=3, padx=5)
            
            # 创建题目框架
            question_frame = ttk.Frame(row_frame, padding=3, relief=tk.GROOVE, borderwidth=1)
            question_frame.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
            
            # 题目标签
            question_label = ttk.Label(question_frame, 
                                      text=f"{i+1}. {op.as_string()}", 
                                      font=('微软雅黑', 12), 
                                      anchor=tk.W,
                                      padding=3)
            question_label.pack(side=tk.TOP, anchor=tk.W)
            
            # 答案输入框
            answer_entry = ttk.Entry(question_frame, 
                                     font=('微软雅黑', 12), 
                                     width=5, 
                                     justify=tk.CENTER)
            answer_entry.pack(side=tk.LEFT, padx=2, pady=2)
            answer_entry.bind('<Return>', lambda e, idx=i: self._focus_next_entry(idx))
            self.answer_entries.append(answer_entry)
            
            # 结果标签
            result_label = ttk.Label(question_frame, 
                                     text="", 
                                     font=('微软雅黑', 11, 'bold'), 
                                     width=8,
                                     anchor=tk.W)
            result_label.pack(side=tk.LEFT, padx=2)
            self.answer_entries[i].result_label = result_label
        
        # 添加提交按钮
        submit_frame = ttk.Frame(scrollable_frame)
        submit_frame.pack(fill=tk.X, pady=15)
        ttk.Button(submit_frame, text="提交所有答案", command=self._submit_all_answers, style='Button.TButton').pack(pady=10)
        
        # 更新画布滚动区域
        if hasattr(self, 'all_canvas'):
            self.all_canvas.update_idletasks()
            self.all_canvas.configure(scrollregion=self.all_canvas.bbox("all"))
    
    def _focus_next_entry(self, current_index):
        """跳转到下一个输入框"""
        if current_index < len(self.answer_entries) - 1:
            self.answer_entries[current_index + 1].focus()
    
    def _submit_all_answers(self):
        """提交全部答案"""
        self.user_answers = []
        self.correct_count = 0
        
        for i, entry in enumerate(self.answer_entries):
            try:
                user_answer = int(entry.get())
                self.user_answers.append(str(user_answer))
            except ValueError:
                self.user_answers.append("")
                user_answer = None
            
            eq = self.exercise.operations[i]
            correct_answer = eq.calculate_result()
            
            if user_answer == correct_answer:
                entry.result_label.config(text="✓ 正确", foreground="#00AA00", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#CCFFCC')  # 浅绿色背景
                self.correct_count += 1
            elif user_answer is None:
                entry.result_label.config(text=f"✗ 未作答", foreground="#FF8800", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#FFEEAA')  # 浅橙色背景
            else:
                entry.result_label.config(text=f"✗ {correct_answer}", foreground="#DD0000", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#FFCCCC')  # 浅红色背景
        
        # 禁用所有输入框
        for entry in self.answer_entries:
            entry.config(state=tk.DISABLED)
        
        # 完成练习
        self._finish_all_practice()
            
    def reset_practice(self):
        self.current_index = 0
        self.user_answers = []
        self.correct_count = 0
        self.elapsed_time = 0
        self.timer_running = False
        self.timer_label.config(text="用时: 00:00")
        self.progress_label.config(text="进度: 0/0")
        self.question_label.config(text="点击开始练习开始答题")
        self.result_label.config(text="")
        self.answer_entry.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state=tk.DISABLED)
        
        # 清空全部显示模式的内容
        for widget in self.all_questions_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 恢复显示逐题模式
        self.practice_frame_all.pack_forget()
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def show_question(self):
        if self.current_index >= len(self.exercise.operations):
            self.finish_practice()
            return
            
        eq = self.exercise.operations[self.current_index]
        total = len(self.exercise.operations)
        self.progress_label.config(text=f"进度: {self.current_index + 1}/{total}")
        self.question_label.config(text=f"{self.current_index + 1}. {eq.as_string()}")
        self.result_label.config(text="")
        self.answer_entry.config(state=tk.NORMAL)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
    def check_answer(self, event=None):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的数字答案")
            return
            
        eq = self.exercise.operations[self.current_index]
        correct_answer = eq.calculate_result()
        
        self.user_answers.append(str(user_answer))
        
        if user_answer == correct_answer:
            self.result_label.config(text="回答正确！", foreground="green")
            self.correct_count += 1
        else:
            self.result_label.config(text=f"回答错误！正确答案是 {correct_answer}", foreground="red")
            
        self.answer_entry.config(state=tk.DISABLED)
        self.current_index += 1
        
        self.dialog.after(800, self.show_question)
        
    def finish_practice(self):
        self.timer_running = False
        self.question_label.config(text="练习完成！")
        self.answer_entry.config(state=tk.DISABLED)
        
        total = len(self.exercise.operations)
        correct = self.correct_count
        wrong = total - correct
        accuracy = int((correct / total) * 100) if total > 0 else 0
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
        
        # 清空并重新创建结果展示区域
        for widget in self.practice_frame_single.winfo_children():
            widget.destroy()
        
        # 创建统计区域框架
        stats_frame = ttk.LabelFrame(self.practice_frame_single, text="练习统计", padding="15")
        stats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # 创建统计网格
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # 总题数
        ttk.Label(stats_grid, text="总题数", font=('微软雅黑', 10)).grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(total), font=('微软雅黑', 14, 'bold'), foreground='#2c3e50').grid(row=0, column=1, padx=10, pady=5)
        
        # 正确数
        ttk.Label(stats_grid, text="正确数", font=('微软雅黑', 10)).grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(correct), font=('微软雅黑', 14, 'bold'), foreground='#27ae60').grid(row=1, column=1, padx=10, pady=5)
        
        # 错误数
        ttk.Label(stats_grid, text="错误数", font=('微软雅黑', 10)).grid(row=2, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(wrong), font=('微软雅黑', 14, 'bold'), foreground='#e74c3c').grid(row=2, column=1, padx=10, pady=5)
        
        # 正确率
        ttk.Label(stats_grid, text="正确率", font=('微软雅黑', 10)).grid(row=3, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=f"{accuracy}%", font=('微软雅黑', 14, 'bold'), foreground='#3498db').grid(row=3, column=1, padx=10, pady=5)
        
        # 用时
        ttk.Label(stats_grid, text="用时", font=('微软雅黑', 10)).grid(row=4, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=time_str, font=('微软雅黑', 14, 'bold'), foreground='#9b59b6').grid(row=4, column=1, padx=10, pady=5)
        
        # 收集错题信息
        self.wrong_questions = []
        for i, (eq, user_answer) in enumerate(zip(self.exercise.operations, self.user_answers)):
            try:
                user_num = int(user_answer)
            except:
                user_num = "未答"
            correct_answer = eq.calculate_result()
            if user_num != correct_answer:
                self.wrong_questions.append({
                    'index': i + 1,
                    'question': eq.as_string(),
                    'user_answer': user_num,
                    'correct_answer': correct_answer
                })
        
        # 如果有错题，显示"查看错题"按钮
        if self.wrong_questions:
            ttk.Button(
                self.practice_frame_single, 
                text=f"查看错题 ({len(self.wrong_questions)} 道)", 
                command=self.show_wrong_questions,
                style='Button.TButton'
            ).pack(fill=tk.X, pady=10, padx=50)
        else:
            ttk.Label(self.practice_frame_single, text="🎉 太棒了！全部答对！", font=('微软雅黑', 16, 'bold'), foreground='#27ae60').pack(pady=20)
        
        # 保存练习结果到数据库
        try:
            exercise_type = self.exercise_type.get()
            type_map = {"减法习题": "subtraction", "加法习题": "addition", "混合习题": "mixed"}
            db_manager.insert_practice_record(
                exercise_type=type_map.get(exercise_type, "mixed"),
                total_count=total,
                correct_count=self.correct_count,
                duration=self.elapsed_time,
                answers=','.join(self.user_answers)
            )
            ttk.Label(self.practice_frame_single, text="✓ 练习记录已保存", font=('微软雅黑', 10), foreground='#27ae60').pack(pady=5)
        except Exception as e:
            print(f"保存练习记录失败: {e}")
        
        self.restart_button.config(state=tk.NORMAL)
        self.update_status("离线练习完成")
    
    def show_wrong_questions(self):
        """显示错题详情对话框"""
        if not hasattr(self, 'wrong_questions') or not self.wrong_questions:
            return
            
        wrong_dialog = tk.Toplevel(self.dialog)
        wrong_dialog.title("错题详情")
        wrong_dialog.geometry("600x500")
        wrong_dialog.transient(self.dialog)
        wrong_dialog.grab_set()
        
        frame = ttk.Frame(wrong_dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"共 {len(self.wrong_questions)} 道错题", 
                 font=('微软雅黑', 14, 'bold')).pack(pady=(0, 10))
        
        # 创建错题列表（可滚动）
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for wq in self.wrong_questions:
            q_frame = ttk.Frame(scrollable_frame, padding="5", relief=tk.RIDGE)
            q_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(q_frame, text=f"第{wq['index']}题: {wq['question']}", 
                     font=('微软雅黑', 12)).pack(anchor=tk.W)
            ttk.Label(q_frame, text=f"你的答案: {wq['user_answer']}", 
                     font=('微软雅黑', 11), foreground='red').pack(anchor=tk.W)
            ttk.Label(q_frame, text=f"正确答案: {wq['correct_answer']}", 
                     font=('微软雅黑', 11), foreground='green').pack(anchor=tk.W)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(frame, text="关闭", command=wrong_dialog.destroy, 
                  style='Button.TButton').pack(pady=10)
    
    def _finish_all_practice(self):
        """全部显示模式下的练习完成处理"""
        self.timer_running = False
        
        # 全部显示模式下，直接在输入框旁通过颜色标识反馈正确性
        # 不需要额外的统计信息显示
        
        # 显示简单的完成提示
        result_frame = ttk.Frame(self.all_questions_frame)
        result_frame.pack(fill=tk.X, pady=20)
        
        total = len(self.exercise.operations)
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
        
        result_label = ttk.Label(result_frame, text=f"练习完成！用时: {time_str}", 
                                font=('微软雅黑', 14, 'bold'))
        result_label.pack(pady=10)
        
        # 保存练习结果到数据库
        try:
            exercise_type = self.exercise_type.get()
            type_map = {"减法习题": "subtraction", "加法习题": "addition", "混合习题": "mixed"}
            db_manager.insert_practice_record(
                exercise_type=type_map.get(exercise_type, "mixed"),
                total_count=total,
                correct_count=self.correct_count,
                duration=self.elapsed_time,
                answers=','.join(self.user_answers)
            )
            
            saved_label = ttk.Label(result_frame, text="✓ 练习记录已保存", font=('微软雅黑', 10), foreground='green')
            saved_label.pack(pady=(10, 0))
        except Exception as e:
            print(f"保存练习记录失败: {e}")
        
        self.restart_button.config(state=tk.NORMAL)
        self.update_status("离线练习完成")

class JudgementDialog:
    def __init__(self, parent, update_status):
        self.parent = parent
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("批量批改操练")
        self.dialog.geometry("700x500")
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="批量批改操练", style='Title.TLabel').pack(pady=(0, 20))
        
        self.file_tree = ttk.Treeview(frame, columns=('name', 'exercise', 'answer'), show='headings')
        self.file_tree.heading('name', text='答题文件')
        self.file_tree.heading('exercise', text='习题状态')
        self.file_tree.heading('answer', text='答案状态')
        self.file_tree.column('name', width=250)
        self.file_tree.column('exercise', width=150)
        self.file_tree.column('answer', width=150)
        self.file_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.load_practice_files()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="开始批改", command=self.judge_selected, style='Button.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(button_frame, text="刷新列表", command=self.load_practice_files).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.result_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def load_practice_files(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        practice_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result"
        if not os.path.exists(practice_dir):
            return
            
        for f in sorted(os.listdir(practice_dir)):
            if f.endswith('.csv'):
                exercise_file = f.replace('_practice_', '_exercise_')
                answer_file = f.replace('_practice_', '_exercise_')
                
                exercise_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice", exercise_file)
                answer_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer", answer_file)
                
                exercise_status = "✓" if os.path.exists(exercise_path) else "✗"
                answer_status = "✓" if os.path.exists(answer_path) else "✗"
                
                self.file_tree.insert('', tk.END, values=(f, exercise_status, answer_status))
                
    def judge_selected(self):
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要批改的文件")
            return
            
        item = self.file_tree.item(selected[0])
        practice_filename = item['values'][0]
        
        practice_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_result", practice_filename)
        exercise_file = practice_filename.replace('_practice_', '_exercise_')
        exercise_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice", exercise_file)
        answer_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice_answer", exercise_file)
        
        if not os.path.exists(exercise_path):
            messagebox.showerror("错误", "未找到对应的习题文件")
            return
            
        if not os.path.exists(answer_path):
            messagebox.showerror("错误", "未找到对应的答案文件")
            return
            
        try:
            self.update_status("正在批改...")
            
            exercise = Exercise()
            if 'addition' in exercise_file.lower():
                exercise.read_csv_addition_exercise(exercise_path)
            elif 'subtraction' in exercise_file.lower():
                exercise.read_csv_subtraction_exercise(exercise_path)
            else:
                exercise.read_csv_mixed_exercise(exercise_path)
                
            judgement = Judgement()
            practice_results = judgement.read_csv_practice(practice_path)
            
            if practice_results is None:
                return
                
            if judgement.judge(exercise, practice_results):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"=== 批改结果 ===\n")
                self.result_text.insert(tk.END, f"习题文件: {exercise_file}\n")
                self.result_text.insert(tk.END, f"答题文件: {practice_filename}\n")
                self.result_text.insert(tk.END, f"总题数: {judgement.correct + judgement.wrong}\n")
                self.result_text.insert(tk.END, f"正确: {judgement.correct}\n")
                self.result_text.insert(tk.END, f"错误: {judgement.wrong}\n")
                score = int((judgement.correct / (judgement.correct + judgement.wrong)) * 100)
                self.result_text.insert(tk.END, f"得分: {score}\n")
                
                if messagebox.askyesno("保存", "是否保存批改结果？"):
                    judgement.write_result_to_csv(exercise_path, practice_path)
                    self.result_text.insert(tk.END, "\n批改结果已保存！")
                
            self.update_status("批改完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"批改失败: {str(e)}")

class OnlinePracticeDialog:
    def __init__(self, parent, update_status):
        self.parent = parent
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("联机操练习题")
        self.dialog.geometry("750x900")  # 增加高度以支持全部显示模式
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.current_index = 0
        self.user_answers = []
        self.correct_count = 0
        self.start_time = 0
        self.timer_running = False
        self.elapsed_time = 0
        self.equations = []
        self.selected_exercise = None
        self.display_mode = 'single'  # 'single'=逐题显示, 'all'=全部显示
        self.answer_entries = []  # 全部显示模式的输入框列表
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="联机操练习题", style='Title.TLabel').pack(pady=(0, 20))
        
        # 数据源选择
        source_frame = ttk.Frame(frame)
        source_frame.pack(fill=tk.X, pady=5)
        
        self.source_var = tk.StringVar(value='database')
        ttk.Radiobutton(source_frame, text="从数据库选择", variable=self.source_var, value='database', 
                        command=self.load_exercises).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(source_frame, text="从文件选择", variable=self.source_var, value='file', 
                        command=self.load_exercises).pack(side=tk.LEFT, padx=10)
        
        # 习题选择区域
        file_frame = ttk.LabelFrame(frame, text="选择习题", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="选择习题类型：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.exercise_type = ttk.Combobox(file_frame, values=["加法习题", "减法习题", "混合习题"], state="readonly", width=15)
        self.exercise_type.current(0)
        self.exercise_type.grid(row=0, column=1, padx=5, pady=5)
        self.exercise_type.bind('<<ComboboxSelected>>', lambda e: self.load_exercises())
        
        # 习题列表
        self.exercise_tree = ttk.Treeview(file_frame, columns=('name', 'type', 'count', 'created'), show='headings', height=6)
        self.exercise_tree.heading('name', text='文件名')
        self.exercise_tree.heading('type', text='类型')
        self.exercise_tree.heading('count', text='题数')
        self.exercise_tree.heading('created', text='创建时间')
        self.exercise_tree.column('name', width=250)
        self.exercise_tree.column('type', width=80)
        self.exercise_tree.column('count', width=60)
        self.exercise_tree.column('created', width=150)
        self.exercise_tree.grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Button(button_frame, text="刷新列表", command=self.load_exercises).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(button_frame, text="开始练习", command=self.start_practice, style='Button.TButton').pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # 显示模式选择
        display_mode_frame = ttk.Frame(frame)
        display_mode_frame.pack(fill=tk.X, pady=5)
        ttk.Label(display_mode_frame, text="显示模式：").pack(side=tk.LEFT, padx=(0, 10))
        self.display_mode_var = tk.StringVar(value='single')
        ttk.Radiobutton(display_mode_frame, text="逐题显示", variable=self.display_mode_var, value='single').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(display_mode_frame, text="全部显示", variable=self.display_mode_var, value='all').pack(side=tk.LEFT, padx=5)
        
        # 练习区域（逐题显示模式）
        self.practice_frame_single = ttk.LabelFrame(frame, text="练习区域", padding="10")
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 状态栏
        status_frame = ttk.Frame(self.practice_frame_single)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(status_frame, text="进度: 0/0", font=('微软雅黑', 10))
        self.progress_label.pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(status_frame, text="用时: 00:00", font=('微软雅黑', 10))
        self.timer_label.pack(side=tk.RIGHT)
        
        # 题目显示
        self.question_label = ttk.Label(self.practice_frame_single, text="请选择习题开始练习", font=('微软雅黑', 28), anchor=tk.CENTER)
        self.question_label.pack(pady=30, fill=tk.X)
        
        # 答案输入
        self.answer_entry = ttk.Entry(self.practice_frame_single, font=('微软雅黑', 24), justify=tk.CENTER)
        self.answer_entry.pack(fill=tk.X, pady=10, padx=50)
        self.answer_entry.bind('<Return>', self.check_answer)
        self.answer_entry.config(state=tk.DISABLED)
        
        # 结果反馈
        self.result_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 16))
        self.result_label.pack(pady=10)
        
        ttk.Button(self.practice_frame_single, text="提交答案", command=self.check_answer, style='Button.TButton').pack(fill=tk.X, pady=10, padx=50)
        
        # 结果汇总
        self.summary_text = tk.Text(self.practice_frame_single, height=8, wrap=tk.WORD, font=('微软雅黑', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # 全部显示模式的容器
        self.practice_frame_all = ttk.LabelFrame(frame, text="练习区域（全部显示）", padding="10")
        self.all_questions_frame = ttk.Frame(self.practice_frame_all)
        self.all_questions_frame.pack(fill=tk.BOTH, expand=True)
        
        # 重新练习按钮
        self.restart_button = ttk.Button(frame, text="重新选择习题", command=self.reset_practice, style='Button.TButton')
        self.restart_button.pack(fill=tk.X, pady=5)
        self.restart_button.config(state=tk.DISABLED)
        
        self.load_exercises()
        
    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"用时: {minutes:02d}:{seconds:02d}")
            self.dialog.after(1000, self.update_timer)
        
    def load_exercises(self):
        """从数据库或文件加载习题列表"""
        # 清空树视图
        for item in self.exercise_tree.get_children():
            self.exercise_tree.delete(item)
            
        source = self.source_var.get()
        exercise_type = self.exercise_type.get()
        type_prefix = ""
        if exercise_type == "加法习题":
            type_prefix = "addition"
        elif exercise_type == "减法习题":
            type_prefix = "subtraction"
        else:
            type_prefix = "mixed"
            
        type_map = {"addition": "加法", "subtraction": "减法", "mixed": "混合"}
        
        if source == 'database':
            # 从数据库加载
            try:
                if not db_manager.is_connected():
                    self.exercise_tree.insert('', tk.END, values=("数据库未连接", "-", "-", "-"))
                    return
                    
                exercises = db_manager.get_exercises_by_type(type_prefix)
                if not exercises:
                    self.exercise_tree.insert('', tk.END, values=("暂无数据", "-", "-", "-"))
                else:
                    for ex in exercises:
                        created_at = ex['created_at']
                        if isinstance(created_at, str):
                            created_str = created_at[:19] if created_at else "-"
                        else:
                            created_str = str(created_at)[:19] if created_at else "-"
                            
                        self.exercise_tree.insert('', tk.END, values=(
                            ex['filename'],
                            type_map.get(ex['file_type'], ex['file_type']),
                            ex['question_count'],
                            created_str
                        ))
            except Exception as e:
                error_msg = f"数据库加载失败: {str(e)}"
                print(error_msg)
                self.exercise_tree.insert('', tk.END, values=(error_msg, "-", "-", "-"))
        else:
            # 从文件加载
            practice_dir = r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice"
            if not os.path.exists(practice_dir):
                self.exercise_tree.insert('', tk.END, values=("目录不存在", "-", "-", "-"))
                return
                
            files = []
            for f in os.listdir(practice_dir):
                if f.endswith('.csv') and type_prefix in f.lower():
                    files.append(f)
            
            if not files:
                self.exercise_tree.insert('', tk.END, values=(f"未找到{exercise_type}文件", "-", "-", "-"))
            else:
                for f in sorted(files):
                    self.exercise_tree.insert('', tk.END, values=(f, type_map.get(type_prefix, type_prefix), "-", "-"))
                
    def get_exercise_content(self, filename, source='database'):
        """获取习题内容"""
        if source == 'database':
            # 从数据库获取内容
            exercise = db_manager.get_exercise_by_filename(filename)
            if exercise:
                # 优先从数据库读取内容
                if exercise.get('content'):
                    return exercise['content']
                # 如果数据库没有内容，尝试从文件路径读取
                elif exercise.get('file_path'):
                    return db_manager.load_file_content_by_path(exercise['file_path'])
            return None
        else:
            # 从文件读取
            file_path = os.path.join(r"e:\Desktop\Engineering\Experiment\Instance\Sys_admin\main\Practices_OL\practice", filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
            
    def parse_equation(self, eq_str):
        """解析算式字符串，返回正确答案"""
        eq_str = eq_str.strip()
        if '+' in eq_str:
            parts = eq_str.split('+')
            if len(parts) >= 2:
                try:
                    return int(parts[0].strip()) + int(parts[1].strip())
                except:
                    return None
        elif '-' in eq_str:
            parts = eq_str.split('-')
            if len(parts) >= 2:
                try:
                    return int(parts[0].strip()) - int(parts[1].strip())
                except:
                    return None
        return None
        
    def start_practice(self):
        selected = self.exercise_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择习题")
            return
            
        item = self.exercise_tree.item(selected[0])
        self.selected_exercise = item['values'][0]
        source = self.source_var.get()
        self.display_mode = self.display_mode_var.get()
        
        try:
            content = self.get_exercise_content(self.selected_exercise, source)
            if not content:
                messagebox.showerror("错误", "无法获取习题内容")
                return
                
            self.equations = []
            for line in content.strip().split('\n'):
                for eq_str in line.split(','):
                    eq_str = eq_str.strip()
                    if eq_str and (('+' in eq_str) or ('-' in eq_str)):
                        self.equations.append(eq_str)
            
            if not self.equations:
                messagebox.showerror("错误", "文件中未找到有效的算式")
                return
                
            self.current_index = 0
            self.user_answers = []
            self.correct_count = 0
            self.elapsed_time = 0
            self.timer_running = True
            self.update_timer()
            
            # 根据显示模式初始化不同的界面
            if self.display_mode == 'all':
                self._init_all_display_mode()
            else:
                self._init_single_display_mode()
            
            self.restart_button.config(state=tk.DISABLED)
            
            self.update_status(f"联机练习开始: {self.selected_exercise}")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载习题失败: {str(e)}")
    
    def _init_single_display_mode(self):
        """初始化逐题显示模式 - 带平滑过渡效果"""
        # 隐藏全部显示模式
        self.practice_frame_all.pack_forget()
        
        # 重置练习区域内容
        for widget in self.practice_frame_single.winfo_children():
            widget.destroy()
        
        # 重新创建练习区域组件
        # 状态栏
        status_frame = ttk.Frame(self.practice_frame_single)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(status_frame, text="进度: 0/0", font=('微软雅黑', 10))
        self.progress_label.pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(status_frame, text="用时: 00:00", font=('微软雅黑', 10))
        self.timer_label.pack(side=tk.RIGHT)
        
        # 题目显示
        self.question_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 28), anchor=tk.CENTER)
        self.question_label.pack(pady=30, fill=tk.X)
        
        # 答案输入
        self.answer_entry = ttk.Entry(self.practice_frame_single, font=('微软雅黑', 24), justify=tk.CENTER, style='Entry.TEntry')
        self.answer_entry.pack(fill=tk.X, pady=10, padx=50)
        self.answer_entry.bind('<Return>', self.check_answer)
        
        # 结果反馈
        self.result_label = ttk.Label(self.practice_frame_single, text="", font=('微软雅黑', 16))
        self.result_label.pack(pady=10)
        
        ttk.Button(self.practice_frame_single, text="提交答案", command=self.check_answer, style='Button.TButton').pack(fill=tk.X, pady=10, padx=50)
        
        # 结果汇总
        self.summary_text = tk.Text(self.practice_frame_single, height=8, wrap=tk.WORD, font=('微软雅黑', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # 平滑显示练习区域
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        self.practice_frame_single.update_idletasks()
        
        # 延迟显示，避免闪烁
        self.dialog.after(100, self.show_question)
    
    def _init_all_display_mode(self):
        """初始化全部显示模式 - 响应式布局"""
        self.practice_frame_single.pack_forget()
        self.practice_frame_all.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # 等待窗口初始化完成后再渲染
        self.dialog.update_idletasks()
        self.dialog.after(100, self._setup_all_mode_canvas)
    
    def _setup_all_mode_canvas(self):
        """设置全部显示模式的画布和题目渲染"""
        # 清空之前的题目和输入框
        for widget in self.all_questions_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 创建主容器
        container = ttk.Frame(self.all_questions_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # 创建带滚动条的画布
        canvas = tk.Canvas(container, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=5)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 保存scrollable_frame的引用，用于后续重绘
        self.all_scroll_frame = scrollable_frame
        self.all_canvas = canvas
        
        # 添加所有题目和输入框（响应式布局，每行根据窗口宽度自动调整）
        self._render_questions_grid()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 记录初始宽度，用于检测窗口大小变化
        self._last_render_width = self.all_questions_frame.winfo_width()
        
        # 启动定时检查窗口大小的任务
        self._check_window_resize_online()
    
    def _check_window_resize_online(self):
        """定时检查联机模式窗口大小变化"""
        if not hasattr(self, 'all_questions_frame'):
            return
        
        # 获取当前容器宽度
        current_width = self.all_questions_frame.winfo_width()
        
        # 如果宽度变化超过阈值（50像素），则重绘
        if abs(current_width - getattr(self, '_last_render_width', 0)) > 50:
            # 只在容器真正可见且有效时才重绘
            if current_width > 50:
                self._last_render_width = current_width
                # 使用较长的延迟避免频繁重绘
                if not hasattr(self, '_resize_scheduled') or not self._resize_scheduled:
                    self._resize_scheduled = True
                    self.dialog.after(800, self._do_render_online)
                return
        
        # 继续定时检查
        self.dialog.after(500, self._check_window_resize_online)
    
    def _do_render_online(self):
        """执行联机模式题目渲染"""
        self._resize_scheduled = False
        self._render_questions_grid()
        # 继续定时检查
        self.dialog.after(500, self._check_window_resize_online)
    
    def _render_questions_grid(self):
        """渲染联机题目网格 - 根据窗口宽度自适应"""
        if not hasattr(self, 'all_scroll_frame') or not hasattr(self, 'equations'):
            return
        
        # 检查 equations 是否有效
        if not self.equations:
            return
            
        scrollable_frame = self.all_scroll_frame
        
        # 清空之前的题目
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 计算可用宽度（减去滚动条宽度和边距）
        # 使用 container 的宽度而不是窗口宽度
        container_width = self.all_questions_frame.winfo_width()
        if container_width < 100:
            container_width = 640  # 默认宽度
        
        # 减去内边距和滚动条占用的宽度
        available_width = container_width - 40  # 减去左右边距和滚动条
        
        # 每个题目单元最小宽度约150像素
        min_width_per_question = 150
        
        # 计算每行可以显示的题目数量
        questions_per_row = max(1, min(5, available_width // min_width_per_question))
        
        # 添加所有题目和输入框
        for i, eq_str in enumerate(self.equations):
            # 计算行和列
            row = i // questions_per_row
            col = i % questions_per_row
            
            # 如果是新的一行，创建行框架
            if col == 0:
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, pady=3, padx=5)
            
            # 创建题目框架
            question_frame = ttk.Frame(row_frame, padding=3, relief=tk.GROOVE, borderwidth=1)
            question_frame.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
            
            # 题目标签
            question_label = ttk.Label(question_frame, 
                                      text=f"{i+1}. {eq_str}", 
                                      font=('微软雅黑', 12), 
                                      anchor=tk.W,
                                      padding=3)
            question_label.pack(side=tk.TOP, anchor=tk.W)
            
            # 答案输入框
            answer_entry = ttk.Entry(question_frame, 
                                     font=('微软雅黑', 12), 
                                     width=5, 
                                     justify=tk.CENTER)
            answer_entry.pack(side=tk.LEFT, padx=2, pady=2)
            answer_entry.bind('<Return>', lambda e, idx=i: self._focus_next_entry(idx))
            self.answer_entries.append(answer_entry)
            
            # 结果标签
            result_label = ttk.Label(question_frame, 
                                     text="", 
                                     font=('微软雅黑', 11, 'bold'), 
                                     width=8,
                                     anchor=tk.W)
            result_label.pack(side=tk.LEFT, padx=2)
            # 将结果标签附加到输入框对象上
            self.answer_entries[-1].result_label = result_label
        
        # 添加提交按钮
        submit_frame = ttk.Frame(scrollable_frame)
        submit_frame.pack(fill=tk.X, pady=10)
        ttk.Button(submit_frame, text="提交所有答案", command=self._submit_all_answers, style='Button.TButton').pack(pady=5)
        
        # 更新画布滚动区域
        if hasattr(self, 'all_canvas'):
            self.all_canvas.update_idletasks()
            self.all_canvas.configure(scrollregion=self.all_canvas.bbox("all"))
    
    def _focus_next_entry(self, current_index):
        """跳转到下一个输入框"""
        if current_index < len(self.answer_entries) - 1:
            self.answer_entries[current_index + 1].focus()
    
    def _submit_all_answers(self):
        """提交全部答案"""
        self.user_answers = []
        self.correct_count = 0
        
        for i, entry in enumerate(self.answer_entries):
            try:
                user_answer = int(entry.get())
                self.user_answers.append(str(user_answer))
            except ValueError:
                self.user_answers.append("")
                user_answer = None
            
            eq_str = self.equations[i]
            correct_answer = self.parse_equation(eq_str)
            
            if correct_answer is None:
                continue
                
            if user_answer == correct_answer:
                entry.result_label.config(text="✓ 正确", foreground="#00AA00", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#CCFFCC')  # 浅绿色背景
                self.correct_count += 1
            elif user_answer is None:
                entry.result_label.config(text=f"✗ 未作答", foreground="#FF8800", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#FFEEAA')  # 浅橙色背景
            else:
                entry.result_label.config(text=f"✗ {correct_answer}", foreground="#DD0000", font=('微软雅黑', 11, 'bold'))
                entry.config(background='#FFCCCC')  # 浅红色背景
        
        # 禁用所有输入框
        for entry in self.answer_entries:
            entry.config(state=tk.DISABLED)
        
        # 完成练习
        self._finish_all_practice()
    
    def _finish_all_practice(self):
        """全部显示模式下的练习完成处理"""
        self.timer_running = False
        
        # 全部显示模式下，直接在输入框旁通过颜色标识反馈正确性
        # 不需要额外的统计信息显示
        
        # 显示简单的完成提示
        result_frame = ttk.Frame(self.all_questions_frame)
        result_frame.pack(fill=tk.X, pady=20)
        
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
        
        result_label = ttk.Label(result_frame, text=f"练习完成！用时: {time_str}", 
                                font=('微软雅黑', 14, 'bold'))
        result_label.pack(pady=10)
        
        self.restart_button.config(state=tk.NORMAL)
        self.update_status("联机练习完成")
            
    def reset_practice(self):
        self.current_index = 0
        self.user_answers = []
        self.correct_count = 0
        self.elapsed_time = 0
        self.timer_running = False
        self.timer_label.config(text="用时: 00:00")
        self.progress_label.config(text="进度: 0/0")
        self.question_label.config(text="请选择习题开始练习")
        self.result_label.config(text="")
        self.answer_entry.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state=tk.DISABLED)
        
        # 清空全部显示模式的内容
        for widget in self.all_questions_frame.winfo_children():
            widget.destroy()
        self.answer_entries = []
        
        # 恢复显示逐题模式
        self.practice_frame_all.pack_forget()
        self.practice_frame_single.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.load_exercises()
        
    def show_question(self):
        if self.current_index >= len(self.equations):
            self.finish_practice()
            return
            
        eq_str = self.equations[self.current_index]
        total = len(self.equations)
        self.progress_label.config(text=f"进度: {self.current_index + 1}/{total}")
        self.question_label.config(text=f"{self.current_index + 1}. {eq_str}")
        self.result_label.config(text="")
        self.answer_entry.config(state=tk.NORMAL)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
    def check_answer(self, event=None):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的数字答案")
            return
            
        eq_str = self.equations[self.current_index]
        correct_answer = self.parse_equation(eq_str)
        
        if correct_answer is None:
            messagebox.showwarning("提示", "无法解析当前算式")
            return
            
        self.user_answers.append(str(user_answer))
        
        if user_answer == correct_answer:
            self.result_label.config(text="回答正确！", foreground="green")
            self.correct_count += 1
        else:
            self.result_label.config(text=f"回答错误！正确答案是 {correct_answer}", foreground="red")
            
        self.answer_entry.config(state=tk.DISABLED)
        self.current_index += 1
        
        self.dialog.after(800, self.show_question)
        
    def finish_practice(self):
        self.timer_running = False
        self.question_label.config(text="练习完成！")
        self.answer_entry.config(state=tk.DISABLED)
        
        total = len(self.equations)
        correct = self.correct_count
        wrong = total - correct
        accuracy = int((correct / total) * 100) if total > 0 else 0
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
        
        # 清空并重新创建结果展示区域
        for widget in self.practice_frame_single.winfo_children():
            widget.destroy()
        
        # 创建统计区域框架
        stats_frame = ttk.LabelFrame(self.practice_frame_single, text="练习统计", padding="15")
        stats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # 创建统计网格
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # 习题文件信息
        ttk.Label(stats_grid, text="习题文件", font=('微软雅黑', 10)).grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=self.selected_exercise, font=('微软雅黑', 11), foreground='#2c3e50').grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # 数据源
        ttk.Label(stats_grid, text="数据源", font=('微软雅黑', 10)).grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text='数据库' if self.source_var.get() == 'database' else '文件', font=('微软雅黑', 11), foreground='#2c3e50').grid(row=1, column=1, padx=10, pady=5)
        
        # 总题数
        ttk.Label(stats_grid, text="总题数", font=('微软雅黑', 10)).grid(row=2, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(total), font=('微软雅黑', 14, 'bold'), foreground='#2c3e50').grid(row=2, column=1, padx=10, pady=5)
        
        # 正确数
        ttk.Label(stats_grid, text="正确数", font=('微软雅黑', 10)).grid(row=3, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(correct), font=('微软雅黑', 14, 'bold'), foreground='#27ae60').grid(row=3, column=1, padx=10, pady=5)
        
        # 错误数
        ttk.Label(stats_grid, text="错误数", font=('微软雅黑', 10)).grid(row=4, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=str(wrong), font=('微软雅黑', 14, 'bold'), foreground='#e74c3c').grid(row=4, column=1, padx=10, pady=5)
        
        # 正确率
        ttk.Label(stats_grid, text="正确率", font=('微软雅黑', 10)).grid(row=5, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=f"{accuracy}%", font=('微软雅黑', 14, 'bold'), foreground='#3498db').grid(row=5, column=1, padx=10, pady=5)
        
        # 用时
        ttk.Label(stats_grid, text="用时", font=('微软雅黑', 10)).grid(row=6, column=0, padx=20, pady=5, sticky=tk.W)
        ttk.Label(stats_grid, text=time_str, font=('微软雅黑', 14, 'bold'), foreground='#9b59b6').grid(row=6, column=1, padx=10, pady=5)
        
        # 收集错题信息
        self.wrong_questions = []
        for i, (eq_str, user_answer) in enumerate(zip(self.equations, self.user_answers)):
            try:
                user_num = int(user_answer)
            except:
                user_num = "未答"
            correct_answer = self.parse_equation(eq_str)
            if correct_answer is None:
                continue
            if user_num != correct_answer:
                self.wrong_questions.append({
                    'index': i + 1,
                    'question': eq_str,
                    'user_answer': user_num,
                    'correct_answer': correct_answer
                })
        
        # 如果有错题，显示"查看错题"按钮
        if self.wrong_questions:
            ttk.Button(
                self.practice_frame_single, 
                text=f"查看错题 ({len(self.wrong_questions)} 道)", 
                command=self.show_wrong_questions,
                style='Button.TButton'
            ).pack(fill=tk.X, pady=10, padx=50)
        else:
            ttk.Label(self.practice_frame_single, text="🎉 太棒了！全部答对！", font=('微软雅黑', 16, 'bold'), foreground='#27ae60').pack(pady=20)
        
        # 保存练习记录到数据库
        try:
            exercise_type = self.exercise_type.get()
            type_map = {"减法习题": "subtraction", "加法习题": "addition", "混合习题": "mixed"}
            db_manager.insert_practice_record(
                exercise_type=type_map.get(exercise_type, "mixed"),
                total_count=total,
                correct_count=self.correct_count,
                duration=self.elapsed_time,
                answers=','.join(self.user_answers),
                file_name=self.selected_exercise
            )
            ttk.Label(self.practice_frame_single, text="✓ 练习记录已保存", font=('微软雅黑', 10), foreground='#27ae60').pack(pady=5)
        except Exception as e:
            print(f"保存练习记录失败: {e}")
        
        self.restart_button.config(state=tk.NORMAL)
        self.update_status("联机练习完成")
    
    def show_wrong_questions(self):
        """显示错题详情对话框"""
        if not hasattr(self, 'wrong_questions') or not self.wrong_questions:
            return
            
        wrong_dialog = tk.Toplevel(self.dialog)
        wrong_dialog.title("错题详情")
        wrong_dialog.geometry("600x500")
        wrong_dialog.transient(self.dialog)
        wrong_dialog.grab_set()
        
        frame = ttk.Frame(wrong_dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"共 {len(self.wrong_questions)} 道错题", 
                 font=('微软雅黑', 14, 'bold')).pack(pady=(0, 10))
        
        # 创建错题列表（可滚动）
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for wq in self.wrong_questions:
            q_frame = ttk.Frame(scrollable_frame, padding="5", relief=tk.RIDGE)
            q_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(q_frame, text=f"第{wq['index']}题: {wq['question']}", 
                     font=('微软雅黑', 12)).pack(anchor=tk.W)
            ttk.Label(q_frame, text=f"你的答案: {wq['user_answer']}", 
                     font=('微软雅黑', 11), foreground='red').pack(anchor=tk.W)
            ttk.Label(q_frame, text=f"正确答案: {wq['correct_answer']}", 
                     font=('微软雅黑', 11), foreground='green').pack(anchor=tk.W)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(frame, text="关闭", command=wrong_dialog.destroy, 
                  style='Button.TButton').pack(pady=10)

class DataManagementDialog:
    def __init__(self, parent, update_status):
        self.parent = parent
        self.update_status = update_status
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("数据管理")
        self.dialog.geometry("700x500")
        self.dialog.resizable(True, True)  # 允许手动调整弹窗大小
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="数据管理", style='Title.TLabel').pack(pady=(0, 20))
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.exercise_tab = ttk.Frame(notebook)
        notebook.add(self.exercise_tab, text="习题文件")
        
        self.practice_tab = ttk.Frame(notebook)
        notebook.add(self.practice_tab, text="练习记录")
        
        self.load_exercise_data()
        self.load_practice_data()
        
    def load_exercise_data(self):
        for widget in self.exercise_tab.winfo_children():
            widget.destroy()
            
        try:
            exercises = db_manager.get_all_exercises()
            
            tree = ttk.Treeview(self.exercise_tab, columns=('id', 'filename', 'type', 'count', 'created'), show='headings')
            tree.heading('id', text='ID')
            tree.heading('filename', text='文件名')
            tree.heading('type', text='类型')
            tree.heading('count', text='题数')
            tree.heading('created', text='创建时间')
            tree.column('id', width=50)
            tree.column('filename', width=250)
            tree.column('type', width=100)
            tree.column('count', width=80)
            tree.column('created', width=150)
            tree.pack(fill=tk.BOTH, expand=True)
            
            type_map = {'addition': '加法', 'subtraction': '减法', 'mixed': '混合'}
            
            for ex in exercises:
                tree.insert('', tk.END, values=(
                    ex['id'],
                    ex['filename'],
                    type_map.get(ex['file_type'], ex['file_type']),
                    ex['question_count'],
                    ex['created_at']
                ))
                
            self.update_status("习题数据加载完成")
            
        except Exception as e:
            ttk.Label(self.exercise_tab, text=f"加载失败: {str(e)}").pack()
            
    def load_practice_data(self):
        for widget in self.practice_tab.winfo_children():
            widget.destroy()
            
        try:
            practices = db_manager.execute_query("SELECT * FROM practice_results ORDER BY created_at DESC")
            
            tree = ttk.Treeview(self.practice_tab, columns=('id', 'filename', 'exercise_id', 'created'), show='headings')
            tree.heading('id', text='ID')
            tree.heading('filename', text='文件名')
            tree.heading('exercise_id', text='关联习题')
            tree.heading('created', text='创建时间')
            tree.column('id', width=50)
            tree.column('filename', width=300)
            tree.column('exercise_id', width=100)
            tree.column('created', width=150)
            tree.pack(fill=tk.BOTH, expand=True)
            
            for pr in practices:
                tree.insert('', tk.END, values=(
                    pr['id'],
                    pr['filename'],
                    pr['exercise_id'],
                    pr['created_at']
                ))
                
            self.update_status("练习记录加载完成")
            
        except Exception as e:
            ttk.Label(self.practice_tab, text=f"加载失败: {str(e)}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    
    try:
        db_manager.create_tables()
        app.update_status("数据库连接成功")
    except Exception as e:
        app.update_status(f"数据库连接失败: {str(e)}")
        messagebox.showwarning("警告", f"数据库连接失败: {str(e)}\n程序仍可运行，但数据无法持久化")
    
    root.mainloop()