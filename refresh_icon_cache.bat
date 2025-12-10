@echo off
REM 清理Windows图标缓存脚本
echo 正在清理Windows图标缓存...

REM 关闭Windows资源管理器
taskkill /f /im explorer.exe

REM 删除图标缓存文件
del /a /f /q %localappdata%\IconCache.db

REM 重启Windows资源管理器
start explorer.exe

echo 图标缓存清理完成！
echo 请重启应用程序查看图标是否显示正常。
pause