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
        return {
            'network': str(network.network_address),
            'netmask': str(network.netmask),
            'broadcast': str(network.broadcast_address),
            'cidr': str(network.with_prefixlen),
            'prefixlen': network.prefixlen,
            'num_addresses': network.num_addresses,
            'usable_addresses': network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
        }
    except ValueError as e:
        return {'error': str(e)}

def is_subnet_of(parent, child):
    """
    检查child是否是parent的子网
    """
    try:
        parent_net = ipaddress.IPv4Network(parent, strict=False)
        child_net = ipaddress.IPv4Network(child, strict=False)
        return child_net.subnet_of(parent_net)
    except ValueError:
        return False

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
        
        # 获取所有可能的下一级子网
        next_prefix = parent_net.prefixlen + 1
        subnets = list(parent_net.subnets(new_prefix=next_prefix))
        
        # 递归切分直到找到包含split_net的子网
        def find_split(network):
            if network == split_net:
                return []
            elif split_net.subnet_of(network):
                next_subs = list(network.subnets(new_prefix=network.prefixlen + 1))
                results = []
                for sub in next_subs:
                    if split_net.subnet_of(sub):
                        results.extend(find_split(sub))
                    else:
                        results.append(sub)
                return results
            else:
                return [network]
        
        remaining_subnets = []
        for subnet in subnets:
            remaining_subnets.extend(find_split(subnet))
        
        # 对结果进行聚合，合并连续的子网
        def aggregate_subnets(subnets):
            if not subnets:
                return []
            
            # 按网络地址排序
            sorted_subnets = sorted(subnets, key=lambda x: int(x.network_address))
            aggregated = [sorted_subnets[0]]
            
            for subnet in sorted_subnets[1:]:
                last = aggregated[-1]
                # 检查是否可以合并
                if last.broadcast_address + 1 == subnet.network_address and last.prefixlen == subnet.prefixlen:
                    # 尝试合并
                    try:
                        merged = ipaddress.collapse_addresses([last, subnet])
                        aggregated[-1] = list(merged)[0]
                    except ValueError:
                        # 无法合并，添加到列表
                        aggregated.append(subnet)
                else:
                    aggregated.append(subnet)
            
            return aggregated
        
        aggregated_subnets = aggregate_subnets(remaining_subnets)
        
        return {
            'parent': parent_cidr,
            'split': split_cidr,
            'remaining_subnets': [str(subnet) for subnet in aggregated_subnets],
            'split_info': get_subnet_info(split_cidr),
            'remaining_subnets_info': [get_subnet_info(str(subnet)) for subnet in aggregated_subnets]
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
