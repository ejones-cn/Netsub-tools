@echo off
chcp 65001 >nul

echo ========================================
echo       IP子网切分工具 - Web版本启动脚本
echo ========================================
echo.

REM 检查Python环境
echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误：Python未安装或未添加到环境变量中
    echo 请先安装Python并确保添加到系统PATH
    pause
    exit /b 1
)
echo Python环境正常

REM 检查并安装依赖
echo.
echo 正在检查依赖包...
python -m pip list | findstr "flask" >nul
if errorlevel 1 (
    echo 正在安装Flask依赖...
    python -m pip install flask
    if errorlevel 1 (
        echo 错误：Flask安装失败
        pause
        exit /b 1
    )
)
echo 依赖包检查完成

REM 启动Web应用
echo.
echo 正在启动Web应用...
echo 应用将在 http://localhost:5000 上运行
echo 按 Ctrl+C 停止服务器
echo.

python web_app.py

pause