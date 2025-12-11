#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
子网计算器应用程序 - 主窗口
"""

# 所有导入语句放在最顶部
import tkinter as tk
import math
from tkinter import ttk, filedialog

# 导入自定义模块
from ip_subnet_calculator import split_subnet, ip_to_int, get_subnet_info

# 自定义的ColoredNotebook类，支持每个标签不同颜色
class ColoredNotebook(ttk.Frame):
    def __init__(self, master, style=None, tab_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # 保存样式对象
        self.style = style
        # 保存标签页切换回调函数
        self.tab_change_callback = tab_change_callback
        
        # 创建标签栏容器，使用ttk.Frame并继承默认样式
        self.tab_bar_container = ttk.Frame(self)
        self.tab_bar_container.pack(side="top", fill="x")
        
        # 创建标签栏 - 使用ttk.Frame并继承默认样式
        self.tab_bar = ttk.Frame(self.tab_bar_container)
        self.tab_bar.pack(side="left", fill="y")
        
        # 创建一个占位Frame，使用ttk.Frame并继承默认样式
        self.tab_bar_spacer = ttk.Frame(self.tab_bar_container)
        self.tab_bar_spacer.pack(side="left", fill="both", expand=True)
        
        # 创建内容区域 - 移除箭头指向的灰色框线
        self.content_area = ttk.Frame(self, borderwidth=0, relief="flat")
        self.content_area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        
        # 标签配置
        self.tabs = []
        self.active_tab = None
        
    def _update_background_color(self):
        """更新标签栏背景色以匹配父容器"""
        # 获取标签栏容器的父组件（result_frame）的背景色
        # 由于ttk组件的背景色获取方式与tk组件不同，我们需要特殊处理
        try:
            # 使用self.master获取父容器对象
            if hasattr(self.master, 'winfo_bg'):
                bg_color = self.master.winfo_bg()
            else:
                # 如果是ttk组件，尝试使用style.lookup获取背景色
                bg_color = self.style.lookup(self.master.winfo_class(), 'background')
            
            # 如果获取的是系统默认颜色名称，转换为实际颜色值
            if not bg_color or bg_color.startswith('system.'):
                bg_color = self.winfo_toplevel().cget("bg")
                
        except Exception as e:
            # 如果获取失败，尝试获取窗口背景色作为备选
            bg_color = self.winfo_toplevel().cget("bg")
        
        # 将背景色应用到所有相关组件
        self.tab_bar_container.config(bg=bg_color)
        self.tab_bar.config(bg=bg_color)
        self.tab_bar_spacer.config(bg=bg_color)
        
    def _update_background_to_result_frame_color(self):
        """更新标签栏背景色以匹配result_frame"""
        try:
            # 获取父容器（result_frame）的类名
            parent_class = self.master.winfo_class()
            
            # 对于ttk组件，使用style.lookup获取背景色
            bg_color = self.style.lookup(parent_class, 'background')
            
            # 如果获取的背景色无效，尝试获取系统默认的ttk.Frame背景色
            if not bg_color or bg_color.startswith('system.'):
                bg_color = self.style.lookup('TFrame', 'background')
            
            # 将背景色应用到所有相关组件
            self.tab_bar_container.config(bg=bg_color)
            self.tab_bar.config(bg=bg_color)
            self.tab_bar_spacer.config(bg=bg_color)
            
        except Exception as e:
            # 回退到浅灰色背景
            self.tab_bar_container.config(bg="#f0f0f0")
            self.tab_bar.config(bg="#f0f0f0")
            self.tab_bar_spacer.config(bg="#f0f0f0")
        
    def add_tab(self, label, content_frame, color="#e0e0e0"):
        """添加一个新标签"""
        tab = {
            "label": label,
            "content": content_frame,
            "color": color,
            "button": None
        }
        
        # 创建标签按钮 - 移除边框和间距，使标签栏更好地融入背景
        button = tk.Button(self.tab_bar, text=label, bg=color, 
                          relief="flat", borderwidth=0, 
                          padx=12, pady=5, font=('微软雅黑', 10, 'normal'),
                          foreground="#333333")  # 深灰色文字
        button.bind("<Button-1>", lambda e, t=len(self.tabs): self.select_tab(t))
        button.pack(side="left", padx=0, pady=0)
        
        tab["button"] = button
        self.tabs.append(tab)
        
        # 如果是第一个标签，自动选中
        if len(self.tabs) == 1:
            self.select_tab(0)
    
    def select_tab(self, tab_index):
        """选中一个标签"""
        if tab_index < 0 or tab_index >= len(self.tabs):
            return
        
        # 隐藏所有内容
        for tab in self.tabs:
            tab["content"].pack_forget()
            tab["button"].config(relief="flat", bg=tab["color"], font=('微软雅黑', 10, 'normal'), foreground="#333333")
        
        # 显示选中的标签内容 - 使用更突出的样式：颜色更深、字体加粗、无边框
        selected_tab = self.tabs[tab_index]
        selected_tab["content"].pack(fill="both", expand=True)
        
        # 为选中标签创建更突出的效果：使用更深的颜色、加粗字体
        if selected_tab["color"] == "#e3f2fd":  # 蓝色标签
            selected_color = "#bbdefb"
        elif selected_tab["color"] == "#e8f5e9":  # 绿色标签
            selected_color = "#c8e6c9"
        else:  # 紫色标签
            selected_color = "#e1bee7"
            
        selected_tab["button"].config(relief="flat", bg=selected_color, font=('微软雅黑', 10, 'bold'), foreground="#000000")
        
        # 更新对应内容框架样式的背景色，使其与选中标签的颜色保持一致
        if selected_tab["color"] == "#e3f2fd":  # 蓝色标签
            self.style.configure("LightBlue.TFrame", background=selected_color)
        elif selected_tab["color"] == "#e8f5e9":  # 绿色标签
            self.style.configure("LightGreen.TFrame", background=selected_color)
        else:  # 紫色标签
            self.style.configure("LightPurple.TFrame", background=selected_color)
        
        self.active_tab = tab_index
        
        # 调用标签页切换回调函数
        if self.tab_change_callback:
            self.tab_change_callback(tab_index)
        
    def add(self, frame, text=""):
        """模拟ttk.Notebook的add方法"""
        # 这里我们不使用这个方法，而是使用add_tab方法
        pass

class IPSubnetSplitterApp:
    def __init__(self, root):
        # 导入版本管理模块
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from version import get_version
        
        # 应用程序信息
        self.app_name = "IP子网切分工具"
        self.app_version = get_version()
        
        self.root = root
        self.root.title(f"IP子网切分工具 v{self.app_version}")
        # 所有窗口大小、位置和限制设置都由主程序入口统一管理
        # 这里只设置窗口标题
        
        # 设置样式
        self.style = ttk.Style()
        
        # 检查当前主题
        current_theme = self.style.theme_use()
        
        # 添加更详细的调试信息
        try:
            # 获取当前可用的主题
            available_themes = self.style.theme_names()
            # 尝试设置为clam主题（这个主题通常支持更多自定义样式）
            self.style.theme_use('clam')
            # 验证主题是否设置成功
            current_theme = self.style.theme_use()
        except Exception as e:
            pass

            
        self.style.configure("TLabel", font=('微软雅黑', 10))
        self.style.configure("TButton", font=('微软雅黑', 10), focuscolor="#888888", focuswidth=1)
        self.style.configure("TEntry", font=('微软雅黑', 10))
        
        # 为按钮添加焦点样式映射，进一步控制焦点效果
        self.style.map("TButton", 
                      focuscolor=[('focus', '#888888'), ('!focus', '#888888')],
                      focuswidth=[('focus', 1), ('!focus', 1)])
        
        # 恢复窗口原始背景色，使用系统默认颜色以保持界面协调
        # 不设置自定义的window_bg，让系统使用默认的背景色方案
        
        # 保持ttk组件的默认背景色，让系统主题来处理颜色协调问题
        # 只保留之前设置的字体样式，不修改背景色
        
        # 优化的标签样式设置
        try:
            # 设置Notebook的基本样式，使用更细的边框
            self.style.configure("TNotebook", background="#ffffff", borderwidth=1, relief="groove")
            
            # 使用更细的边框，确保区域分割清晰但不突兀
            self.style.configure("TLabelframe", borderwidth=1, relief="groove")
            # 增大LabelFrame标题的字体大小
            self.style.configure("TLabelframe.Label", borderwidth=0, relief="flat", font=('微软雅黑', 12))
            
            # 移除对所有标签的基础样式配置，避免干扰特定标签样式
            # 直接为每个标签样式配置完整的样式属性
            
            # 为三个标签页分别创建不同颜色的标签样式 - 现代化配色方案
            # 蓝色标签样式 - 切分网段信息
            self.style.configure("Blue.TNotebook.Tab", 
                               background="#e3f2fd",  # 浅蓝色背景
                               foreground="#1976d2",  # 深蓝色文字
                               padding=(15, 6),       # 增加内边距
                               relief="flat",         # 边框样式
                               font=('微软雅黑', 10))  # 统一字体
            
            # 蓝色标签选中状态
            self.style.map("Blue.TNotebook.Tab", 
                      background=[('selected', '#2196f3'),  # 选中时使用更鲜艳的蓝色
                                  ('!selected', '#e3f2fd')], # 非选中时的背景色
                      foreground=[('selected', 'white'),    # 选中时白色文字
                                  ('!selected', '#1976d2')]) # 非选中时的文字颜色
            
            # 绿色标签样式 - 剩余网段列表
            self.style.configure("Green.TNotebook.Tab", 
                               background="#e8f5e9",  # 浅绿色背景
                               foreground="#388e3c",  # 深绿色文字
                               padding=(15, 6),       # 增加内边距
                               relief="flat",         # 边框样式
                               font=('微软雅黑', 10))  # 统一字体
            
            # 绿色标签选中状态
            self.style.map("Green.TNotebook.Tab", 
                      background=[('selected', '#4caf50'),  # 选中时使用更鲜艳的绿色
                                  ('!selected', '#e8f5e9')], # 非选中时的背景色
                      foreground=[('selected', 'white'),    # 选中时白色文字
                                  ('!selected', '#388e3c')]) # 非选中时的文字颜色
            
            # 紫色标签样式 - 网段分布图表
            self.style.configure("Purple.TNotebook.Tab", 
                               background="#f3e5f5",  # 浅紫色背景
                               foreground="#7b1fa2",  # 深紫色文字
                               padding=(15, 6),       # 增加内边距
                               relief="flat",         # 边框样式
                               font=('微软雅黑', 10))  # 统一字体
            
            # 紫色标签选中状态
            self.style.map("Purple.TNotebook.Tab", 
                      background=[('selected', '#9c27b0'),  # 选中时使用更鲜艳的紫色
                                  ('!selected', '#f3e5f5')], # 非选中时的背景色
                      foreground=[('selected', 'white'),    # 选中时白色文字
                                  ('!selected', '#7b1fa2')]) # 非选中时的文字颜色
            
            # 添加内容框架样式，使内容区域颜色与激活标签保持一致
            self.style.configure("LightBlue.TFrame", background="#f5f9ff")  # 更浅的蓝色背景
            self.style.configure("LightGreen.TFrame", background="#f5fff7") # 更浅的绿色背景
            self.style.configure("LightPurple.TFrame", background="#fcf5ff") # 更浅的紫色背景
            
            print("标签样式设置完成")
            
        except Exception as e:
            pass
        
        # 为不同标签页的内容区域设置不同的背景色
        self.style.configure("LightBlue.TFrame", background="#e3f2fd")   # 浅蓝色 - 切分网段信息
        self.style.configure("LightGreen.TFrame", background="#e8f5e9")  # 浅绿色 - 剩余网段列表
        self.style.configure("LightPurple.TFrame", background="#f3e5f5") # 浅紫色 - 网段分布图表
        
        # 为Treeview添加明确的表格线样式配置 - 优化样式提高可读性
        # 设置Treeview的整体样式
        self.style.configure("TTreeview", 
                            background="white",  # 表格背景色
                            foreground="black",  # 文本颜色
                            rowheight=28,         # 增加行高，提高可读性
                            fieldbackground="white",  # 数据区域背景色
                            bordercolor="#e0e0e0",  # 使用浅灰色边框
                            borderwidth=1,        # 边框宽度
                            relief="solid")       # 边框样式
        
        # 设置表头样式 - 现代化设计
        self.style.configure("TTreeview.Heading", 
                            background="#1976d2",  # 使用蓝色表头背景
                            foreground="white",  # 表头文本颜色为白色
                            font=("微软雅黑", 10, "bold"),  # 表头字体
                            bordercolor="#1565c0",  # 表头边框颜色
                            borderwidth=1,        # 表头边框宽度
                            relief="solid")       # 表头边框样式
        
        # 为Treeview添加表格线和交替行颜色
        self.style.map("TTreeview", 
                      background=[("selected", "#2196f3"),  # 选中状态背景色（蓝色）
                                 ("!selected", "alternate", "#f5f5f5"),  # 交替行背景色
                                 ("!selected", "", "white")],  # 默认行背景色
                      foreground=[("selected", "white"),    # 选中状态文本颜色
                                 ("!selected", "black")],   # 默认文本颜色
                      bordercolor=[("", "#e0e0e0"),           # 默认状态边框颜色
                                 ("hover", "#bdbdbd"),        # 悬停状态边框颜色
                                 ("selected", "#1976d2")],    # 选中状态边框颜色
                      relief=[("", "solid"),                # 默认状态边框样式
                             ("hover", "solid"),           # 悬停状态边框样式
                             ("selected", "solid")])       # 选中状态边框样式
        
        # 设置表头边框样式，确保清晰可见
        self.style.map("TTreeview.Heading", 
                      background=[("", "#1976d2")],         # 表头背景色
                      foreground=[("", "white")],           # 表头文本颜色
                      bordercolor=[("", "#1565c0")],          # 表头边框颜色
                      relief=[("", "solid")])                # 表头边框样式
        
        print("Treeview表格线样式设置完成")
        
        # 先在右上角添加关于链接按钮，确保它显示在标题栏右侧
        self.create_about_link()
        
        # 创建主框架 - 调整内边距使其更加紧凑
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 再次提升关于链接的层级，确保在主框架之上
        self.about_label.lift()
        
        # 创建输入区域
        self.create_input_section()
        
        # 创建按钮区域
        self.create_button_section()
        
        # 创建结果区域
        self.create_result_section()
        
        # 初始化图表数据
        self.chart_data = None
        
    def create_input_section(self):
        """创建输入区域 - 优化布局"""
        
        input_frame = ttk.LabelFrame(self.main_frame, text="输入参数", padding="15")  # 增加内边距
        input_frame.pack(fill=tk.X, pady=(0, 10))  # 减少底部外边距
        
        # 父网段
        ttk.Label(input_frame, text="父网段 (如: 10.0.0.0/8)", anchor="e", width=22).grid(row=0, column=0, sticky=tk.E, pady=8, padx=(0, 15))
        self.parent_entry = ttk.Entry(input_frame, width=32, font=('微软雅黑', 10))
        self.parent_entry.grid(row=0, column=1, padx=0, pady=8, sticky=tk.W)
        self.parent_entry.insert(0, "10.0.0.0/8")  # 默认值
        
        # 切分网段
        ttk.Label(input_frame, text="切分网段 (如: 10.21.60.0/23)", anchor="e", width=22).grid(row=1, column=0, sticky=tk.E, pady=8, padx=(0, 15))
        self.split_entry = ttk.Entry(input_frame, width=32, font=('微软雅黑', 10))
        self.split_entry.grid(row=1, column=1, padx=0, pady=8, sticky=tk.W)
        self.split_entry.insert(0, "10.21.60.0/23")  # 默认值
        
        # 按钮区域
        # 执行按钮
        self.execute_btn = ttk.Button(input_frame, text="执行切分", command=self.execute_split, width=12)
        self.execute_btn.grid(row=0, column=2, padx=(15, 8), pady=8, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # 清空按钮
        self.clear_btn = ttk.Button(input_frame, text="清空结果", command=self.clear_result, width=12)
        self.clear_btn.grid(row=1, column=2, padx=(15, 8), pady=8, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # 导出按钮
        self.export_btn = ttk.Button(input_frame, text="导出结果", command=self.export_result, width=14)
        self.export_btn.grid(row=0, column=3, rowspan=2, padx=(0, 0), pady=8, sticky=tk.N+tk.S+tk.E+tk.W)
    
    def create_button_section(self):
        """创建按钮区域 (已合并到输入区域中)"""
        pass
    
    def adjust_remaining_tree_width(self):
        """调整剩余网段列表表格的宽度，使其自适应窗口大小"""
        # 让表格更新界面
        self.remaining_tree.update_idletasks()
        
        # 获取剩余网段框架的宽度
        frame_width = self.remaining_frame.winfo_width()
        
        # 计算每列的宽度
        total_columns = 7
        if frame_width > 0:
            # 为每列分配适当的宽度（减去滚动条和边距）
            column_width = (frame_width - 30) // total_columns  # 30为滚动条和边距留出空间
            
            # 设置每列的宽度，跳过index列（保持固定宽度）
            for col in ["cidr", "network", "netmask", "wildcard", "broadcast", "usable"]:
                self.remaining_tree.column(col, width=column_width)
            
            # 调整最后一列的宽度以填充剩余空间
            last_col_width = (frame_width - 30) - (column_width * (total_columns - 1))
            if last_col_width > 0:
                self.remaining_tree.column("usable", width=last_col_width)
    
    def on_tab_change(self, tab_index):
        """标签页切换时的处理函数"""
        # 如果切换到剩余网段列表标签页（索引为1），触发表格自适应
        if tab_index == 1:
            # 确保界面更新后再调整宽度
            self.remaining_tree.update_idletasks()
            # 调用完整的表格宽度调整方法
            self.adjust_remaining_tree_width()
    
    def create_result_section(self):
        """创建结果显示区域"""
        result_frame = ttk.LabelFrame(self.main_frame, text="切分结果", padding="10")
        # 调整底部外边距，将结果区域与窗体下边距缩小
        result_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 5))
        
        # 创建一个自定义的笔记本控件来显示不同的结果页面
        self.notebook = ColoredNotebook(result_frame, style=self.style, tab_change_callback=self.on_tab_change)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 切分网段信息页面
        self.split_info_frame = ttk.Frame(self.notebook.content_area, padding="5", style="LightBlue.TFrame")
        
        # 创建切分网段信息表格
        self.split_tree = ttk.Treeview(self.split_info_frame, columns=("item", "value"), show="headings")
        self.split_tree.heading("item", text="项目")
        self.split_tree.heading("value", text="值")
        # 设置合适的列宽
        self.split_tree.column("item", width=100, minwidth=100, stretch=False)
        self.split_tree.column("value", width=250)
        self.split_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 剩余网段列表页面
        self.remaining_frame = ttk.Frame(self.notebook.content_area, padding="5", style="LightGreen.TFrame")
        
        # 创建剩余网段信息表格
        self.remaining_tree = ttk.Treeview(self.remaining_frame, 
                                          columns=("index", "cidr", "network", "netmask", "wildcard", "broadcast", "usable"), 
                                          show="headings")
        self.remaining_tree.heading("index", text="序号")
        self.remaining_tree.heading("cidr", text="CIDR")
        self.remaining_tree.heading("network", text="网络地址")
        self.remaining_tree.heading("netmask", text="子网掩码")
        self.remaining_tree.heading("wildcard", text="通配符掩码")
        self.remaining_tree.heading("broadcast", text="广播地址")
        self.remaining_tree.heading("usable", text="可用地址数")
        
        # 设置列宽，使用minwidth替代width，让列可以自适应
        self.remaining_tree.column("index", minwidth=35, width=35, stretch=False)
        self.remaining_tree.column("cidr", minwidth=100, width=120, stretch=True)
        self.remaining_tree.column("network", minwidth=100, width=120, stretch=True)
        self.remaining_tree.column("netmask", minwidth=100, width=120, stretch=True)
        self.remaining_tree.column("wildcard", minwidth=100, width=120, stretch=True)
        
        # 网段分布图表页面
        self.chart_frame = ttk.Frame(self.notebook.content_area, padding="5", style="LightPurple.TFrame")
        
        # 添加标签页，每个标签页设置不同的颜色
        self.notebook.add_tab("切分网段信息", self.split_info_frame, "#e3f2fd")  # 浅蓝色
        self.notebook.add_tab("剩余网段列表", self.remaining_frame, "#e8f5e9")  # 浅绿色
        self.notebook.add_tab("网段分布图表", self.chart_frame, "#f3e5f5")  # 浅紫色
        
        # 创建滚动容器
        scroll_frame = ttk.Frame(self.chart_frame, style="LightPurple.TFrame")
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        self.chart_scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        self.chart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建Canvas用于绘制柱状图，移除pady边距以避免显示灰色背景
        self.chart_canvas = tk.Canvas(scroll_frame, bg="white", yscrollcommand=self.chart_scrollbar.set)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=0)
        
        # 配置滚动条
        self.chart_scrollbar.config(command=self.chart_canvas.yview)
        
        # 绑定窗口大小变化事件，实现图表自适应
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        # 绑定鼠标滚轮事件
        self.chart_canvas.bind("<MouseWheel>", self.on_chart_mousewheel)
        self.chart_frame.bind("<Enter>", lambda e: self.chart_canvas.focus_set())
        # 调整列宽，确保所有列都能完整显示并自适应窗口宽度
        self.remaining_tree.column("broadcast", minwidth=100, width=130, stretch=True)
        self.remaining_tree.column("usable", minwidth=100, width=110, stretch=True)
        
        # 添加垂直滚动条
        self.remaining_scroll_v = ttk.Scrollbar(self.remaining_frame, orient=tk.VERTICAL, command=self.remaining_tree.yview)
        self.remaining_tree.configure(yscrollcommand=self.remaining_scroll_v.set)
        
        # 设置布局：Treeview在左，垂直滚动条在右，都填满整个可用空间
        self.remaining_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        self.remaining_scroll_v.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # 绑定窗口大小变化事件，实现表格自适应
        self.root.bind("<Configure>", self.on_window_resize)
        
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
                        network.get('wildcard', ''),
                        network['broadcast'],
                        network['usable_addresses']
                    ))
            else:
                self.remaining_tree.insert("", tk.END, values=(1, "无", "无", "无", "无", "无"))
            
            # 让表格自适应窗口宽度
            self.adjust_remaining_tree_width()
            
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
                    'color': '#f3e5f5'  # 浅紫色背景
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
                    'color': '#2196f3',  # 现代蓝色
                    'type': 'split'
                })
            
            # 添加剩余网段 - 使用更现代化的颜色方案
            colors = ['#4caf50', '#ff9800', '#f44336', '#9c27b0', '#00bcd4', '#795548', '#ffeb3b', '#607d8b']  # 现代化颜色列表
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
    
    def on_chart_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.chart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def draw_text_with_stroke(self, text, x, y, font, anchor=tk.W, fill="#ffffff", stroke="#000000", stroke_width=1.5, letter_spacing=1.5):
        """绘制带描边的文字（使用4方向基础描边，平衡性能和可读性）
        
        Args:
            text: 要绘制的文字
            x: 起始x坐标
            y: 起始y坐标
            font: 字体设置
            anchor: 文字锚点
            fill: 文字颜色
            stroke: 描边颜色（为了兼容性保留此参数）
            stroke_width: 描边宽度（为了兼容性保留此参数）
            letter_spacing: 字间距（为了兼容性保留此参数）
        """
        try:
            # 使用4个方向的基础描边，平衡性能和可读性
            stroke_color = "#000000"
            offset = 1  # 描边偏移量
            
            # 绘制4个方向的描边
            self.chart_canvas.create_text(x-offset, y, text=text, font=font, anchor=anchor, fill=stroke_color)
            self.chart_canvas.create_text(x+offset, y, text=text, font=font, anchor=anchor, fill=stroke_color)
            self.chart_canvas.create_text(x, y-offset, text=text, font=font, anchor=anchor, fill=stroke_color)
            self.chart_canvas.create_text(x, y+offset, text=text, font=font, anchor=anchor, fill=stroke_color)
            
            # 绘制主文字
            self.chart_canvas.create_text(x, y, text=text, font=font, anchor=anchor, fill=fill)
        except Exception as e:
            # 出错时直接绘制文字，不添加描边
            self.chart_canvas.create_text(x, y, text=text, font=font, anchor=anchor, fill=fill)

    def draw_text_without_stroke(self, text, x, y, font, anchor=tk.W, fill="#ffffff"):
        """高效绘制不带描边的文字
        
        Args:
            text: 要绘制的文字
            x: 起始x坐标
            y: 起始y坐标
            font: 字体设置
            anchor: 文字锚点
            fill: 文字颜色
        """
        # 直接绘制文字，不添加描边
        self.chart_canvas.create_text(x, y, text=text, font=font, anchor=anchor, fill=fill)
    
    def draw_distribution_chart(self):
        """绘制网段分布柱状图 - 参考Web版本的呈现方式"""
        if not self.chart_data:
            return
        
        try:
            # 清空Canvas
            self.chart_canvas.delete("all")
            
            # 获取Canvas尺寸
            width = self.chart_canvas.winfo_width()
            canvas_height = self.chart_canvas.winfo_height()
            
            # 如果Canvas还没有渲染完成，使用默认尺寸
            if width < 10:
                width = 600
            if canvas_height < 10:
                canvas_height = 400
            
            # 设置边距（参考Web版布局）
            margin_left = 50
            margin_right = 80
            margin_top = 50
            margin_bottom = 80
            
            # 计算可用绘图区域宽度
            chart_width = width - margin_left - margin_right
            
            # 获取父网段信息
            parent_info = self.chart_data.get('parent', {})
            parent_cidr = parent_info.get('name', '')
            parent_range = parent_info.get('range', 1)
            
            # 获取网段列表
            networks = self.chart_data.get('networks', [])
            if not networks:
                # 没有网段时显示提示
                self.chart_canvas.create_text(width / 2, canvas_height / 2, 
                                             text="无网段数据", font=('微软雅黑', 12))
                return
            
            # 不绘制主标题，父网段和切分网段同等地位显示
            
            # 使用对数比例尺来更好显示差距巨大的网段大小（参考Web版算法）
            log_max = math.log10(parent_range)
            log_min = 3  # 最小显示3个数量级（1000个地址）
            min_bar_width = 50  # 小网段的最小显示宽度
            
            # 柱状图配置 - 调整为更紧凑的显示
            bar_height = 30
            padding = 10
            x = margin_left
            y = margin_top
            
            # 动态设置Canvas高度
            required_height = (y +  # 起始位置
                               (bar_height + padding) +  # 父网段
                               (bar_height + padding) +  # 切分网段
                               40 +  # 剩余网段标题
                               (len(networks) * (bar_height + padding)) +  # 所有剩余网段
                               80)  # 图例和底部边距
            
            # 确保背景色覆盖整个滚动区域，而不仅仅是初始可见区域
            background_height = max(required_height, canvas_height)
            self.chart_canvas.create_rectangle(0, 0, width, background_height, fill="#333333", outline="", width=0)
            
            # 设置Canvas滚动区域
            self.chart_canvas.config(scrollregion=(0, 0, width, background_height))
            
            # 绘制父网段
            parent_range = parent_info.get('range', 1)
            log_value = max(log_min, math.log10(parent_range))
            bar_width = max(min_bar_width, ((log_value - log_min) / (log_max - log_min)) * chart_width)
            
            # 绘制父网段条（使用明显的深灰色）
            color = '#636e72'  # 明显的深灰色
            self.chart_canvas.create_rectangle(x, y, x + bar_width, y + bar_height, 
                                               fill=color, outline="", width=0)
            
            # 绘制父网段信息
            usable_addresses = parent_range - 2 if parent_range > 2 else parent_range
            
            # 网段信息 - 使用带描边的文字绘制，提高可见度
            segment_text = f"父网段: {parent_cidr}"
            text_x = x + 15
            text_y = y + bar_height / 2
            font = ('微软雅黑', 11, 'bold')  # 使用粗体提高可读性
            # 使用带描边的文字绘制方法
            self.draw_text_with_stroke(segment_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
            
            # 可用地址数 - 使用带描边的文字绘制，提高可见度
            address_text = f"可用地址数: {usable_addresses:,}"
            text_x = x + 250
            # 使用带描边的文字绘制方法
            self.draw_text_with_stroke(address_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
            
            y += bar_height + padding
            
            # 绘制切分网段
            split_networks = [net for net in networks if net.get('type') == 'split']
            for i, network in enumerate(split_networks):
                # 使用对数比例尺计算宽度（参考Web版）
                network_range = network.get('range', 1)
                log_value = max(log_min, math.log10(network_range))
                bar_width = max(min_bar_width, ((log_value - log_min) / (log_max - log_min)) * chart_width)
                
                # 绘制切分网段条（明显的蓝色）
                color = '#4a7eb4'  # 明显的蓝色
                self.chart_canvas.create_rectangle(x, y, x + bar_width, y + bar_height, 
                                                   fill=color, outline="", width=0)
                
                # 绘制网段信息（参考Web版布局）
                name = network.get('name', '')
                usable_addresses = network_range - 2 if network_range > 2 else network_range
                
                # 网段信息 - 使用带描边的文字绘制，提高可见度
                segment_text = f"切分网段: {name}"
                text_x = x + 15
                text_y = y + bar_height / 2
                font = ('微软雅黑', 11, 'bold')  # 使用粗体提高可读性
                # 使用带描边的文字绘制方法
                self.draw_text_with_stroke(segment_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
                
                # 可用地址数 - 使用带描边的文字绘制，提高可见度
                address_text = f"可用地址数: {usable_addresses:,}"
                text_x = x + 250
                # 使用带描边的文字绘制方法
                self.draw_text_with_stroke(address_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
                
                y += bar_height + padding
                
                # 添加切分网段和剩余网段之间的虚线分割
                self.chart_canvas.create_line(x, y + 5, x + chart_width, y + 5, 
                                         fill="#cccccc", dash=(5, 2), width=1)
            
            # 绘制剩余网段标题
            y += 20  # 额外间距
            title_font = ('微软雅黑', 11)  # 调小标题字体
            remaining_count = len([n for n in networks if n.get('type') != 'split'])
            self.chart_canvas.create_text(x, y, text=f"剩余网段 ({remaining_count} 个):", 
                                         font=title_font, anchor=tk.W, fill="#ffffff")
            y += 15
            
            # 为剩余网段分配高区分度的柔和配色方案
            subnet_colors = [
                '#5e9c6a', '#db6679', '#f0ab55', '#8b6cb8', '#5b8fd9',
                '#3c70d8', '#e68838', '#a04132', '#6a9da8', '#87c569',
                '#6d8de8', '#c16fa0', '#a99bc6', '#a44d69', '#b9d0f8',
                '#5d4ea5', '#f5ad8c', '#5b8fd9', '#db6679', '#a6c589'
            ]
            
            # 绘制剩余网段
            remaining_networks = [net for net in networks if net.get('type') != 'split']
            for i, network in enumerate(remaining_networks):
                # 使用对数比例尺计算宽度
                network_range = network.get('range', 1)
                log_value = max(log_min, math.log10(network_range))
                bar_width = max(min_bar_width, ((log_value - log_min) / (log_max - log_min)) * chart_width)
                
                # 为每个剩余网段选择不同颜色（参考Web版）
                color_index = i % len(subnet_colors)
                color = subnet_colors[color_index]
                
                # 绘制剩余网段条
                self.chart_canvas.create_rectangle(x, y, x + bar_width, y + bar_height, 
                                                   fill=color, outline="", width=0)
                
                # 绘制网段信息
                name = network.get('name', '')
                usable_addresses = network_range - 2 if network_range > 2 else network_range
                
                # 网段信息 - 使用带描边的文字绘制，提高可见度
                segment_text = f"网段 {i + 1}: {name}"
                text_x = x + 15
                text_y = y + bar_height / 2
                font = ('微软雅黑', 9, 'bold')  # 使用粗体提高可读性
                # 使用带描边的文字绘制方法
                self.draw_text_with_stroke(segment_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
                
                # 可用地址数 - 使用带描边的文字绘制，提高可见度
                address_text = f"可用地址数: {usable_addresses:,}"
                text_x = x + 250
                # 使用带描边的文字绘制方法
                self.draw_text_with_stroke(address_text, text_x, text_y, font, anchor=tk.W, fill="#ffffff")
                
                y += bar_height + padding
            
            # 添加剩余网段和图例之间的虚线分割
            self.chart_canvas.create_line(x, y, x + chart_width, y, 
                                         fill="#cccccc", dash=(5, 2), width=1)
            
            # 绘制图例（参考Web版）
            legend_y = y + 15
            self.chart_canvas.create_text(x, legend_y, text="图例:", 
                                         font=('微软雅黑', 11), anchor=tk.W, fill="#ffffff")
            
            # 增加图例文字与图例图形之间的间距
            legend_items_y = legend_y + 25
            
            # 父网段图例
            self.chart_canvas.create_rectangle(x, legend_items_y, x + 20, legend_items_y + 15, 
                                               fill='#636e72')
            self.chart_canvas.create_text(x + 30, legend_items_y + 6, text="父网段", 
                                         font=('微软雅黑', 9), anchor=tk.W, fill="#ffffff")
            
            # 切分网段图例
            self.chart_canvas.create_rectangle(x + 100, legend_items_y, x + 120, legend_items_y + 12, 
                                               fill='#4a7eb4')
            self.chart_canvas.create_text(x + 130, legend_items_y + 6, text="切分网段", 
                                         font=('微软雅黑', 9), anchor=tk.W, fill="#ffffff")
            
            # 剩余网段图例（显示多彩示例，匹配高区分度配色方案）
            legend_colors = ['#5e9c6a', '#db6679', '#f0ab55', '#8b6cb8']
            for j, color in enumerate(legend_colors):
                self.chart_canvas.create_rectangle(x + 230 + j * 25, legend_items_y, 
                                                   x + 250 + j * 25, legend_items_y + 12, 
                                                   fill=color)
            
            self.chart_canvas.create_text(x + 340, legend_items_y + 6, text="剩余网段(多色)", 
                                         font=('微软雅黑', 9), anchor=tk.W, fill="#ffffff")
            
        except Exception as e:
            # 出现错误时显示提示
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width() or 600
            height = self.chart_canvas.winfo_height() or 400
            title_font = ('微软雅黑', 12, 'bold')
            self.chart_canvas.create_text(width / 2, height / 2,
                                         text=f"图表绘制失败: {str(e)}", font=title_font, fill="red")
    

    
    def on_window_resize(self, event):
        """窗口大小变化时的处理函数，实现表格和图表自适应"""
        # 确保表格能够自适应窗口宽度
        self.remaining_tree.update_idletasks()
        # 重新绘制图表以适应新的窗口大小
        self.draw_distribution_chart()
        
    def export_result(self):
        """导出结果为CSV格式"""
        try:
            # 使用更简单的文件对话框
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv")],
                title="保存子网切分结果",
                initialdir=""
            )
            
            if not file_path:
                return  # 用户取消了保存
            
            # 使用更简单的文件写入方式
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                # 写入切分网段信息
                f.write("切分网段信息,\n")
                f.write("项目,值\n")
                
                for item in self.split_tree.get_children():
                    values = self.split_tree.item(item, "values")
                    f.write(",".join(map(str, values)) + "\n")
                
                # 写入一个空行作为分隔
                f.write("\n")
                
                # 写入剩余网段信息
                f.write("剩余网段信息,\n")
                
                # 获取剩余网段表格的列标题
                headers = [self.remaining_tree.heading(col, "text") for col in self.remaining_tree["columns"]]
                f.write(",".join(headers) + "\n")
                
                for item in self.remaining_tree.get_children():
                    values = self.remaining_tree.item(item, "values")
                    f.write(",".join(map(str, values)) + "\n")
            
            # 显示导出成功信息
            self.show_result(f"结果已成功导出到: {file_path}")
            
        except Exception as e:
            # 显示导出错误信息
            self.show_result(f"导出失败: {str(e)}", error=True)

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
        
    def create_about_link(self):
        """在主窗体标题栏右侧（红框位置）创建关于链接按钮"""
        # 直接在root窗口创建关于链接，不使用框架
        # 创建链接样式的按钮
        style = ttk.Style()
        style.configure("Link.TLabel", foreground="blue", cursor="hand2")
        
        # 创建标签
        self.about_label = ttk.Label(self.root, text="关于……", style="Link.TLabel")
        
        # 放置在窗口标题栏右侧位置
        # 使用绝对定位确保在标题栏右侧可见区域
        # 将y坐标设置为15，将关于链接稍微向下移动
        self.about_label.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-30, y=15)  
        self.about_label.bind("<Button-1>", lambda e: self.show_about_dialog())
        
        # 确保在Z轴上处于最顶层，不被其他控件覆盖
        self.about_label.lift()
        
    def show_about_dialog(self):
        """显示关于对话框"""
        # 创建对话框窗口
        about_window = tk.Toplevel(self.root)
        about_window.title(f"关于 {self.app_name}")
        about_window.geometry("350x220")  # 调大窗口高度
        about_window.resizable(False, False)
        
        # 确保对话框在主窗口之上
        about_window.transient(self.root)
        about_window.grab_set()
        
        # 计算主窗口中心位置并放置窗口（跟随主窗口位置变化）
        about_window.update_idletasks()
        
        # 获取对话框的尺寸
        dialog_width = about_window.winfo_width()
        dialog_height = about_window.winfo_height()
        
        # 获取主窗口的位置和尺寸
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        # 计算对话框在主窗口中心的位置
        x = main_x + (main_width // 2) - (dialog_width // 2)
        y = main_y + (main_height // 2) - (dialog_height // 2)
        
        # 设置对话框位置
        about_window.geometry('{}x{}+{}+{}'.format(dialog_width, dialog_height, x, y))
        
        # 创建内容框架，移除所有边框和焦点指示
        content_frame = ttk.Frame(about_window, padding=(15, 0, 15, 0), relief="flat", borderwidth=0)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建上下占位框架实现内容垂直居中
        top_spacer = ttk.Frame(content_frame)
        top_spacer.pack(side="top", expand=True, fill="y")
        
        # 创建内部框架放置实际内容
        inner_frame = ttk.Frame(content_frame)
        inner_frame.pack(side="top", fill="both")
        
        bottom_spacer = ttk.Frame(content_frame)
        bottom_spacer.pack(side="top", expand=True, fill="y")
        
        # 移除对话框的焦点指示
        about_window.focus_set()
        about_window.bind("<FocusIn>", lambda e: None)
        about_window.bind("<FocusOut>", lambda e: None)
        
        # 为所有标签和按钮添加焦点样式，移除虚线
        self.style.configure("TLabel", focuscolor="none")
        self.style.configure("TButton", focuscolor="none", focuswidth=0)
        self.style.map("TButton", focuscolor=[('focus', 'none')], focuswidth=[('focus', 0)])
        
        # 标题区域
        title_frame = ttk.Frame(inner_frame)
        title_frame.pack(pady=(10, 8))
        
        # 添加应用名称作为主要标题
        app_name_label = ttk.Label(title_frame, text=self.app_name, font=('微软雅黑', 16, 'bold'))
        app_name_label.pack()
        
        # 添加版本号
        version_label = ttk.Label(title_frame, text=f"版本 {self.app_version}", font=('微软雅黑', 10))
        version_label.pack(pady=(1, 0))
        
        # 信息区域
        info_frame = ttk.Frame(inner_frame)
        info_frame.pack(pady=(0, 8))
        
        # 添加作者信息
        author_label = ttk.Label(info_frame, text="作者：Ejones", font=('微软雅黑', 10))
        author_label.pack(pady=(0, 1))
        
        # 添加联系方式
        email_label = ttk.Label(info_frame, text="邮箱：ejones.cn@hotmail.com", font=('微软雅黑', 10))
        email_label.pack()
        
        # 直接在内容框架中添加确定按钮和版权信息，不使用额外的底部框架
        # 添加确定按钮
        ok_button = ttk.Button(inner_frame, text="确定", command=about_window.destroy, width=12)
        ok_button.pack(pady=(0, 2))
        
        # 添加版权信息
        copyright_label = ttk.Label(inner_frame, text="© 2025 IP 子网分割工具", font=('微软雅黑', 8))
        copyright_label.pack(pady=(2, 10))

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口初始大小
    window_width = 800
    window_height = 600
    
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 计算窗口居中的坐标
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # 设置窗口大小和位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 设置窗口最小大小
    root.minsize(800, 400)
    
    # 禁止调整窗口宽度，但允许调整高度
    root.resizable(width=False, height=True)
    
    # 设置窗口图标
    try:
        # 尝试加载图标文件
        # 在开发环境中，图标文件位于当前目录
        # 在打包后的程序中，使用PyInstaller的资源路径
        import os
        import sys
        import tkinter as tk
        
        # 获取图标文件路径
        icon_path = None
        if hasattr(sys, '_MEIPASS'):
            # 打包后的路径
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            # 开发环境路径
            icon_path = 'icon.ico'
            
        # 确保图标文件存在
        if os.path.exists(icon_path):
            # Windows系统上设置图标的最佳实践
            # 使用iconbitmap设置窗口标题栏图标
            root.iconbitmap(default=icon_path)
            
            # 额外尝试：使用PhotoImage和iconphoto作为备选
            try:
                # 注意：PhotoImage可能无法直接处理.ico文件，需要转换
                # 这里先尝试直接加载，如果失败则忽略
                icon = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, icon)
            except Exception:
                pass  # 如果PhotoImage方法失败，继续执行
    except Exception as e:
        print(f"设置窗口图标失败: {e}")
    
    # 创建应用实例
    app = IPSubnetSplitterApp(root)
    

    
    # 运行应用
    root.mainloop()
