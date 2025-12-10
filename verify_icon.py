import os
import struct

def check_exe_icon(exe_path):
    """检查EXE文件是否包含图标资源"""
    if not os.path.exists(exe_path):
        print(f"文件不存在: {exe_path}")
        return False
    
    print(f"检查EXE文件: {exe_path}")
    print(f"文件大小: {os.path.getsize(exe_path)} 字节")
    
    try:
        with open(exe_path, 'rb') as f:
            # 检查DOS头
            dos_header = f.read(64)
            if dos_header[:2] != b'MZ':
                print("不是有效的PE文件")
                return False
            
            # 获取PE头偏移量
            pe_offset = struct.unpack('<L', dos_header[0x3C:0x40])[0]
            
            # 读取PE头
            f.seek(pe_offset)
            pe_header = f.read(24)
            if pe_header[:2] != b'PE':
                print("不是有效的PE文件")
                return False
            
            # 获取文件头信息
            num_sections = struct.unpack('<H', pe_header[6:8])[0]
            
            # 读取节表
            section_table = f.read(40 * num_sections)
            
            # 检查资源表
            for i in range(num_sections):
                section = section_table[i*40:(i+1)*40]
                section_name = section[:8].decode('ascii', errors='replace').strip('\x00')
                if '.rsrc' in section_name:
                    print("✓ 发现资源节(.rsrc)")
                    return True
            
            print("✗ 未发现资源节(.rsrc)")
            return False
    
    except Exception as e:
        print(f"检查过程中发生错误: {e}")
        return False

# 验证我们的EXE文件
if __name__ == "__main__":
    exe_path = "dist\IP子网分割工具.exe"
    has_icon = check_exe_icon(exe_path)
    
    if has_icon:
        print("\n结论: EXE文件包含图标资源，Windows应该能显示图标。")
        print("如果仍无法显示，请尝试：")
        print("1. 等待几分钟，让Windows更新图标缓存")
        print("2. 重启Windows资源管理器")
        print("3. 将EXE文件复制到新位置")
    else:
        print("\n结论: EXE文件可能不包含图标资源。")