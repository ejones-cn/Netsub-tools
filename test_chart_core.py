#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
直接测试图表绘制核心功能的脚本
"""

import tkinter as tk
import sys
import traceback

# 测试数据
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

# 直接测试draw_distribution_chart的核心逻辑
def test_chart_drawing():
    """测试图表绘制的核心逻辑"""
    print("开始测试图表绘制核心逻辑...")
    
    # 模拟ChartCanvas的基本功能
    class MockCanvas:
        def __init__(self, width=600, height=400):
            self.width = width
            self.height = height
            self.drawn_elements = []
            
        def winfo_width(self):
            return self.width
            
        def winfo_height(self):
            return self.height
            
        def delete(self, *args):
            self.drawn_elements = []
            
        def create_rectangle(self, x1, y1, x2, y2, **kwargs):
            self.drawn_elements.append(('rectangle', x1, y1, x2, y2, kwargs))
            
        def create_text(self, x, y, **kwargs):
            self.drawn_elements.append(('text', x, y, kwargs))
    
    # 模拟应用程序的相关属性
    class MockApp:
        def __init__(self):
            self.chart_data = mock_chart_data
            self.chart_canvas = MockCanvas()
    
    app = MockApp()
    
    # 复制核心绘制逻辑
    try:
        canvas = app.chart_canvas
        chart_data = app.chart_data
        
        # 清空Canvas
        canvas.delete("all")
        print("清空Canvas成功")
        
        # 获取Canvas尺寸
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        print(f"Canvas尺寸: {width}x{height}")
        
        # 边距设置
        margin_left = int(width * 0.15)
        margin_right = int(width * 0.1)
        margin_top = 60
        margin_bottom = 60
        print(f"边距设置: 左={margin_left}, 右={margin_right}, 上={margin_top}, 下={margin_bottom}")
        
        # 可用绘图区域
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        print(f"可用绘图区域: {chart_width}x{chart_height}")
        
        # 获取父网段范围
        parent_start = chart_data.get('parent', {}).get('start', 0)
        parent_end = chart_data.get('parent', {}).get('end', 1)
        parent_range = chart_data.get('parent', {}).get('range', 1)
        print(f"父网段: 开始={parent_start}, 结束={parent_end}, 范围={parent_range}")
        
        # 计算缩放比例
        scale = chart_width / parent_range if parent_range > 0 else 1
        print(f"缩放比例: {scale}")
        
        # 获取网段列表
        networks = chart_data.get('networks', [])
        print(f"网段数量: {len(networks)}")
        
        # 计算柱状图参数
        total_items = len(networks)
        if total_items > 0:
            available_height = chart_height - 20
            min_bar_height = 20
            min_bar_spacing = 10
            print(f"可用高度: {available_height}, 最小高度: {min_bar_height}, 最小间距: {min_bar_spacing}")
            
            total_spacing = (total_items - 1) * min_bar_spacing
            max_possible_bar_height = (available_height - total_spacing) / total_items
            print(f"总间距: {total_spacing}, 最大可能高度: {max_possible_bar_height}")
            
            bar_height = max(min(max_possible_bar_height, 30), min_bar_height)
            bar_spacing = min_bar_spacing
            print(f"柱状图参数: 高度={bar_height}, 间距={bar_spacing}")
            
            required_height = total_items * bar_height + (total_items - 1) * bar_spacing
            print(f"所需高度: {required_height}")
            
            start_y = margin_top + (chart_height - required_height) / 2
            start_y = max(start_y, margin_top + 10)
            print(f"起始Y坐标: {start_y}")
            
            # 测试绘制每个网段
            for i, network in enumerate(networks):
                x1 = margin_left + (network.get('start', 0) - parent_start) * scale
                x2 = margin_left + (network.get('end', 0) - parent_start) * scale
                y1 = start_y + i * (bar_height + bar_spacing)
                y2 = y1 + bar_height
                
                # 确保柱状图在可用区域内
                y1 = min(y1, margin_top + chart_height - bar_height)
                y2 = min(y2, margin_top + chart_height)
                
                print(f"网段 {i+1} - {network['name']}:")
                print(f"  坐标: ({x1:.2f}, {y1:.2f}) 到 ({x2:.2f}, {y2:.2f})")
                print(f"  宽度: {x2 - x1:.2f}")
                
                # 绘制柱状图
                canvas.create_rectangle(x1, y1, x2, y2, 
                                       fill=network.get('color', '#cccccc'), 
                                       outline="#333", width=1)
                
                # 绘制标签
                label_x = max(10, margin_left - 10)
                label_y = y1 + bar_height / 2
                canvas.create_text(label_x, label_y, 
                                  text=network.get('name', '未知'), 
                                  anchor='e')
                
                # 绘制百分比
                percentage_x = min(width - 10, margin_left + chart_width + 10)
                percentage = (network.get('range', 0) / parent_range * 100) if parent_range > 0 else 0
                canvas.create_text(percentage_x, label_y, 
                                  text=f"{percentage:.1f}%", 
                                  anchor='w')
        
        print(f"\n绘制完成，共创建 {len(canvas.drawn_elements)} 个元素")
        print("测试成功！")
        
    except Exception as e:
        print(f"\n测试失败: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False
    
    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("图表绘制核心逻辑测试")
    print("=" * 60)
    
    success = test_chart_drawing()
    
    print("\n" + "=" * 60)
    if success:
        print("测试通过！图表绘制核心逻辑正常工作")
    else:
        print("测试失败！图表绘制核心逻辑存在问题")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
