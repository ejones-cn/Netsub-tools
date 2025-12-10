#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IP子网切分计算器

提供IP子网切分的核心功能，包括:
1. IP地址和整数之间的转换
2. 获取子网的详细信息
3. 检查子网关系
4. 执行子网切分
"""

__version__ = "1.1.0"

import ipaddress

def ip_to_int(ip_str):
    """
    将IP地址字符串转换为整数
    """
    parts = ip_str.split('.')
    return int(parts[0]) << 24 | int(parts[1]) << 16 | int(parts[2]) << 8 | int(parts[3])

def int_to_ip(ip_int):
    """
    将整数转换为IP地址字符串
    """
    return f"{ip_int >> 24}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

def get_subnet_info(network_str):
    """
    获取子网的详细信息
    """
    try:
        network = ipaddress.IPv4Network(network_str, strict=False)
        
        # 计算通配符掩码：子网掩码的反码
        wildcard = ~int(network.netmask) & 0xFFFFFFFF
        wildcard_mask = int_to_ip(wildcard)
        
        return {
            'network': str(network.network_address),
            'netmask': str(network.netmask),
            'wildcard': wildcard_mask,
            'broadcast': str(network.broadcast_address),
            'cidr': str(network.with_prefixlen),
            'prefixlen': network.prefixlen,
            'num_addresses': network.num_addresses,
            'usable_addresses': network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
        }
    except ValueError as e:
        return {'error': str(e)}


def split_subnet(parent_cidr, split_cidr):
    """
    将split_cidr从parent_cidr中切分出来，返回剩余的子网列表
    """
    try:
        parent_net = ipaddress.IPv4Network(parent_cidr, strict=False)
        split_net = ipaddress.IPv4Network(split_cidr, strict=False)
        
        # 检查split_net是否是parent_net的子网
        if not split_net.subnet_of(parent_net):
            return {'error': f"{split_cidr} 不是 {parent_cidr} 的子网"}
        
        # 如果父网段和切分网段相同，直接返回空列表
        if parent_net == split_net:
            return {
                'parent': parent_cidr,
                'split': split_cidr,
                'remaining_subnets': [],
                'split_info': get_subnet_info(split_cidr),
                'remaining_subnets_info': []
            }
        
        # 使用Python ipaddress模块的address_exclude方法获取剩余网段
        # 这个方法会自动生成最简洁的剩余网段列表
        remaining = list(parent_net.address_exclude(split_net))
        
        # 对剩余网段按CIDR进行排序
        remaining.sort()
        
        return {
            'parent': parent_cidr,
            'split': split_cidr,
            'remaining_subnets': [str(subnet) for subnet in remaining],
            'split_info': get_subnet_info(split_cidr),
            'remaining_subnets_info': [get_subnet_info(str(subnet)) for subnet in remaining]
        }
        
    except ValueError as e:
        return {'error': str(e)}

# 测试示例
if __name__ == "__main__":
    result = split_subnet("10.0.0.0/8", "10.21.60.0/23")
    if 'error' in result:
        print(f"错误: {result['error']}")
    else:
        print(f"父网段: {result['parent']}")
        print(f"切分网段: {result['split']}")
        print("\n切分网段信息:")
        for key, value in result['split_info'].items():
            print(f"  {key}: {value}")
        print(f"\n剩余网段 ({len(result['remaining_subnets'])} 个):")
        for i, subnet in enumerate(result['remaining_subnets_info'], 1):
            print(f"\n网段 {i}:")
            for key, value in subnet.items():
                print(f"  {key}: {value}")
