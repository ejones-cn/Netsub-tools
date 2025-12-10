@echo off
rem 停止Windows资源管理器
taskkill /f /im explorer.exe

rem 删除图标缓存文件
cd /d %userprofile%\AppData\Local
if exist IconCache.db (del /f IconCache.db)

rem 重新启动Windows资源管理器
start explorer.exe

rem 显示完成信息
echo 图标缓存已刷新！请等待几秒钟后查看图标。