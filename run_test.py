import subprocess
import time
import os

# 设置程序路径
app_path = os.path.join(os.getcwd(), "dist", "IP子网分割工具", "IP子网分割工具.exe")

print(f"尝试运行程序: {app_path}")
print(f"程序是否存在: {os.path.exists(app_path)}")

# 尝试运行程序并捕获输出
if os.path.exists(app_path):
    try:
        print("启动程序...")
        # 使用subprocess.Popen启动程序
        process = subprocess.Popen(
            [app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"程序已启动，进程ID: {process.pid}")
        
        # 等待几秒钟
        time.sleep(5)
        
        # 检查程序是否还在运行
        if process.poll() is None:
            print("程序仍在运行")
            # 终止程序
            process.terminate()
            print("程序已终止")
        else:
            print(f"程序已退出，退出码: {process.returncode}")
            # 获取输出
            stdout, stderr = process.communicate()
            if stdout:
                print(f"标准输出:\n{stdout}")
            if stderr:
                print(f"错误输出:\n{stderr}")
    except Exception as e:
        print(f"运行程序时出错: {e}")
else:
    print("程序文件不存在!")
