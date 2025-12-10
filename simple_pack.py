#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的PyInstaller打包脚本
"""

import os
import shutil
import sys

# 清理旧的打包文件
def clean_old_builds():
    print("清理旧的打包文件...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除 {dir_name} 目录")

# 创建新的打包配置
def create_pack_config():
    print("创建打包配置...")
    
    # 使用命令行直接打包，避免spec文件的复杂配置
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # 单文件模式
        '--windowed',  # 窗口模式，无控制台
        '--icon=icon.ico',  # 指定图标
        '--name=IP子网分割工具',  # 程序名称
        '--distpath=dist',  # 输出目录
        '--workpath=build',  # 工作目录
        '--clean',  # 清理临时文件
        '--noconfirm',  # 覆盖现有文件
        '--hidden-import=tkinter',  # 确保tkinter被正确导入
        'windows_app.py'  # 主程序文件
    ]
    
    return cmd

# 执行打包命令
def run_pack(cmd):
    print("执行打包命令...")
    import subprocess
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功！")
        print("标准输出:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print("标准错误:")
        print(e.stderr)
        return False

# 测试打包结果
def test_pack_result():
    print("检查打包结果...")
    
    # 查找EXE文件
    import glob
    exe_files = glob.glob(os.path.join('dist', '**', 'IP子网分割工具.exe'), recursive=True)
    
    if exe_files:
        exe_path = exe_files[0]
        print(f"EXE文件已生成: {exe_path}")
        print(f"文件大小: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        
        # 手动复制图标文件到EXE所在目录
        icon_path = os.path.abspath('icon.ico')
        if os.path.exists(icon_path):
            import shutil
            target_icon_path = os.path.join(os.path.dirname(exe_path), 'icon.ico')
            shutil.copy2(icon_path, target_icon_path)
            print(f"图标文件已复制到: {target_icon_path}")
        
        return exe_path
    else:
        print("EXE文件未生成！")
        return None

# 主函数
def main():
    print("IP子网分割工具打包程序")
    print("=" * 40)
    
    # 清理旧文件
    clean_old_builds()
    
    # 创建并执行打包命令
    cmd = create_pack_config()
    print(f"执行命令: {' '.join(cmd)}")
    
    if run_pack(cmd):
        # 测试打包结果
        exe_path = test_pack_result()
        if exe_path:
            print("\n打包完成！您可以在以下路径找到程序:")
            print(exe_path)
        else:
            print("\n打包过程完成，但未找到生成的EXE文件。")
    else:
        print("\n打包过程失败，请检查错误信息。")

if __name__ == "__main__":
    main()
