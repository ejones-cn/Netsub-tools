from ip_subnet_calculator import split_subnet

# 测试切分功能
parent = "10.0.0.0/8"
split = "10.21.60.0/23"

print(f"测试IP子网切分：")
print(f"父网段: {parent}")
print(f"切分网段: {split}")
print("=" * 50)

try:
    # 调用切分函数
    result = split_subnet(parent, split)
    
    print(f"\n执行结果：")
    print(f"result字典包含的键：{list(result.keys())}")
    
    if 'error' in result:
        print(f"错误: {result['error']}")
    else:
        print(f"\n切分网段信息：")
        if 'split_info' in result:
            split_info = result['split_info']
            print(f"  split_info包含的键：{list(split_info.keys())}")
            for key, value in split_info.items():
                print(f"  {key}: {value}")
        
        print(f"\n剩余网段信息：")
        if 'remaining_subnets_info' in result:
            print(f"  剩余网段数量：{len(result['remaining_subnets_info'])}")
            for i, subnet in enumerate(result['remaining_subnets_info'], 1):
                print(f"  网段 {i} 包含的键：{list(subnet.keys())}")
                print(f"  网段 {i} 的CIDR：{subnet.get('cidr', 'N/A')}")
                print(f"  网段 {i} 的网络地址：{subnet.get('network', 'N/A')}")
                
except Exception as e:
    print(f"\n执行过程中发生错误：")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n测试完成。")
