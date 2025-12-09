print("Hello, World!")
print("Python基本功能测试")

try:
    import sys
    print(f"Python版本: {sys.version}")
    
    import os
    print(f"当前工作目录: {os.getcwd()}")
    
    print("测试成功!")
except Exception as e:
    print(f"测试失败: {e}")
