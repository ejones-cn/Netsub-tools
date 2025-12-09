# 测试脚本，用于检查代码语法

try:
    import tkinter as tk
    from tkinter import ttk
    print("tkinter 导入成功")
    
    # 检查核心模块
    from ip_subnet_calculator import split_subnet
    print("ip_subnet_calculator 导入成功")
    
    # 简单测试split_subnet函数
    result = split_subnet('192.168.0.0/24', '192.168.0.0/25')
    print("split_subnet 函数调用成功")
    print(f"返回结果包含的键: {list(result.keys())}")
    
    # 测试Windows应用类定义
    from windows_app import IPSubnetSplitterApp
    print("IPSubnetSplitterApp 类定义成功")
    
    print("\n所有测试通过！代码语法正确。")
    
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()