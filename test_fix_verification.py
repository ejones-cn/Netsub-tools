#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证窗口高度自适应修复的简单测试脚本
"""

import tkinter as tk

# 测试数据 - 模拟分割后的网段
test_data = {
    'parent': {
        'start': 0,
        'end': 1,
        'range': 1,
        'color': '#e0e0e0'
    },
    'networks': [
        {'start': 0, 'end': 0.25, 'range': 0.25, 'name': '192.168.1.0/26', 'color': '#3498db'},
        {'start': 0.25, 'end': 0.5, 'range': 0.25, 'name': '192.168.1.64/26', 'color': '#2ecc71'},
        {'start': 0.5, 'end': 0.75, 'range': 0.25, 'name': '192.168.1.128/26', 'color': '#e74c3c'},
        {'start': 0.75, 'end': 1, 'range': 0.25, 'name': '192.168.1.192/26', 'color': '#f39c12'}
    ]
}

class TestFixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("窗口高度自适应修复验证")
        self.geometry("800x600")
        
        # 创建Canvas
        self.chart_canvas = tk.Canvas(self, bg="white", borderwidth=1, relief=tk.SUNKEN)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 绑定窗口大小变化事件
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        
        # 存储图表数据
        self.chart_data = test_data
        
        # 初始绘制
        self.draw_distribution_chart()
    
    def on_chart_resize(self, event):
        """Canvas尺寸变化时重新绘制图表"""
        self.draw_distribution_chart()
    
    def draw_distribution_chart(self):
        """
        绘制网段分布柱状图 - 从windows_app.py复制的修复后的版本
        """
        if not self.chart_data:
            return
        
        try:
            # 清空Canvas
            self.chart_canvas.delete("all")
            
            # 获取Canvas尺寸
            width = self.chart_canvas.winfo_width()
            height = self.chart_canvas.winfo_height()
            
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
            
            # 获取父网段范围
            parent_start = self.chart_data.get('parent', {}).get('start', 0)
            parent_end = self.chart_data.get('parent', {}).get('end', 1)
            parent_range = self.chart_data.get('parent', {}).get('range', 1)
            
            # 计算缩放比例
            scale = chart_width / parent_range if parent_range > 0 else 1
            
            # 绘制背景
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, fill="#f5f5f5")
            
            # 绘制父网段背景
            parent_color = self.chart_data.get('parent', {}).get('color', '#e0e0e0')
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, 
                                              fill=parent_color, outline="#ccc")
            
            # 获取网段列表
            networks = self.chart_data.get('networks', [])
            if not networks:
                # 没有网段时显示提示
                self.chart_canvas.create_text(width / 2, height / 2, 
                                             text="无网段数据", font=('微软雅黑', 12))
                return
            
            # 自适应字体大小 - 主要根据宽度调整
            base_font_size = width // 60
            label_font = ('微软雅黑', max(base_font_size, 8))
            title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
            
            # 绘制标题
            self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                         text="网段分布示意图", font=title_font)
            
            # 绘制各网段
            total_items = len(networks)
            if total_items > 0:
                # 优化的柱状图高度策略
                fixed_bar_height = 30  # 固定柱状图高度
                fixed_bar_spacing = 15  # 固定柱状图间距
                
                # 计算所需的总高度
                required_height = total_items * (fixed_bar_height + fixed_bar_spacing)
                
                # 计算垂直居中的起始位置
                start_y = margin_top + (chart_height - required_height) / 2
                
                # 确保起始位置不会太靠上或太靠下
                start_y = max(start_y, margin_top + 10)
                
                for i, network in enumerate(networks):
                    # 计算柱状图位置和宽度
                    x1 = margin_left + (network.get('start', 0) - parent_start) * scale
                    x2 = margin_left + (network.get('end', 0) - parent_start) * scale
                    y1 = start_y + i * (fixed_bar_height + fixed_bar_spacing)
                    y2 = y1 + fixed_bar_height
                    
                    # 绘制柱状图
                    color = network.get('color', '#cccccc')
                    self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333", width=1)
                    
                    # 绘制网段名称
                    label_x = margin_left - 10
                    label_y = y1 + fixed_bar_height / 2  # 修复：使用fixed_bar_height而不是未定义的bar_height
                    name = network.get('name', '未知')
                    self.chart_canvas.create_text(label_x, label_y, text=name, anchor=tk.E, font=label_font)
                    
                    # 绘制网段范围占比
                    network_range = network.get('range', 0)
                    percentage = (network_range / parent_range * 100) if parent_range > 0 else 0
                    self.chart_canvas.create_text(margin_left + chart_width + 10, label_y, 
                                                 text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
        except Exception as e:
            # 出现错误时显示提示
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width() or 600
            height = self.chart_canvas.winfo_height() or 400
            title_font = ('微软雅黑', 12, 'bold')
            self.chart_canvas.create_text(width / 2, height / 2, 
                                         text="图表绘制失败", font=title_font, fill="red")
            self.chart_canvas.create_text(width / 2, height / 2 + 30, 
                                         text=str(e), font=('微软雅黑', 10), fill="#666")
        
        # 绘制X轴标签
        self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                     text="网段地址范围", font=('微软雅黑', 10))

if __name__ == "__main__":
    print("启动窗口高度自适应修复验证应用...")
    try:
        app = TestFixApp()
        print("应用启动成功，进入主循环...")
        app.mainloop()
        print("应用已退出")
    except Exception as e:
        print(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()
