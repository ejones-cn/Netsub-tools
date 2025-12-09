#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
直接测试图表绘制功能的脚本
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import traceback

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 模拟必要的数据结构
mock_chart_data = {
    'parent': {
        'start': 0,
        'end': 255,
        'range': 255,
        'color': '#e0e0e0'
    },
    'networks': [
        {
            'name': '网段1',
            'start': 0,
            'end': 63,
            'range': 64,
            'color': '#4CAF50'
        },
        {
            'name': '网段2',
            'start': 64,
            'end': 127,
            'range': 64,
            'color': '#2196F3'
        },
        {
            'name': '网段3',
            'start': 128,
            'end': 191,
            'range': 64,
            'color': '#FF9800'
        },
        {
            'name': '网段4',
            'start': 192,
            'end': 255,
            'range': 64,
            'color': '#F44336'
        }
    ]
}

class TestChartApp:
    """用于测试图表绘制的简单应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("图表绘制测试")
        self.root.geometry("800x600")
        
        # 创建图表框架
        self.chart_frame = ttk.Frame(self.root, padding="10")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Canvas
        self.chart_canvas = tk.Canvas(self.chart_frame, bg="white")
        self.chart_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 设置图表数据
        self.chart_data = mock_chart_data
        
        # 绑定尺寸变化事件
        self.chart_canvas.bind("<Configure>", self.on_chart_resize)
        
        # 初始绘制
        self.draw_distribution_chart()
    
    def on_chart_resize(self, event=None):
        """处理图表尺寸变化"""
        self.draw_distribution_chart()
    
    def draw_distribution_chart(self):
        """绘制网段分布柱状图 - 直接从windows_app.py复制的代码"""
        print("开始绘制图表...")
        if not self.chart_data:
            print("没有图表数据")
            return
        
        # 初始化安全的默认值，防止异常时变量未定义
        width = 600
        height = 400
        label_font = ('微软雅黑', 8)
        title_font = ('微软雅黑', 10, 'bold')
        margin_bottom = 60
        
        try:
            print("清空Canvas...")
            # 清空Canvas
            self.chart_canvas.delete("all")
            
            # 获取Canvas尺寸
            width = self.chart_canvas.winfo_width()
            height = self.chart_canvas.winfo_height()
            
            print(f"Canvas尺寸: {width}x{height}")
            
            # 如果Canvas还没有渲染完成，使用默认尺寸
            if width < 10 or height < 10:
                width = 600
                height = 400
                print(f"使用默认尺寸: {width}x{height}")
            
            # 优化的边距策略 - 左右边距根据宽度自适应，上下边距固定比例
            margin_left = int(width * 0.15)  # 左侧边距占15%，用于显示标签
            margin_right = int(width * 0.1)   # 右侧边距占10%，用于显示百分比
            margin_top = 60  # 固定上边距，用于标题
            margin_bottom = 60  # 固定下边距，用于X轴标签
            
            # 确保最小边距
            margin_left = max(margin_left, 120)  # 确保有足够空间显示标签
            margin_right = max(margin_right, 60)  # 确保有足够空间显示百分比
            
            print(f"边距: 左={margin_left}, 右={margin_right}, 上={margin_top}, 下={margin_bottom}")
            
            # 可用绘图区域
            chart_width = width - margin_left - margin_right
            chart_height = height - margin_top - margin_bottom
            
            print(f"绘图区域: {chart_width}x{chart_height}")
            
            # 获取父网段范围
            parent_start = self.chart_data.get('parent', {}).get('start', 0)
            parent_end = self.chart_data.get('parent', {}).get('end', 1)
            parent_range = self.chart_data.get('parent', {}).get('range', 1)
            
            print(f"父网段: 开始={parent_start}, 结束={parent_end}, 范围={parent_range}")
            
            # 计算缩放比例
            scale = chart_width / parent_range if parent_range > 0 else 1
            
            print(f"缩放比例: {scale}")
            
            # 绘制背景
            print("绘制背景...")
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, fill="#f5f5f5")
            
            # 绘制父网段背景
            parent_color = self.chart_data.get('parent', {}).get('color', '#e0e0e0')
            self.chart_canvas.create_rectangle(margin_left, margin_top, margin_left + chart_width, margin_top + chart_height, 
                                              fill=parent_color, outline="#ccc")
            
            # 获取网段列表
            networks = self.chart_data.get('networks', [])
            if not networks:
                # 没有网段时显示提示
                print("没有网段数据可显示")
                self.chart_canvas.create_text(width / 2, height / 2, 
                                             text="无网段数据", font=('微软雅黑', 12))
                return
            
            print(f"共有{len(networks)}个网段需要绘制")
            
            # 自适应字体大小 - 主要根据宽度调整
            base_font_size = width // 60
            label_font = ('微软雅黑', max(base_font_size, 8))
            title_font = ('微软雅黑', max(base_font_size + 2, 10), 'bold')
            
            print(f"字体大小: 基础={base_font_size}, 标签={label_font}, 标题={title_font}")
            
            # 绘制标题
            print("绘制标题...")
            self.chart_canvas.create_text(width / 2, margin_top / 2, 
                                         text="网段分布示意图", font=title_font)
            
            # 绘制各网段
            total_items = len(networks)
            if total_items > 0:
                print("开始绘制网段...")
                # 计算合适的柱状图高度，确保在可用高度内显示
                available_height = chart_height - 20  # 留出20px的额外空间
                min_bar_height = 20  # 最小柱状图高度
                min_bar_spacing = 10  # 最小间距
                
                print(f"可用高度: {available_height}, 最小高度: {min_bar_height}, 最小间距: {min_bar_spacing}")
                
                # 计算最大可能的柱状图高度和间距
                total_spacing = (total_items - 1) * min_bar_spacing
                max_possible_bar_height = (available_height - total_spacing) / total_items
                
                print(f"总间距: {total_spacing}, 最大可能高度: {max_possible_bar_height}")
                
                # 确定最终的柱状图高度和间距
                bar_height = max(min(max_possible_bar_height, 30), min_bar_height)  # 限制在20-30之间
                bar_spacing = min_bar_spacing  # 使用最小间距以节省空间
                
                print(f"最终柱状图高度: {bar_height}, 间距: {bar_spacing}")
                
                # 计算实际需要的高度
                required_height = total_items * bar_height + (total_items - 1) * bar_spacing
                
                # 计算垂直居中的起始位置
                start_y = margin_top + (chart_height - required_height) / 2
                
                # 确保起始位置不会越界
                start_y = max(start_y, margin_top + 10)
                
                print(f"所需高度: {required_height}, 起始Y坐标: {start_y}")
                
                for i, network in enumerate(networks):
                    print(f"绘制网段 {i+1}: {network['name']}")
                    # 计算柱状图位置和宽度
                    x1 = margin_left + (network.get('start', 0) - parent_start) * scale
                    x2 = margin_left + (network.get('end', 0) - parent_start) * scale
                    y1 = start_y + i * (bar_height + bar_spacing)
                    y2 = y1 + bar_height
                    
                    print(f"  坐标: ({x1}, {y1}) 到 ({x2}, {y2})")
                    
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
            
            print("图表绘制完成")
            
        except Exception as e:
            print(f"绘制过程中发生错误: {type(e).__name__}: {str(e)}")
            traceback.print_exc()
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
            print("绘制X轴标签...")
            self.chart_canvas.create_text(width / 2, height - margin_bottom / 2, 
                                         text="网段地址范围", font=label_font)
        except Exception as e:
            print(f"绘制X轴标签时发生错误: {type(e).__name__}: {str(e)}")
            traceback.print_exc()
            # 最后的安全保障
            pass

def main():
    print("启动测试应用程序...")
    root = tk.Tk()
    app = TestChartApp(root)
    
    # 绑定窗口关闭事件
    def on_closing():
        print("窗口关闭")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    print("应用程序启动成功，进入主循环")
    root.mainloop()
    print("应用程序退出")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("=" * 50)
        print("应用程序启动失败:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误消息: {str(e)}")
        print("\n完整堆栈跟踪:")
        traceback.print_exc()
        print("=" * 50)
        sys.exit(1)
