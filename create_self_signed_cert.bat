@echo off
REM 创建自签名代码签名证书的批处理脚本
REM 此脚本使用OpenSSL创建自签名证书
REM 请确保已安装OpenSSL（下载地址：https://slproweb.com/products/Win32OpenSSL.html）

echo ================================================
echo 创建自签名代码签名证书
echo ================================================
echo.

REM 检查OpenSSL是否可用
openssl version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到OpenSSL。请先安装OpenSSL。
    echo 下载地址：https://slproweb.com/products/Win32OpenSSL.html
    pause
    exit /b 1
)

echo 1. 生成私钥...
openssl genrsa -out private.key 2048
if %errorlevel% neq 0 (
    echo 生成私钥失败！
    pause
    exit /b 1
)

echo 2. 创建证书请求文件...
openssl req -new -key private.key -out certificate.csr -subj "/CN=IP子网分割工具/O=个人开发者/C=CN"
if %errorlevel% neq 0 (
    echo 创建证书请求失败！
    pause
    exit /b 1
)

echo 3. 生成自签名证书...
openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.crt
if %errorlevel% neq 0 (
    echo 生成证书失败！
    pause
    exit /b 1
)

echo 4. 导出为PFX格式...
set /p password=请输入证书密码：
openssl pkcs12 -export -out my_signing_cert.pfx -inkey private.key -in certificate.crt -passout pass:%password%
if %errorlevel% neq 0 (
    echo 导出PFX失败！
    pause
    exit /b 1
)

echo.
echo ================================================
echo 自签名证书创建成功！
echo ================================================
echo 证书文件：my_signing_cert.pfx
echo 有效期：365天
echo 证书密码：%password%
echo.
echo 使用方法：
echo python simple_pack.py --sign --cert-path=my_signing_cert.pfx --password=%password%
echo.
echo 注意：自签名证书不会被默认信任，仅用于测试或内部使用。
echo ================================================

REM 清理临时文件
del private.key certificate.csr certificate.crt

echo 按任意键退出...
pause >nul