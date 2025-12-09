#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
子网计算器应用程序 - 主窗口
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import os

# 配置日志记录
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'app.log')),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

logger = logging.getLogger(__name__)

from ip_subnet_calculator import split_subnet, ip_to_int, get_subnet_info

class IPSubnetSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP子网切分工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TLabel", font=('微软雅黑', 10))
        self.style.configure("TButton", font=('微软雅黑', 10))
        self.style.configure("TEntry", font=('微软雅黑', 10))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建输入区域
        self.create_input_section()
        
        # 创建按钮区域
        self.create_button_section()
        
        # 创建结果区域
        self.create_result_section()
        
        # 初始化图表数据
        self.chart_data = None
        
    def create_input_section(self):
        """创建输入区域"""
        input_frame = ttk.LabelFrame(self.main_frame, text="输入参数", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 父网段
        ttk.Label(input_frame, text="父网段 (如: 10.0.0.0/8)").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.parent_entry = ttk.Entry(input_frame, width=30)
        self.parent_entry.grid(row=0, column=1, padx=10, pady=5)
        self.parent_entry.insert(0, "10.0.0.0/8")  # 默认值
        
        # 切分网段
        ttk.Label(input_frame, text="切分网段 (如: 10.21.60.0/23)").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.split_entry = ttk.Entry(input_frame, width=30)
        self.split_entry.grid(row=1, column=1, padx=10, pady=5)
        self.split_entry.insert(0, "10.21.60.0/23")  # 默认值
    
    def create_button_section(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 执行按钮
        self.execute_btn = ttk.Button(button_frame, text="执行切分", command=self.execute_split, width=20)
        self.execute_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        self.clear_btn = ttk.Button(button_frame, text="清空结果", command=self.clear_result, width=20)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
    
    def create_result_section(self):
        """创建结果显示区域"""
        result_frame = ttk.LabelFrame(self.main_frame, text="切分结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个笔记本控件来显示不同的结果页面
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 切分网段信息页面
        self.split_info_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.split_info_frame, text="切分网段信息")
        
        # 创建切分网段信息表格
        self.split_tree = ttk.Treeview(self.split_info_frame, columns=("item", "value"), show="headings")
        self.split_tree.heading("item", text="项目")
        self.split_tree.heading("value", text="值")
        self.split_tree.column("item", width=150)
        self.split_tree.column("value", width=250)
        self.split_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 剩余网段列表页面
        self.remaining_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.remaining_frame, text="剩余网段列表")
        
        # 创建剩余网段信息表格
        self.remaining_tree = ttk.Treeview(self.remaining_frame, 
                                          columns=("index", "cidr", "network", "netmask", "broadcast", "usable"), 
                                          show="headings")
        self.remaining_tree.heading("index", text="序号")
        self.remaining_tree.heading("cidr", text="CIDR")
        self.remaining_tree.heading("network", text="网络地址")
        self.remaining_tree.heading("netmask", text="子网掩码")
        self.remaining_tree.heading("broadcast", text="广播地址")
        self.remaining_tree.heading("usable", text="可用地址数")
        
        self.remaining_tree.column("index", width=50)
        self.remaining_tree.column("cidr", width=120)
        self.remaining_tree.column("network", width=120)
        self.remaining_tree.column("netmask", width=120)
        
        # 网段分布图表页面
        self.chart_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.chart_frame, text="网段分布图表")
        
        # 创建Canvas用于绘制柱状图
        self.chart_canvas = tk.Canvas(self.chart_frame, bg="white")
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 绑定窗口大小变化事件，实现图表自适应
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        self.remaining_tree.column("broadcast", width=120)
        self.remaining_tree.column("usable", width=100)
        
        # 添加滚动条
        self.remaining_scroll = ttk.Scrollbar(self.remaining_frame, orient=tk.VERTICAL, command=self.remaining_tree.yview)
        self.remaining_tree.configure(yscrollcommand=self.remaining_scroll.set)
        
        self.remaining_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        self.remaining_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # 初始提示
        self.clear_result()
    
    def execute_split(self):
        """执行切分操作"""
        parent = self.parent_entry.get().strip()
        split = self.split_entry.get().strip()
        
        # 验证输入
        if not parent or not split:
            # 清空表格并显示错误信息
            self.clear_result()
            self.split_tree.delete(*self.split_tree.get_children())
            self.split_tree.insert("", tk.END, values=("错误", "父网段和切分网段都不能为空！"), tags=('error',))
            # 设置错误标签样式
            self.split_tree.tag_configure('error', foreground='red')
            return
        
        try:
            # 调用切分函数
            result = split_subnet(parent, split)
            
            # 清空现有结果
            for item in self.split_tree.get_children():
                self.split_tree.delete(item)
            for item in self.remaining_tree.get_children():
                self.remaining_tree.delete(item)
            
            if 'error' in result:
                # 显示错误信息
                self.split_tree.delete(*self.split_tree.get_children())
                self.split_tree.insert("", tk.END, values=("错误", result['error']), tags=('error',))
                self.split_tree.tag_configure('error', foreground='red')
                return
            
            # 显示切分网段信息表格
            self.split_tree.delete(*self.split_tree.get_children())
            self.split_tree.insert("", tk.END, values=("父网段", parent))
            self.split_tree.insert("", tk.END, values=("切分网段", split))
            self.split_tree.insert("", tk.END, values=("-" * 10, "-" * 20))
            
            # 添加切分后的网段信息
            split_info = result['split_info']
            self.split_tree.insert("", tk.END, values=("网络地址", split_info['network']))
            self.split_tree.insert("", tk.END, values=("子网掩码", split_info['netmask']))
            self.split_tree.insert("", tk.END, values=("广播地址", split_info['broadcast']))
            self.split_tree.insert("", tk.END, values=("可用地址数", split_info['usable_addresses']))
            self.split_tree.insert("", tk.END, values=("CIDR", split_info['cidr']))
            
            # 显示剩余网段列表表格
            if result['remaining_subnets_info']:
                for i, network in enumerate(result['remaining_subnets_info'], 1):
                    self.remaining_tree.insert("", tk.END, values=(
                        i,
                        network['cidr'],
                        network['network'],
                        network['netmask'],
                        network['broadcast'],
                        network['usable_addresses']
                    ))
            else:
                self.remaining_tree.insert("", tk.END, values=(1, "无", "无", "无", "无", "无"))
            
            # 准备图表数据
            self.prepare_chart_data(result, split_info, result['remaining_subnets_info'])
            
            # 绘制图表
            self.draw_distribution_chart()
                
        except Exception as e:
            self.clear_result()
            self.split_tree.insert("", tk.END, values=("错误", str(e)), tags=('error',))
            self.split_tree.tag_configure('error', foreground='red')
    
    def show_result(self, text, error=False):
        """显示结果"""
        # 清空表格
        self.clear_result()
        
        # 在切分网段表格中显示错误信息
        if error:
            self.split_tree.insert("", tk.END, values=("错误", text), tags=('error',))
        else:
            self.split_tree.insert("", tk.END, values=("信息", text), tags=('info',))
        self.split_tree.tag_configure('error', foreground='red')
        self.split_tree.tag_configure('info', foreground='blue')

    def prepare_chart_data(self, result, split_info, remaining_subnets):
        """准备图表数据"""
        try:
            # 获取父网段信息
            parent_cidr = result.get('parent', '')
            if not parent_cidr:
                self.chart_data = None
                return
            
            parent_info = get_subnet_info(parent_cidr)
            if 'error' in parent_info:
                self.chart_data = None
                return
            
            parent_start = ip_to_int(parent_info.get('network', '0.0.0.0'))
            parent_end = ip_to_int(parent_info.get('broadcast', '0.0.0.0'))
            parent_range = parent_end - parent_start + 1
            
            # 准备所有网段数据
            self.chart_data = {
                'parent': {
                    'start': parent_start,
                    'end': parent_end,
                    'range': parent_range,
                    'name': parent_info.get('cidr', parent_cidr),
                    'color': '#e0e0e0'
                },
                'networks': []
            }
            
            # 添加切分网段
            if split_info:
                split_start = ip_to_int(split_info.get('network', '0.0.0.0'))
                split_end = ip_to_int(split_info.get('broadcast', '0.0.0.0'))
                self.chart_data['networks'].append({
                    'start': split_start,
                    'end': split_end,
                    'range': split_end - split_start + 1,
                    'name': split_info.get('cidr', result.get('split', '')),
                    'color': '#4285f4',  # 蓝色
                    'type': 'split'
                })
            
            # 添加剩余网段
            colors = ['#34a853', '#fbbc05', '#ea4335', '#9c27b0', '#00acc1', '#ff5722']  # 颜色列表
            for i, subnet in enumerate(remaining_subnets):
                subnet_start = ip_to_int(subnet.get('network', '0.0.0.0'))
                subnet_end = ip_to_int(subnet.get('broadcast', '0.0.0.0'))
                self.chart_data['networks'].append({
                    'start': subnet_start,
                    'end': subnet_end,
                    'range': subnet_end - subnet_start + 1,
                    'name': subnet.get('cidr', ''),
                    'color': colors[i % len(colors)],  # 循环使用颜色
                    'type': 'remaining'
                })
            
            # 按起始地址排序
            self.chart_data['networks'].sort(key=lambda x: x['start'])
        except Exception as e:
            # 如果出现任何错误，就不绘制图表
            self.chart_data = None
    
    def on_chart_resize(self, event):
        """Canvas尺寸变化时重新绘制图表"""
        # 当Canvas尺寸变化时重新绘制图表
        self.draw_distribution_chart()
    
    def draw_distribution_chart(self):
        """绘制网段分布柱状图"""
        logger.debug("开始绘制分布图...")
        if not self.chart_data:
            logger.debug("没有图表数据，跳过绘制")
            return
        
        # 初始化安全的默认值，防止异常时变量未定义
        width = 600
        height = 400
        label_font = ('微软雅黑', 8)
        title_font = ('微软雅黑', 10, 'bold')
        margin_bottom = 60
        
        try:
            # 清空Canvas
            logger.debug("清空Canvas...")
            self.chart_canvas.delete("all")
            
            # 获取Canvas尺寸
            width = self.chart_canvas.winfo_width()
            height = self.chart_canvas.winfo_height()
            logger.debug(f"Canvas尺寸: {width}x{height}")
            
            # 如果Canvas还没有渲染完成，使用默认尺寸
            if width < 10 or height < 10:
                width = 600
                height = 400
                logger.debug(f"Canvas未渲染完成，使用默认尺寸: {width}x{height}")
            
            # 优化的边距策略 - 左右边距根据宽度自适应，上下边距固定比例
            margin_left = int(width * 0.15)  # 左侧边距占15%，用于显示标签
            margin_right = int(width * 0.1)   # 右侧边距占10%，用于显示百分比
            margin_top = 60  # 固定上边距，用于标题
            margin_bottom = 60  # 固定下边距，用于X轴标签
            
            # 确保最小边距
            margin_left = max(margin_left, 120)  # 确保有足够空间显示标签
            margin_right = max(margin_right, 60)  # 确保有足够空间显示百分比
            logger.debug(f"边距设置: 左={margin_left}, 右={margin_right}, 上={margin_top}, 下={margin_bottom}")
            
            # 可用绘图区域
            chart_width = width - margin_left - margin_right
            chart_height = height - margin_top - margin_bottom
            logger.debug(f"可用绘图区域: {chart_width}x{chart_height}")
            
            # 获取父网段范围
            parent_start = self.chart_data.get('parent', {}).get('start', 0)
            parent_end = self.chart_data.get('parent', {}).get('end', 1)
            parent_range = self.chart_data.get('parent', {}).get('range', 1)
            logger.debug(f"父网段: 开始={parent_start}, 结束={parent_end}, 范围={parent_range}")
            
            # 计算缩放比例
            scale = chart_width / parent_range if parent_range > 0 else 1
            logger.debug(f"缩放比例: {scale}")
            
            # 绘制背景
            logger.debug("绘制背景...")
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, fill="#f5f5f5")
            
            # 绘制父网段背景
            parent_color = self.chart_data.get('parent', {}).get('color', '#e0e0e0')
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, 
                                              fill=parent_color, outline="#ccc")
            
            # 获取网段列表
            networks = self.chart_data.get('networks', [])
            logger.debug(f"获取到网段列表: {networks}")
            if not networks:
                # 没有网段时显示提示
                logger.debug("没有网段数据，显示提示信息")
                self.chart_canvas.create_text(width / 2, height / 2, 
                                             text="无网段数据", font=('微软雅黑', 12))
                return
            
            # 自适应字体大小 - 主要根据宽度调整
            base_font_size = width // 60
            label_font = ('微软雅黑', max(base_font_size, 8))
            title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
            logger.debug(f"字体设置: 基础={base_font_size}, 标签={label_font}, 标题={title_font}")
            
            # 绘制标题
            logger.debug("绘制标题...")
            self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                         text="网段分布示意图", font=title_font)
            
            # 绘制各网段
            total_items = len(networks)
            logger.debug(f"网段数量: {total_items}")
            if total_items > 0:
                # 计算合适的柱状图高度，确保在可用高度内显示
                available_height = chart_height - 20  # 留出20px的额外空间
                min_bar_height = 15  # 最小柱状图高度，减少到15px以适应更多网段
                min_bar_spacing = 5  # 最小间距，减少到5px以适应更多网段
                logger.debug(f"可用高度: {available_height}, 最小高度: {min_bar_height}, 最小间距: {min_bar_spacing}")
                
                # 计算最大可能的柱状图高度和间距
                total_spacing = (total_items - 1) * min_bar_spacing
                max_possible_bar_height = (available_height - total_spacing) / total_items
                logger.debug(f"总间距: {total_spacing}, 最大可能高度: {max_possible_bar_height}")
                
                # 确定最终的柱状图高度和间距
                bar_height = max(max_possible_bar_height, min_bar_height)  # 不再限制最大高度，确保能在可用高度内显示
                bar_spacing = min_bar_spacing  # 使用最小间距以节省空间
                logger.debug(f"柱状图参数: 高度={bar_height}, 间距={bar_spacing}")
                
                # 计算实际需要的高度
                required_height = total_items * bar_height + (total_items - 1) * bar_spacing
                logger.debug(f"所需高度: {required_height}")
                
                # 计算垂直居中的起始位置
                start_y = margin_top + (chart_height - required_height) / 2
                logger.debug(f"起始Y坐标: {start_y}")
                
                # 确保起始位置不会越界
                start_y = max(start_y, margin_top + 5)
                logger.debug(f"调整后起始Y坐标: {start_y}")
                
                # 如果所需高度超过可用高度，强制压缩
                if required_height > available_height:
                    # 重新计算，确保所有柱状图都能在可用高度内显示
                    total_height_needed = total_items * min_bar_height + (total_items - 1) * min_bar_spacing
                    if total_height_needed > available_height:
                        # 即使使用最小高度和间距也不够，进一步压缩
                        total_elements = total_items * 2 - 1  # 每个柱状图和间距算一个元素
                        min_element_height = 20  # 最小元素高度（柱状图+间距）
                        if total_elements * min_element_height > available_height:
                            # 极端情况：每个元素只占1px
                            min_element_height = 1
                        
                        # 计算新的高度和间距
                        bar_height = max(min_element_height - 2, 1)  # 柱状图高度
                        bar_spacing = min(2, available_height - total_items * bar_height)  # 间距
                        if bar_spacing < 1:
                            bar_spacing = 1
                    
                    # 重新计算所需高度和起始位置
                    required_height = total_items * bar_height + (total_items - 1) * bar_spacing
                    start_y = margin_top + 5  # 从顶部开始绘制
                    logger.debug(f"高度不足，强制压缩: 新高度={bar_height}, 新间距={bar_spacing}, 新起始Y={start_y}")
                
                # 确保字体大小与柱状图高度匹配
                if bar_height < 20:
                    # 当柱状图高度较小时，减小字体大小
                    label_font_size = max(int(bar_height * 0.6), 6)
                    label_font = ('微软雅黑', label_font_size)
                    logger.debug(f"柱状图高度较小，调整字体大小: {label_font_size}")
                
                for i, network in enumerate(networks):
                    logger.debug(f"处理网段 {i+1}: {network['name']}")
                    # 计算柱状图位置和宽度
                    x1 = margin_left + (network.get('start', 0) - parent_start) * scale
                    x2 = margin_left + (network.get('end', 0) - parent_start) * scale
                    y1 = start_y + i * (bar_height + bar_spacing)
                    y2 = y1 + bar_height
                    logger.debug(f"  原始坐标: ({x1}, {y1}) 到 ({x2}, {y2})")
                    
                    # 确保柱状图在可用区域内
                    y1 = min(y1, margin_top + chart_height - bar_height)
                    y2 = min(y2, margin_top + chart_height)
                    logger.debug(f"  调整后坐标: ({x1}, {y1}) 到 ({x2}, {y2})")
                    
                    # 绘制柱状图
                    color = network.get('color', '#cccccc')
                    logger.debug(f"  绘制矩形: 颜色={color}")
                    self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333", width=1)
                    
                    # 绘制网段名称 - 确保在Canvas范围内
                    label_x = max(10, margin_left - 10)  # 确保不超出左边界
                    label_y = y1 + bar_height / 2
                    name = network.get('name', '未知')
                    logger.debug(f"  绘制名称: {name} 位置=({label_x}, {label_y})")
                    self.chart_canvas.create_text(label_x, label_y, text=name, anchor=tk.E, font=label_font)
                    
                    # 绘制网段范围占比 - 确保在Canvas范围内
                    percentage_x = min(width - 10, margin_left + chart_width + 10)  # 确保不超出右边界
                    percentage = (network.get('range', 0) / parent_range * 100) if parent_range > 0 else 0
                    logger.debug(f"  绘制百分比: {percentage:.1f}% 位置=({percentage_x}, {label_y})")
                    self.chart_canvas.create_text(percentage_x, label_y, 
                                                 text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
        except Exception as e:
            logger.error(f"图表绘制失败: {str(e)}", exc_info=True)
            # 出现错误时显示提示
            self.chart_canvas.delete("all")
            # 使用安全的默认值
            width = self.chart_canvas.winfo_width() or 600
            height = self.chart_canvas.winfo_height() or 400
            title_font = ('微软雅黑', 10, 'bold')  # 确保字体已定义
            self.chart_canvas.create_text(width / 2, height / 2, 
                                         text="图表绘制失败", font=title_font, fill="red")
        
        # 绘制X轴标签 - 确保使用已定义的变量
        try:
            logger.debug(f"绘制X轴标签: 位置=({width/2}, {height - margin_bottom/2})")
            self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                         text="网段地址范围", font=label_font)
        except Exception as e:
            logger.error(f"绘制X轴标签失败: {str(e)}", exc_info=True)
            # 最后的安全保障
            pass
        
        logger.debug("分布图绘制完成")
    
    def clear_result(self):
        """清空结果表格和图表"""
        # 清空切分网段信息表格
        for item in self.split_tree.get_children():
            self.split_tree.delete(item)
        self.split_tree.insert("", tk.END, values=("提示", "点击'执行切分'按钮开始操作..."))
        
        # 清空剩余网段列表表格
        for item in self.remaining_tree.get_children():
            self.remaining_tree.delete(item)
        
        # 清空图表
        self.chart_canvas.delete("all")
        self.chart_data = None

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口图标（可选，如果有图标文件可以添加）
    # root.iconbitmap("icon.ico")
    
    # 创建应用实例
    app = IPSubnetSplitterApp(root)
    
    # 运行应用
    root.mainloop()
