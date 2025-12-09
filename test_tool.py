# 简单测试脚本
from ip_subnet_calculator import split_subnet

print("测试IP子网切分工具...")
print("=" * 40)

# 测试用例
test_cases = [
    ("10.0.0.0/8", "10.21.60.0/23"),
    ("192.168.0.0/16", "192.168.10.0/24"),
    ("172.16.0.0/12", "172.16.1.0/24")
]

for parent, split in test_cases:
    print(f"\n测试: {split} 从 {parent} 中切分")
    print("-" * 30)
    
    result = split_subnet(parent, split)
    
    if 'error' in result:
        print(f"错误: {result['error']}")
    else:
        print(f"切分网段信息:")
        for key, value in result['split_info'].items():
            print(f"  {key}: {value}")
        
        print(f"\n剩余网段 ({len(result['remaining_subnets'])} 个):")
        for i, subnet in enumerate(result['remaining_subnets'], 1):
            print(f"  {i}. {subnet}")

print("\n" + "=" * 40)
print("测试完成！")
