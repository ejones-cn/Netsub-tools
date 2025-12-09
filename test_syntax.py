# 测试脚本，检查代码语法

try:
    # 尝试导入模块
    from windows_app import IPSubnetSplitterApp
    from ip_subnet_calculator import split_subnet, ip_to_int
    
    print("模块导入成功")
    
    # 测试核心函数
    result = split_subnet('10.0.0.0/8', '10.21.60.0/23')
    print("split_subnet 函数调用成功")
    print(f"返回结果包含的键: {list(result.keys())}")
    
    # 测试IP转换函数
    ip = '192.168.1.1'
    ip_int = ip_to_int(ip)
    print(f"IP转换测试: {ip} -> {ip_int}")
    
    print("所有语法检查通过！")
    
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()