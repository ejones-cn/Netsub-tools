#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调试用打包脚本，不使用windowed参数
"""

import os
import shutil
import sys
import subprocess

# 清理旧的打包文件
if os.path.exists("build"):
    shutil.rmtree("build")
    print("已删除 build 目录")
if os.path.exists("dist_debug"):
    shutil.rmtree("dist_debug")
    print("已删除 dist_debug 目录")

# 创建调试版本的打包命令
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--onefile",
    # "--windowed",  # 不使用windowed参数，这样可以看到控制台错误
    "--icon=icon.ico",
    "--name=IP子网分割工具_debug",
    "--distpath=dist_debug",
    "--workpath=build",
    "--clean",
    "--noconfirm",
    "--hidden-import=tkinter",
    "--hidden-import=reportlab",
    "--hidden-import=charset_normalizer",
    "--hidden-import=openpyxl",
    "--hidden-import=urllib",
    "--hidden-import=urllib3",
    "--hidden-import=email",
    "--add-data=icon.ico;."
]

cmd.append("windows_app.py")

# 执行打包命令
print("开始打包调试版本...")
print(f"执行命令: {' '.join(cmd)}")

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("打包成功！")
    print(f"EXE文件已生成: dist_debug\IP子网分割工具_debug.exe")
    
    # 检查文件大小
    exe_path = os.path.join("dist_debug", "IP子网分割工具_debug.exe")
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"文件大小: {size / (1024 * 1024):.2f} MB")
        
except subprocess.CalledProcessError as e:
    print(f"打包失败: {e}")
    print("标准错误:")
    print(e.stderr)
