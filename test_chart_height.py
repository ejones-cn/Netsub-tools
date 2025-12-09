#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表高度自适应功能
"""

import tkinter as tk
from tkinter import ttk
import random

class TestChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图表高度自适应测试")
        self.root.geometry("800x600")
        
        # 创建控制面板
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(control_frame, text="网段数量:").grid(row=0, column=0, padx=5)
        self.network_count = tk.IntVar(value=10)
        ttk.Entry(control_frame, textvariable=self.network_count, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="生成测试数据", command=self.generate_test_data).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="调整窗口大小", command=self.resize_window).grid(row=0, column=3, padx=5)
        
        # 创建图表Canvas
        self.chart_frame = ttk.Frame(root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chart_canvas = tk.Canvas(self.chart_frame, bg="white")
        self.chart_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定尺寸变化事件
        self.chart_canvas.bind("<Configure>", self.on_resize)
        
        # 测试数据
        self.chart_data = None
        
        # 生成默认测试数据
        self.generate_test_data()
    
    def generate_test_data(self):
        """生成测试数据"""
        count = self.network_count.get()
        
        # 父网段
        parent_start = 0
        parent_end = 10000
        parent_range = parent_end - parent_start
        
        # 生成随机网段
        networks = []
        used_ranges = []
        
        for i in range(count):
            # 随机生成不重叠的网段
            while True:
                start = random.randint(parent_start, parent_end - 10)
                length = random.randint(10, 500)
                end = start + length
                
                # 检查是否与已存在的网段重叠
                overlap = False
                for (s, e) in used_ranges:
                    if not (end <= s or start >= e):
                        overlap = True
                        break
                
                if not overlap:
                    used_ranges.append((start, end))
                    break
            
            networks.append({
                "name": f"网段{i+1}",
                "start": start,
                "end": end,
                "range": end - start,
                "color": f"#{random.randint(0, 0xFFFFFF):06x}"
            })
        
        # 按起始地址排序
        networks.sort(key=lambda x: x["start"])
        
        self.chart_data = {
            "parent": {
                "start": parent_start,
                "end": parent_end,
                "range": parent_range,
                "color": "#e0e0e0"
            },
            "networks": networks
        }
        
        # 绘制图表
        self.draw_distribution_chart()
    
    def resize_window(self):
        """调整窗口大小"""
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        
        # 随机调整窗口大小
        new_width = random.randint(600, 1000)
        new_height = random.randint(400, 800)
        
        self.root.geometry(f"{new_width}x{new_height}")
    
    def on_resize(self, event):
        """尺寸变化时重新绘制图表"""
        self.draw_distribution_chart()
    
    def draw_distribution_chart(self):
        """绘制测试图表"""
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
            
            # 边距设置
            margin_left = int(width * 0.15)
            margin_right = int(width * 0.1)
            margin_top = 60
            margin_bottom = 60
            
            margin_left = max(margin_left, 120)
            margin_right = max(margin_right, 60)
            
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
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, 
                                              fill="#f5f5f5", outline="#ccc")
            
            # 获取网段列表
            networks = self.chart_data.get('networks', [])
            if not networks:
                self.chart_canvas.create_text(width / 2, height / 2, 
                                             text="无网段数据", font=('微软雅黑', 12))
                return
            
            # 自适应字体大小
            base_font_size = width // 60
            label_font = ('微软雅黑', max(base_font_size, 8))
            title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
            
            # 绘制标题
            self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                         text="网段分布示意图", font=title_font)
            
            # 绘制各网段
            total_items = len(networks)
            
            if total_items > 0:
                # 计算合适的柱状图高度，确保在可用高度内显示
                available_height = chart_height - 20
                min_bar_height = 15  # 最小柱状图高度，减少到15px以适应更多网段
                min_bar_spacing = 5   # 最小间距，减少到5px以适应更多网段
                
                # 计算最大可能的柱状图高度和间距
                total_spacing = (total_items - 1) * min_bar_spacing
                max_possible_bar_height = (available_height - total_spacing) / total_items
                
                # 确定最终的柱状图高度和间距
                bar_height = max(max_possible_bar_height, min_bar_height)
                bar_spacing = min_bar_spacing
                
                # 计算实际需要的高度
                required_height = total_items * bar_height + (total_items - 1) * bar_spacing
                
                # 计算垂直居中的起始位置
                start_y = margin_top + (chart_height - required_height) / 2
                
                # 确保起始位置不会越界
                start_y = max(start_y, margin_top + 5)
                
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
                
                # 确保字体大小与柱状图高度匹配
                if bar_height < 20:
                    # 当柱状图高度较小时，减小字体大小
                    label_font_size = max(int(bar_height * 0.6), 6)
                    label_font = ('微软雅黑', label_font_size)
                
                for i, network in enumerate(networks):
                    # 计算柱状图位置和宽度
                    x1 = margin_left + (network.get('start', 0) - parent_start) * scale
                    x2 = margin_left + (network.get('end', 0) - parent_start) * scale
                    y1 = start_y + i * (bar_height + bar_spacing)
                    y2 = y1 + bar_height
                    
                    # 确保柱状图在可用区域内
                    y1 = min(y1, margin_top + chart_height - bar_height)
                    y2 = min(y2, margin_top + chart_height)
                    
                    # 绘制柱状图
                    color = network.get('color', '#cccccc')
                    self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333", width=1)
                    
                    # 绘制网段名称
                    label_x = max(10, margin_left - 10)
                    label_y = y1 + bar_height / 2
                    name = network.get('name', '未知')
                    self.chart_canvas.create_text(label_x, label_y, text=name, anchor=tk.E, font=label_font)
                    
                    # 绘制网段范围占比
                    percentage_x = min(width - 10, margin_left + chart_width + 10)
                    percentage = (network.get('range', 0) / parent_range * 100) if parent_range > 0 else 0
                    self.chart_canvas.create_text(percentage_x, label_y, 
                                                 text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
            
            # 绘制X轴标签
            self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                         text="网段地址范围", font=label_font)
            
        except Exception as e:
            print(f"图表绘制失败: {str(e)}")
            # 出现错误时显示提示
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width() or 600
            height = self.chart_canvas.winfo_height() or 400
            title_font = ('微软雅黑', 10, 'bold')
            self.chart_canvas.create_text(width / 2, height / 2, 
                                         text="图表绘制失败", font=title_font, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = TestChartApp(root)
    root.mainloop()
