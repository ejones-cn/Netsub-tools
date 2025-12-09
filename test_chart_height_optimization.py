#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表高度自适应优化的脚本
"""

import tkinter as tk
from tkinter import ttk

class TestChartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图表高度自适应优化测试")
        self.geometry("800x600")
        
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建测试按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="测试10个网段", command=lambda: self.change_network_count(10)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="测试5个网段", command=lambda: self.change_network_count(5)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="测试2个网段", command=lambda: self.change_network_count(2)).pack(side=tk.LEFT, padx=5)
        
        # 创建Canvas用于测试自适应功能
        self.chart_canvas = tk.Canvas(main_frame, bg="white", borderwidth=1, relief=tk.SUNKEN)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 绑定窗口大小变化事件
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        
        # 初始绘制测试内容
        self.network_count = 5
        self.draw_test_chart()
    
    def change_network_count(self, count):
        """改变测试网段数量"""
        self.network_count = count
        self.draw_test_chart()
    
    def on_chart_resize(self, event):
        """Canvas尺寸变化时重新绘制图表"""
        print(f"Canvas尺寸变化: {event.width}x{event.height}")
        self.draw_test_chart()
    
    def draw_test_chart(self):
        """绘制测试图表，验证优化后的高度自适应效果"""
        # 清空Canvas
        self.chart_canvas.delete("all")
        
        # 获取Canvas尺寸
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        
        print(f"当前Canvas尺寸: {width}x{height}")
        
        # 如果Canvas还没有渲染完成，使用默认尺寸
        if width < 10 or height < 10:
            width = 600
            height = 400
        
        # 优化的边距策略 - 左右边距根据宽度自适应，上下边距固定
        margin_left = int(width * 0.15)  # 左侧边距占15%，用于显示标签
        margin_right = int(width * 0.1)   # 右侧边距占10%，用于显示百分比
        margin_top = 60  # 固定上边距，用于标题
        margin_bottom = 60  # 固定下边距，用于X轴标签
        
        # 确保最小边距
        margin_left = max(margin_left, 120)  # 确保有足够空间显示标签
        margin_right = max(margin_right, 60)  # 确保有足够空间显示百分比
        
        # 可用绘图区域
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        # 自适应字体大小 - 主要根据宽度调整
        base_font_size = width // 60
        label_font = ('微软雅黑', max(base_font_size, 8))
        title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
        
        print(f"字体大小: 基础={base_font_size}, 标签={label_font[1]}, 标题={title_font[1]}")
        
        # 绘制标题
        self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                     text=f"高度自适应测试 - {self.network_count}个网段", 
                                     font=title_font)
        
        # 绘制背景
        self.chart_canvas.create_rectangle(margin_left, margin_top, 
                                          margin_left + chart_width, 
                                          margin_top + chart_height, 
                                          fill="#f5f5f5", outline="#ccc")
        
        # 绘制示例网段数据
        networks = []
        for i in range(self.network_count):
            start_ratio = i * (1.0 / self.network_count)
            end_ratio = (i + 1) * (1.0 / self.network_count)
            networks.append({
                "name": f"网段{i+1}",
                "start": start_ratio,
                "end": end_ratio,
                "color": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c", "#e67e22", "#34495e", "#95a5a6", "#d35400"][i % 10]
            })
        
        # 优化的柱状图高度策略
        total_items = len(networks)
        if total_items > 0:
            # 设置固定的柱状图高度和间距
            fixed_bar_height = 30  # 固定柱状图高度
            fixed_bar_spacing = 15  # 固定柱状图间距
            
            # 计算所需的总高度
            required_height = total_items * (fixed_bar_height + fixed_bar_spacing)
            
            # 计算垂直居中的起始位置
            start_y = margin_top + (chart_height - required_height) / 2
            
            # 确保起始位置不会太靠上或太靠下
            start_y = max(start_y, margin_top + 10)
            
            print(f"柱状图设置: 高度={fixed_bar_height}, 间距={fixed_bar_spacing}, 起始Y={start_y}, 总高度={required_height}")
            
            for i, network in enumerate(networks):
                # 计算柱状图位置和宽度
                x1 = margin_left + network["start"] * chart_width
                x2 = margin_left + network["end"] * chart_width
                y1 = start_y + i * (fixed_bar_height + fixed_bar_spacing)
                y2 = y1 + fixed_bar_height
                
                # 绘制柱状图
                self.chart_canvas.create_rectangle(x1, y1, x2, y2, 
                                                 fill=network["color"], outline="#333", width=1)
                
                # 绘制标签
                label_x = margin_left - 10
                label_y = y1 + fixed_bar_height / 2
                self.chart_canvas.create_text(label_x, label_y, 
                                             text=network["name"], anchor=tk.E, font=label_font)
                
                # 绘制百分比
                percentage = (network["end"] - network["start"]) * 100
                self.chart_canvas.create_text(margin_left + chart_width + 10, label_y, 
                                             text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
        
        # 绘制X轴标签
        self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                     text="网段地址范围", font=label_font)
        
        # 绘制调试信息
        debug_text = f"Canvas: {width}x{height} | 绘图区: {chart_width}x{chart_height} | 网段: {total_items}"
        self.chart_canvas.create_text(width / 2, height - 10, text=debug_text, font=('微软雅黑', 8), fill="#666")

if __name__ == "__main__":
    print("启动图表高度自适应测试应用...")
    app = TestChartApp()
    print("应用启动成功，进入主循环...")
    app.mainloop()
    print("应用已退出")
