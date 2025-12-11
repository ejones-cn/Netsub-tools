Write-Host "Running application..."
Start-Process "dist\IP子网分割工具.exe"
Write-Host "Application started. Checking process status..."
Start-Sleep -Seconds 2
tasklist | findstr "IP子网分割工具"
Write-Host "Test completed."
