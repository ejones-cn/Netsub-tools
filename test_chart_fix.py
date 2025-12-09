#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表高度和越界修复的脚本
"""

import tkinter as tk
from tkinter import ttk
import random

class TestChartFixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图表高度和越界修复测试")
        self.geometry("800x600")
        
        # 创建控制区域
        control_frame = ttk.Frame(self, padding="10")
        control_frame.pack(fill=tk.X, side=tk.TOP)
        
        # 网段数量滑块
        ttk.Label(control_frame, text="网段数量: ").pack(side=tk.LEFT, padx=5)
        self.network_count_var = tk.IntVar(value=5)
        count_scale = ttk.Scale(control_frame, from_=2, to_=20, orient=tk.HORIZONTAL, 
                               variable=self.network_count_var, command=self.on_count_change)
        count_scale.pack(side=tk.LEFT, padx=5)
        self.count_label = ttk.Label(control_frame, text="5")
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # 创建测试按钮
        ttk.Button(control_frame, text="重新生成", command=self.generate_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="重置窗口", command=self.reset_window).pack(side=tk.LEFT, padx=5)
        
        # 创建Canvas用于测试图表
        self.chart_canvas = tk.Canvas(self, bg="white", borderwidth=1, relief=tk.SUNKEN)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 绑定窗口大小变化事件
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        
        # 生成初始测试数据
        self.generate_data()
        
    def on_count_change(self, value):
        """网段数量变化时更新"""
        count = int(float(value))
        self.count_label.config(text=str(count))
        self.generate_data()
    
    def generate_data(self):
        """生成随机测试数据"""
        count = self.network_count_var.get()
        
        # 生成随机网段数据
        networks = []
        current_start = 0
        
        # 生成随机大小的网段
        for i in range(count):
            if i == count - 1:
                # 最后一个网段占剩余所有空间
                end = 1
            else:
                # 随机生成网段大小，确保有剩余空间
                size = random.uniform(0.05, (1 - current_start) / 2)
                end = current_start + size
            
            networks.append({
                'name': f'192.168.{i}.0/24',
                'start': current_start,
                'end': end,
                'range': end - current_start,
                'color': f'#{random.randint(0, 0xFFFFFF):06x}'
            })
            
            current_start = end
        
        # 保存测试数据
        self.test_data = {
            'parent': {
                'start': 0,
                'end': 1,
                'range': 1,
                'color': '#e0e0e0'
            },
            'networks': networks
        }
        
        # 绘制图表
        self.draw_test_chart()
    
    def on_chart_resize(self, event):
        """Canvas尺寸变化时重新绘制图表"""
        self.draw_test_chart()
    
    def reset_window(self):
        """重置窗口大小"""
        self.geometry("800x600")
    
    def draw_test_chart(self):
        """绘制测试图表，使用修复后的算法"""
        if not self.test_data:
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
            
            # 确保最小边距
            margin_left = max(margin_left, 120)
            margin_right = max(margin_right, 60)
            
            # 可用绘图区域
            chart_width = width - margin_left - margin_right
            chart_height = height - margin_top - margin_bottom
            
            # 获取父网段范围
            parent_start = self.test_data.get('parent', {}).get('start', 0)
            parent_end = self.test_data.get('parent', {}).get('end', 1)
            parent_range = self.test_data.get('parent', {}).get('range', 1)
            
            # 计算缩放比例
            scale = chart_width / parent_range if parent_range > 0 else 1
            
            # 绘制背景
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, fill="#f5f5f5")
            
            # 绘制父网段背景
            parent_color = self.test_data.get('parent', {}).get('color', '#e0e0e0')
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, 
                                              fill=parent_color, outline="#ccc")
            
            # 获取网段列表
            networks = self.test_data.get('networks', [])
            if not networks:
                self.chart_canvas.create_text(width / 2, height / 2, text="无网段数据", font=('微软雅黑', 12))
                return
            
            # 自适应字体大小
            base_font_size = width // 60
            label_font = ('微软雅黑', max(base_font_size, 8))
            title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
            
            # 绘制标题
            self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                         text=f"网段分布示意图 ({len(networks)}个网段)", font=title_font)
            
            # 绘制各网段 - 使用修复后的算法
            total_items = len(networks)
            if total_items > 0:
                # 计算合适的柱状图高度，确保在可用高度内显示
                available_height = chart_height - 20  # 留出20px的额外空间
                min_bar_height = 20  # 最小柱状图高度
                min_bar_spacing = 10  # 最小间距
                
                # 计算最大可能的柱状图高度
                total_spacing = (total_items - 1) * min_bar_spacing
                max_possible_bar_height = (available_height - total_spacing) / total_items if total_items > 0 else 0
                
                # 确定最终的柱状图高度和间距
                bar_height = max(min(max_possible_bar_height, 30), min_bar_height)  # 限制在20-30之间
                bar_spacing = min_bar_spacing  # 使用最小间距以节省空间
                
                # 计算实际需要的高度
                required_height = total_items * bar_height + (total_items - 1) * bar_spacing
                
                # 计算垂直居中的起始位置
                start_y = margin_top + (chart_height - required_height) / 2
                
                # 确保起始位置不会越界
                start_y = max(start_y, margin_top + 10)
                
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
                    
                    # 绘制网段名称 - 确保在Canvas范围内
                    label_x = max(10, margin_left - 10)  # 确保不超出左边界
                    label_y = y1 + bar_height / 2
                    name = network.get('name', '未知')
                    self.chart_canvas.create_text(label_x, label_y, text=name, anchor=tk.E, font=label_font)
                    
                    # 绘制网段范围占比 - 确保在Canvas范围内
                    percentage_x = min(width - 10, margin_left + chart_width + 10)  # 确保不超出右边界
                    percentage = (network.get('range', 0) / parent_range * 100) if parent_range > 0 else 0
                    self.chart_canvas.create_text(percentage_x, label_y, 
                                                 text=f"{percentage:.1f}%", anchor=tk.W, font=label_font)
            
            # 绘制X轴标签
            self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                         text="网段地址范围", font=label_font)
            
            # 绘制调试信息
            debug_text = f"Canvas: {width}x{height} | 网段: {len(networks)} | 柱状图高度: {bar_height}px"
            self.chart_canvas.create_text(width / 2, height - 10, text=debug_text, 
                                         font=('微软雅黑', 8), fill="#666")
            
        except Exception as e:
            # 出现错误时显示提示
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width() or 600
            height = self.chart_canvas.winfo_height() or 400
            self.chart_canvas.create_text(width / 2, height / 2, 
                                         text=f"图表绘制失败: {str(e)}", 
                                         font=('微软雅黑', 10), fill="red")
    
    def reset_window(self):
        """重置窗口大小"""
        self.geometry("800x600")

if __name__ == "__main__":
    print("启动图表高度和越界修复测试...")
    try:
        app = TestChartFixApp()
        app.mainloop()
    except Exception as e:
        print(f"测试应用出错: {e}")
        import traceback
        traceback.print_exc()
