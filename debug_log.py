# 详细的错误日志脚本

import sys
import traceback
import os

# 创建日志文件
log_file = "error_log.txt"
with open(log_file, 'w') as f:
    f.write("=== 错误日志 ===\n")
    f.write(f"时间: {os.path.getmtime(__file__)}\n")
    f.write(f"Python版本: {sys.version}\n")
    f.write(f"当前目录: {os.getcwd()}\n")
    f.write("\n")

# 尝试导入模块
try:
    import tkinter as tk
    with open(log_file, 'a') as f:
        f.write("✅ tkinter导入成功\n")
except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ tkinter导入失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

try:
    import ipaddress
    with open(log_file, 'a') as f:
        f.write("✅ ipaddress导入成功\n")
except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ ipaddress导入失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

try:
    from ip_subnet_calculator import split_subnet, ip_to_int, get_subnet_info
    with open(log_file, 'a') as f:
        f.write("✅ ip_subnet_calculator导入成功\n")
except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ ip_subnet_calculator导入失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

# 尝试测试split_subnet函数
try:
    result = split_subnet('10.0.0.0/8', '10.21.60.0/23')
    with open(log_file, 'a') as f:
        f.write(f"✅ split_subnet函数调用成功\n")
        f.write(f"返回键: {list(result.keys())}\n")
except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ split_subnet函数调用失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

# 尝试测试图表数据准备
try:
    parent_info = get_subnet_info('10.0.0.0/8')
    split_info = get_subnet_info('10.21.60.0/23')
    
    # 模拟结果数据
    result = {
        'parent': '10.0.0.0/8',
        'split': '10.21.60.0/23',
        'split_info': split_info,
        'remaining_subnets_info': [get_subnet_info('10.0.0.0/10')]
    }
    
    with open(log_file, 'a') as f:
        f.write("✅ 模拟数据创建成功\n")
        f.write(f"父网段信息: {parent_info}\n")
        f.write(f"切分网段信息: {split_info}\n")

except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ 数据准备失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

# 尝试导入并运行应用程序
try:
    import windows_app
    with open(log_file, 'a') as f:
        f.write("✅ windows_app导入成功\n")
    
    # 尝试创建应用程序实例
    try:
        root = tk.Tk()
        app = windows_app.IPSubnetSplitterApp(root)
        with open(log_file, 'a') as f:
            f.write("✅ 应用程序实例创建成功\n")
        
        # 关闭窗口
        root.destroy()
    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"❌ 应用程序实例创建失败: {e}\n")
            f.write(traceback.format_exc() + "\n")
    
except Exception as e:
    with open(log_file, 'a') as f:
        f.write(f"❌ windows_app导入或运行失败: {e}\n")
        f.write(traceback.format_exc() + "\n")

with open(log_file, 'a') as f:
    f.write("\n=== 日志结束 ===\n")

print(f"错误日志已生成: {log_file}")
# 读取并显示日志内容
with open(log_file, 'r') as f:
    print(f.read())
