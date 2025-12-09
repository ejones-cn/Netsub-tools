#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用于使用cx_Freeze打包IP子网分割工具的配置文件
"""

from cx_Freeze import setup, Executable
import sys

# 排除可能导致360误报的模块
excluded_modules = [
    'ssl', 'cryptography', 'pyOpenSSL', 
    'win32api', 'win32con', 'win32security',
    'hashlib', 'hmac', 'crypt',
    'http', 'urllib', 'ftplib',
    'email', 'smtplib', 'poplib', 'imaplib',
    'ctypes', '_ctypes',
    'wincertstore', 'certifi', 'winreg',
    'tcl8', 'tk8', 'http-2.9.8.tm'
]

# 设置打包选项
build_exe_options = {
    'excludes': excluded_modules,
    'optimize': 2,  # 使用更高级别的优化
    'include_msvcr': True,
    'packages': ['tkinter'],
    'include_files': [],  # 不包含额外的文件
    'zip_include_packages': '*',  # 压缩所有包
    'zip_exclude_packages': [],  # 不排除任何包
}

# 创建可执行文件配置
executables = [
    Executable(
        'windows_app.py',
        base=None,  # 使用默认基础，可能会显示控制台窗口
        target_name='IP子网分割工具.exe',
    )
]

setup(
    name='IP子网分割工具',
    version='1.0',
    description='IP子网分割工具 - 使用cx_Freeze打包',
    options={'build_exe': build_exe_options},
    executables=executables
)