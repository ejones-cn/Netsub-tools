Write-Host "正在运行应用程序..."
$process = Start-Process "dist\IP子网分割工具.exe" -PassThru

Write-Host "应用程序已启动，进程ID: $($process.Id)"
Write-Host "等待3秒..."
Start-Sleep -Seconds 3

# 检查进程是否仍在运行
if ($process.HasExited) {
    Write-Host "应用程序已退出，退出代码: $($process.ExitCode)"
} else {
    Write-Host "应用程序仍在运行中"
    # 可以选择终止进程用于测试
    # $process.Kill()
    # Write-Host "应用程序已被终止"
}
