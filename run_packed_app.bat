@echo off
cd /d "%~dp0"

echo 正在运行打包后的IP子网分割工具...
echo 请检查程序窗口是否正常显示以及图标是否正确
pause

dist\IP子网分割工具\IP子网分割工具.exe

if errorlevel 1 (
    echo 程序运行出错！
    pause
) else (
    echo 程序已退出
    pause
)
