#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表优化功能的脚本
"""

import tkinter as tk
from tkinter import ttk

class TestChartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图表优化测试")
        self.geometry("800x600")
        
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Canvas用于测试自适应功能
        self.chart_canvas = tk.Canvas(main_frame, bg="white")
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 绑定窗口大小变化事件
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        
        # 初始绘制测试内容
        self.draw_test_chart()
    
    def on_chart_resize(self, event):
        """Canvas尺寸变化时重新绘制图表"""
        print(f"Canvas尺寸变化: {event.width}x{event.height}")
        self.draw_test_chart()
    
    def draw_test_chart(self):
        """绘制测试图表，模拟优化后的效果"""
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
        
        # 自适应边距 - 根据Canvas尺寸动态调整
        margin_left = int(width * 0.15)  # 左侧边距占15%
        margin_right = int(width * 0.1)   # 右侧边距占10%
        margin_top = int(height * 0.1)    # 上侧边距占10%
        margin_bottom = int(height * 0.15) # 下侧边距占15%
        
        # 确保最小边距
        margin_left = max(margin_left, 50)
        margin_right = max(margin_right, 30)
        margin_top = max(margin_top, 30)
        margin_bottom = max(margin_bottom, 50)
        
        print(f"边距设置: 左={margin_left}, 右={margin_right}, 上={margin_top}, 下={margin_bottom}")
        
        # 可用绘图区域
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        # 自适应字体大小
        base_font_size = min(width, height) // 50
        label_font = ('微软雅黑', max(base_font_size, 8))
        title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
        
        print(f"字体大小: 基础={base_font_size}, 标签={label_font[1]}, 标题={title_font[1]}")
        
        # 绘制标题
        self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                     text="测试图表 - 自适应优化", font=title_font)
        
        # 绘制背景
        self.chart_canvas.create_rectangle(margin_left, margin_top, 
                                          margin_left + chart_width, 
                                          margin_top + chart_height, 
                                          fill="#f5f5f5", outline="#ccc")
        
        # 绘制示例柱状图
        bars = [
            {"name": "测试网段1", "start": 0, "end": 0.3, "color": "#3498db"},
            {"name": "测试网段2", "start": 0.3, "end": 0.6, "color": "#2ecc71"},
            {"name": "测试网段3", "start": 0.6, "end": 1.0, "color": "#e74c3c"}
        ]
        
        bar_height = chart_height / len(bars) * 0.8
        bar_spacing = chart_height / len(bars) * 0.2
        bar_height = max(bar_height, 20)
        
        for i, bar in enumerate(bars):
            # 计算柱状图位置和宽度
            x1 = margin_left + bar["start"] * chart_width
            x2 = margin_left + bar["end"] * chart_width
            y1 = margin_top + i * (bar_height + bar_spacing)
            y2 = y1 + bar_height
            
            # 绘制柱状图
            self.chart_canvas.create_rectangle(x1, y1, x2, y2, 
                                             fill=bar["color"], outline="#333", width=1)
            
            # 绘制标签
            label_x = margin_left - 10
            label_y = y1 + bar_height / 2
            self.chart_canvas.create_text(label_x, label_y, 
                                         text=bar["name"], anchor=tk.E, font=label_font)
            
            # 绘制百分比
            percentage = (bar["end"] - bar["start"]) * 100
            self.chart_canvas.create_text(margin_left + chart_width + 10, label_y, 
                                         text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
        
        # 绘制X轴标签
        self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                     text="测试地址范围", font=label_font)

if __name__ == "__main__":
    print("启动测试应用...")
    app = TestChartApp()
    print("应用启动成功，进入主循环...")
    app.mainloop()
    print("应用已退出")
