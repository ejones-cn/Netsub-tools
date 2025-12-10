from cx_Freeze import setup, Executable
import sys

# 创建一个可执行文件的配置
executables = [
    Executable(
        script="windows_app.py",
        base=None,  # 不使用任何基础，生成带控制台的版本
        icon="icon.ico",
        target_name="IP子网分割工具.exe"
    )
]

# 打包配置
options = {
    "build_exe": {
        "include_files": ["icon.ico"],
        "packages": ["tkinter"],
        "excludes": [],
        "optimize": 2
    }
}

# 设置项目信息
setup(
    name="IP子网分割工具",
    version="1.1.0",
    description="一个用于IP子网分割的工具",
    executables=executables,
    options=options
)