# 测试split_subnet函数的返回结构

from ip_subnet_calculator import split_subnet

# 测试正常情况
result = split_subnet('10.0.0.0/8', '10.21.60.0/23')
print("split_subnet返回结构:")
print(f"所有键: {list(result.keys())}")

# 打印父网段信息
print(f"父网段: {result['parent']}")

# 打印切分网段信息
print(f"切分网段: {result['split']}")
print(f"切分网段信息键: {list(result['split_info'].keys())}")

# 打印剩余网段信息
print(f"剩余网段列表: {result['remaining_subnets']}")
print(f"剩余网段信息数量: {len(result['remaining_subnets_info'])}")

if result['remaining_subnets_info']:
    print(f"剩余网段信息键: {list(result['remaining_subnets_info'][0].keys())}")
else:
    print("无剩余网段")

# 测试特殊情况（父网段等于切分网段）
print("\n测试特殊情况（父网段等于切分网段）:")
result2 = split_subnet('192.168.1.0/24', '192.168.1.0/24')
print(f"所有键: {list(result2.keys())}")
print(f"剩余网段信息数量: {len(result2['remaining_subnets_info'])}")
