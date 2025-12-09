# 简单测试split_subnet函数

# 先测试导入
print("测试导入")
try:
    from ip_subnet_calculator import split_subnet
    print("导入成功")
except Exception as e:
    print(f"导入失败: {e}")
    exit()

# 测试函数调用
print("\n测试函数调用")
try:
    result = split_subnet('10.0.0.0/8', '10.21.60.0/23')
    print("函数调用成功")
except Exception as e:
    print(f"函数调用失败: {e}")
    import traceback
    traceback.print_exc()
    exit()

# 测试返回结构
print("\n测试返回结构")
try:
    print(f"返回类型: {type(result)}")
    print(f"是否为字典: {isinstance(result, dict)}")
    
    # 检查所有必要的键是否存在
    required_keys = ['parent', 'split', 'split_info', 'remaining_subnets', 'remaining_subnets_info']
    for key in required_keys:
        if key in result:
            print(f"键 '{key}' 存在")
        else:
            print(f"键 '{key}' 不存在")
    
    # 打印值的类型
    for key in required_keys:
        if key in result:
            print(f"键 '{key}' 的类型: {type(result[key])}")
            if isinstance(result[key], list):
                print(f"键 '{key}' 的长度: {len(result[key])}")

except Exception as e:
    print(f"测试返回结构失败: {e}")
    import traceback
    traceback.print_exc()
