# 简单的应用程序测试

import sys
import traceback

# 打印Python版本
print(f"Python版本: {sys.version}")

# 尝试导入必要的模块
print("\n尝试导入模块...")
try:
    import tkinter as tk
    print("tkinter导入成功")
except Exception as e:
    print(f"tkinter导入失败: {e}")
    traceback.print_exc()

try:
    import ipaddress
    print("ipaddress导入成功")
except Exception as e:
    print(f"ipaddress导入失败: {e}")
    traceback.print_exc()

# 尝试直接运行应用程序
print("\n尝试运行应用程序...")
try:
    import windows_app
    print("windows_app导入成功")
except Exception as e:
    print(f"windows_app导入失败: {e}")
    traceback.print_exc()

print("\n测试完成")
