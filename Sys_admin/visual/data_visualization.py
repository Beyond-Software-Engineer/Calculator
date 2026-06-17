

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, SpanSelector
from matplotlib.patches import Rectangle
from scipy import stats

# 设置现代化风格
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100


class InteractiveDataVisualizer:
    """交互式数据可视化类"""
    
    def __init__(self, data_path):
        """初始化"""
        self.data_path = data_path
        self.df = None
        self.numeric_data = None
        self.gene_names = []
        self.selected_genes = []
        self.fig = None
        self.ax = None
        self.lines = {}
        self.check = None
        self.line_colors = {}
        # 使用现代化配色方案
        self.color_palette = [
            '#3B82F6',  # 蓝色
            '#EF4444',  # 红色
            '#10B981',  # 绿色
            '#F59E0B',  # 橙色
            '#8B5CF6',  # 紫色
            '#EC4899',  # 粉色
            '#06B6D4',  # 青色
            '#84CC16',  # 黄绿
            '#F97316',  # 琥珀
            '#6366F1',  # 靛蓝
            '#EC4899',  # 玫红
            '#14B8A6',  # 青绿
            '#FBBF24',  # 黄色
            '#A855F7',  # 紫罗兰
            '#0EA5E9',  # 天蓝
            '#D946EF',  # 紫红
            '#22C55E',  # 翠绿
            '#F43F5E',  # 玫瑰红
            '#60A5FA',  # 浅蓝
        ]
        self.load_data()
    
    def load_data(self):
        """加载CSV数据"""
        print("正在加载数据...")
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            data = []
            max_columns = 0
            
            for i, line in enumerate(lines):
                parts = [p for p in line.strip().split() if p != '']
                if len(parts) > 0:
                    if len(parts) > max_columns:
                        max_columns = len(parts)
                    gene_name = parts[0]
                    values = []
                    for val in parts[1:]:
                        try:
                            values.append(float(val))
                        except ValueError:
                            values.append(np.nan)
                    data.append([gene_name] + values)
            
            for row in data:
                while len(row) < max_columns:
                    row.append(np.nan)
            
            headers = ['gene'] + [f'feature_{j}' for j in range(max_columns - 1)]
            self.df = pd.DataFrame(data, columns=headers)
            self.numeric_data = self.df.iloc[:, 1:].fillna(0)
            self.gene_names = self.df['gene'].tolist()
            
            # 为每个基因分配颜色
            for i, gene in enumerate(self.gene_names):
                self.line_colors[gene] = self.color_palette[i % len(self.color_palette)]
            
            print(f"数据加载完成，共 {len(self.gene_names)} 个基因")
            
        except Exception as e:
            print(f"数据加载失败: {e}")
    
    def calculate_correlation(self, gene1, gene2):
        """计算两条折线的相关性"""
        data1 = self.numeric_data.iloc[self.gene_names.index(gene1)].values
        data2 = self.numeric_data.iloc[self.gene_names.index(gene2)].values
        
        pearson_r, pearson_p = stats.pearsonr(data1, data2)
        spearman_r, spearman_p = stats.spearmanr(data1, data2)
        
        return {
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p
        }
    
    def calculate_association(self, gene1, gene2):
        """计算两条折线的关联性"""
        data1 = self.numeric_data.iloc[self.gene_names.index(gene1)].values
        data2 = self.numeric_data.iloc[self.gene_names.index(gene2)].values
        
        covariance = np.cov(data1, data2)[0, 1]
        median1 = np.median(data1)
        median2 = np.median(data2)
        binary1 = (data1 >= median1).astype(int)
        binary2 = (data2 >= median2).astype(int)
        point_biserial_r, _ = stats.pointbiserialr(binary2, data1)
        
        bins = 5
        hist_2d, _, _ = np.histogram2d(data1, data2, bins=bins)
        hist_1d_1 = np.sum(hist_2d, axis=1)
        hist_1d_2 = np.sum(hist_2d, axis=0)
        
        mutual_info = 0
        n = len(data1)
        for i in range(bins):
            for j in range(bins):
                if hist_2d[i, j] > 0:
                    p_xy = hist_2d[i, j] / n
                    p_x = hist_1d_1[i] / n
                    p_y = hist_1d_2[j] / n
                    if p_x > 0 and p_y > 0:
                        mutual_info += p_xy * np.log(p_xy / (p_x * p_y) + 1e-10)
        
        return {
            'covariance': covariance,
            'point_biserial_r': point_biserial_r,
            'mutual_info': mutual_info
        }
    
    def on_click(self, event):
        """点击事件处理"""
        if event.inaxes != self.ax:
            return
        
        x, y = event.xdata, event.ydata
        if x is None:
            return
        
        feature_idx = int(x)
        if feature_idx < 0 or feature_idx >= len(self.numeric_data.columns):
            return
        
        selected_text = "选择点的特征索引: {}\n".format(feature_idx)
        for gene in self.selected_genes:
            gene_idx = self.gene_names.index(gene)
            value = self.numeric_data.iloc[gene_idx, feature_idx]
            selected_text += f"{gene}: {value:.4f}\n"
        
        print(selected_text)
    
    def onselect(self, xmin, xmax):
        """区域选择"""
        xmin_idx = max(0, int(xmin))
        xmax_idx = min(len(self.numeric_data.columns) - 1, int(xmax))
        
        if len(self.selected_genes) == 2:
            gene1, gene2 = self.selected_genes[0], self.selected_genes[1]
            data1 = self.numeric_data.iloc[self.gene_names.index(gene1), xmin_idx:xmax_idx+1].values
            data2 = self.numeric_data.iloc[self.gene_names.index(gene2), xmin_idx:xmax_idx+1].values
            
            pearson_r, pearson_p = stats.pearsonr(data1, data2)
            spearman_r, spearman_p = stats.spearmanr(data1, data2)
            
            result_text = f"\n选中区域 [{xmin_idx}-{xmax_idx}] 的相关性分析:\n"
            result_text += f"  Pearson相关系数: {pearson_r:.4f} (p={pearson_p:.4f})\n"
            result_text += f"  Spearman相关系数: {spearman_r:.4f} (p={spearman_p:.4f})\n"
            
            print(result_text)
    
    def update(self, label):
        """更新选择"""
        if label in self.selected_genes:
            self.selected_genes.remove(label)
            self.lines[label].set_visible(False)
            self.lines[label].set_alpha(0)
        else:
            self.selected_genes.append(label)
            self.lines[label].set_visible(True)
            self.lines[label].set_alpha(1)
        
        if len(self.selected_genes) == 2:
            gene1, gene2 = self.selected_genes[0], self.selected_genes[1]
            self.show_correlation_analysis(gene1, gene2)
            self.plot_scatter_correlation(gene1, gene2)
        elif len(self.selected_genes) > 2:
            print("警告: 最多只能选择两条折线进行相关性分析")
        
        plt.draw()
    
    def show_correlation_analysis(self, gene1, gene2):
        """显示相关性分析结果"""
        print("\n" + "="*60)
        print(f"相关性分析: {gene1} vs {gene2}")
        print("="*60)
        
        corr = self.calculate_correlation(gene1, gene2)
        print("\n【相关性分析】")
        print(f"  Pearson相关系数: {corr['pearson_r']:.4f}")
        print(f"  Pearson p值: {corr['pearson_p']:.6f}")
        print(f"  Spearman相关系数: {corr['spearman_r']:.4f}")
        print(f"  Spearman p值: {corr['spearman_p']:.6f}")
        
        assoc = self.calculate_association(gene1, gene2)
        print("\n【关联性分析】")
        print(f"  协方差: {assoc['covariance']:.4f}")
        print(f"  点二列相关系数: {assoc['point_biserial_r']:.4f}")
        print(f"  互信息: {assoc['mutual_info']:.4f}")
        
        print("\n【结果解读】")
        r = corr['pearson_r']
        if abs(r) >= 0.8:
            strength = "极强"
        elif abs(r) >= 0.6:
            strength = "强"
        elif abs(r) >= 0.4:
            strength = "中等"
        elif abs(r) >= 0.2:
            strength = "弱"
        else:
            strength = "极弱或无"
        
        direction = "正" if r > 0 else "负"
        print(f"  两基因表达呈{direction}向{strength}相关性")
        
        if corr['pearson_p'] < 0.05:
            print(f"  统计显著性: 显著 (p < 0.05)")
        else:
            print(f"  统计显著性: 不显著 (p >= 0.05)")
        
        print("="*60 + "\n")
    
    def plot_scatter_correlation(self, gene1, gene2):
        """绘制散点图显示相关性"""
        fig, ax = plt.subplots(figsize=(9, 7))
        
        data1 = self.numeric_data.iloc[self.gene_names.index(gene1)].values
        data2 = self.numeric_data.iloc[self.gene_names.index(gene2)].values
        
        ax.scatter(data1, data2, alpha=0.7, s=70, c=self.line_colors[gene1], 
                   edgecolors='white', linewidth=1.5, zorder=2)
        
        z = np.polyfit(data1, data2, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(data1), max(data1), 100)
        ax.plot(x_line, p(x_line), "--", color=self.line_colors[gene2], 
                alpha=0.9, linewidth=2.5, label='趋势线')
        
        r, p_value = stats.pearsonr(data1, data2)
        
        ax.set_title(f'{gene1} vs {gene2} 相关性分析', fontsize=16, pad=20, fontweight='bold')
        ax.set_xlabel(f'{gene1} 表达值', fontsize=13)
        ax.set_ylabel(f'{gene2} 表达值', fontsize=13)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.legend(fontsize=12)
        
        # 添加相关性系数注释
        ax.annotate(f'Pearson r = {r:.4f}', xy=(0.05, 0.92), xycoords='axes fraction',
                    fontsize=12, fontweight='bold', color='#374151')
        ax.annotate(f'p-value = {p_value:.4f}', xy=(0.05, 0.87), xycoords='axes fraction',
                    fontsize=11, color='#6B7280')
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_plot(self):
        """创建交互式折线图"""
        print("\n正在创建交互式可视化...")
        print("提示: 点击右侧复选框选择基因，最多选择2条折线进行相关性分析")
        print("      点击图表上的点可以查看具体数值")
        print("-" * 60)
        
        # 创建图形
        self.fig = plt.figure(figsize=(16, 9), facecolor='#F8FAFC')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#FFFFFF')
        
        # 绘制所有基因的折线
        x = range(len(self.numeric_data.columns))
        
        for i, gene in enumerate(self.gene_names):
            data = self.numeric_data.iloc[i].values
            color = self.line_colors[gene]
            line, = self.ax.plot(x, data, label=gene, color=color, 
                                 linewidth=2.5, alpha=0, visible=False,
                                 linestyle='-', marker='', markerfacecolor=color)
            self.lines[gene] = line
        
        # 默认选择前两条
        if len(self.gene_names) >= 2:
            self.selected_genes = [self.gene_names[0], self.gene_names[1]]
            for gene in self.selected_genes:
                self.lines[gene].set_visible(True)
                self.lines[gene].set_alpha(1)
        
        # 设置坐标轴样式
        self.ax.set_title('基因表达折线图', fontsize=20, pad=25, fontweight='bold', color='#1E293B')
        self.ax.set_xlabel('特征索引', fontsize=14, color='#475569')
        self.ax.set_ylabel('表达值', fontsize=14, color='#475569')
        self.ax.grid(True, alpha=0.15, linestyle='--', color='#CBD5E1')
        self.ax.tick_params(axis='both', labelsize=12, colors='#64748B')
        
        # 设置边框样式
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#E2E8F0')
            spine.set_linewidth(1.5)
        
        # 创建现代化图例
        handles, labels = self.ax.get_legend_handles_labels()
        legend = self.ax.legend(handles, labels, loc='upper right', 
                               bbox_to_anchor=(0.98, 0.98),
                               fontsize=11, frameon=True,
                               fancybox=True, shadow=True,
                               borderpad=1.2, labelspacing=0.8,
                               handlelength=2.5, handletextpad=1.0)
        legend.get_frame().set_facecolor('#FFFFFF')
        legend.get_frame().set_edgecolor('#E2E8F0')
        legend.get_frame().set_alpha(0.95)
        
        # 创建现代化复选框面板
        check_ax = plt.axes([0.86, 0.08, 0.13, 0.85], facecolor='#FAFBFC')
        check_ax.set_frame_on(True)
        check_ax.spines['top'].set_edgecolor('#E2E8F0')
        check_ax.spines['bottom'].set_edgecolor('#E2E8F0')
        check_ax.spines['left'].set_edgecolor('#E2E8F0')
        check_ax.spines['right'].set_edgecolor('#E2E8F0')
        
        # 添加面板标题
        check_ax.text(0.5, 0.97, '基因选择', fontsize=14, fontweight='bold',
                     color='#1E293B', ha='center')
        check_ax.axhline(y=0.94, xmin=0.05, xmax=0.95, color='#E2E8F0', linewidth=1)
        
        # 创建复选框（使用标准参数）
        self.check = CheckButtons(check_ax, self.gene_names, 
                                 [gene in self.selected_genes for gene in self.gene_names])
        
        # 设置复选框标签样式
        for i, label in enumerate(self.check.labels):
            label.set_fontsize(11)
            label.set_color(self.line_colors[self.gene_names[i]])
            label.set_fontweight('normal')
        
        self.check.on_clicked(self.update)
        
        # 添加区域选择器
        span = SpanSelector(self.ax, self.onselect, 'horizontal', 
                           button=1, useblit=True,
                           props=dict(alpha=0.25, facecolor='#3B82F6', edgecolor='#1D4ED8', 
                                     linewidth=1.5, linestyle='--'))
        
        # 添加提示文字
        self.fig.text(0.02, 0.02, '💡 提示: 点击复选框选择基因 | 鼠标拖拽选择区域分析', 
                     fontsize=11, color='#94A3B8')
        
        # 连接点击事件
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        plt.tight_layout()
        plt.subplots_adjust(right=0.84)
        
        plt.show()
    
    def run(self):
        """运行交互式程序"""
        if self.numeric_data is not None:
            self.create_interactive_plot()


def main():
    """主函数"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '实验7-数据.csv')
    
    visualizer = InteractiveDataVisualizer(data_path)
    
    if visualizer.numeric_data is not None:
        print("\n" + "="*60)
        print("交互式基因表达可视化程序")
        print("="*60)
        print(f"数据概览:")
        print(f"  - 基因数量: {len(visualizer.gene_names)}")
        print(f"  - 特征数量: {len(visualizer.numeric_data.columns)}")
        print(f"  - 基因列表: {', '.join(visualizer.gene_names)}")
        
        visualizer.run()


if __name__ == '__main__':
    main()