# 测试ipaddress模块

print("测试ipaddress模块")
try:
    import ipaddress
    print("ipaddress模块导入成功")
    
    # 测试基本功能
    try:
        net = ipaddress.IPv4Network('10.0.0.0/8')
        print(f"网络地址: {net.network_address}")
        print(f"广播地址: {net.broadcast_address}")
        print(f"前缀长度: {net.prefixlen}")
        print(f"地址总数: {net.num_addresses}")
    except Exception as e:
        print(f"ipaddress功能测试失败: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"ipaddress模块导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试其他基本功能
print("\n测试其他基本功能")
try:
    # 测试字典
    test_dict = {'a': 1, 'b': 2}
    print(f"字典测试: {test_dict.keys()}")
    
    # 测试列表
    test_list = [1, 2, 3]
    print(f"列表测试: {len(test_list)}")
    
    # 测试字符串
    test_str = "Hello, World!"
    print(f"字符串测试: {test_str.split(',')}")
    
    print("基本功能测试成功")
except Exception as e:
    print(f"基本功能测试失败: {e}")
    import traceback
    traceback.print_exc()
