#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Hello, World!")
import sys
print(f"Python版本: {sys.version}")

# 尝试导入所需模块
try:
    import ipaddress
    print("ipaddress 模块导入成功")
except Exception as e:
    print(f"ipaddress 模块导入失败: {e}")

try:
    import tkinter as tk
    print("tkinter 模块导入成功")
except Exception as e:
    print(f"tkinter 模块导入失败: {e}")
