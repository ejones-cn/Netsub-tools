#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
详细错误捕获测试脚本
用于捕获windows_app.py的完整错误信息
"""

import sys
import traceback
import tkinter as tk

# 确保导入路径正确
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from windows_app import SubnetCalculatorApp
    
    def main():
        print("开始启动应用程序...")
        root = tk.Tk()
        app = SubnetCalculatorApp(root)
        
        # 绑定窗口关闭事件
        def on_closing():
            print("窗口关闭")
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        print("应用程序启动成功，进入主循环")
        root.mainloop()
        print("应用程序退出")

    if __name__ == "__main__":
        main()

except Exception as e:
    print("=" * 50)
    print("捕获到严重错误:")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误消息: {str(e)}")
    print("\n完整堆栈跟踪:")
    traceback.print_exc()
    print("=" * 50)
    sys.exit(1)
