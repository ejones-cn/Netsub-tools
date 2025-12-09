#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ip_subnet_calculator import split_subnet, get_subnet_info, is_subnet_of

def main():
    parser = argparse.ArgumentParser(description='IP子网切分工具')
    parser.add_argument('--parent', '-p', required=True, help='父网段（如：10.0.0.0/8）')
    parser.add_argument('--split', '-s', required=True, help='要切分的子网（如：10.21.60.0/23）')
    
    args = parser.parse_args()
    parent_cidr = args.parent
    split_cidr = args.split
    
    print("=" * 60)
    print("IP子网切分工具")
    print("=" * 60)
    
    # 验证输入
    if not is_subnet_of(parent_cidr, split_cidr):
        print(f"❌ 错误: {split_cidr} 不是 {parent_cidr} 的子网")
        return
    
    # 执行切分
    result = split_subnet(parent_cidr, split_cidr)
    
    if 'error' in result:
        print(f"❌ 错误: {result['error']}")
        return
    
    # 显示结果
    print(f"父网段: {result['parent']}")
    print(f"切分网段: {result['split']}")
    
    print("\n" + "-" * 40)
    print("切分网段信息:")
    print("-" * 40)
    split_info = result['split_info']
    print(f"  网络地址: {split_info['network']}")
    print(f"  子网掩码: {split_info['netmask']}")
    print(f"  广播地址: {split_info['broadcast']}")
    print(f"  CIDR表示: {split_info['cidr']}")
    print(f"  前缀长度: {split_info['prefixlen']}")
    print(f"  地址总数: {split_info['num_addresses']}")
    print(f"  可用地址: {split_info['usable_addresses']}")
    
    remaining_count = len(result['remaining_subnets_info'])
    print(f"\n" + "-" * 40)
    print(f"剩余网段 ({remaining_count} 个):")
    print("-" * 40)
    
    for i, subnet in enumerate(result['remaining_subnets_info'], 1):
        print(f"\n网段 {i}:")
        print(f"  网络地址: {subnet['network']}")
        print(f"  子网掩码: {subnet['netmask']}")
        print(f"  广播地址: {subnet['broadcast']}")
        print(f"  CIDR表示: {subnet['cidr']}")
        print(f"  前缀长度: {subnet['prefixlen']}")
        print(f"  地址总数: {subnet['num_addresses']}")
        print(f"  可用地址: {subnet['usable_addresses']}")
    
    print("\n" + "=" * 60)
    print("切分完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
