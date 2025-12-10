import struct
import zlib

# 创建一个简单的64x64图标数据
width = 64
height = 64

# 创建一个简单的网络节点图案的像素数据
pixels = []
for y in range(height):
    row = []
    for x in range(width):
        # 背景色 - 蓝色
        r, g, b, a = 52, 152, 219, 255
        
        # 中心节点 - 红色
        cx, cy, cr = width//2, height//2, 10
        if (x - cx)**2 + (y - cy)**2 <= cr**2:
            r, g, b = 231, 76, 60
        
        # 四个外围节点 - 绿色
        for (nx, ny) in [(width//2, 16), (16, height//2), (width//2, height-16), (width-16, height//2)]:
            if (x - nx)**2 + (y - ny)**2 <= 8**2:
                r, g, b = 46, 204, 113
        
        # 连接线 - 深灰色
        if (x >= width//2-1 and x <= width//2+1) and (y >= 24 and y <= 44):
            r, g, b = 44, 62, 80
        if (y >= height//2-1 and y <= height//2+1) and (x >= 24 and x <= 44):
            r, g, b = 44, 62, 80
            
        row.append((r, g, b, a))
    pixels.extend(row)

# 转换像素数据为BMP格式
# BMP文件头
bmp_header = struct.pack('<2sIHHI', 
    b'BM',  # 文件类型
    54 + 4 * width * height,  # 文件大小
    0,  # 保留
    0,  # 保留
    54  # 数据偏移
)

# BMP信息头
bmp_info_header = struct.pack('<IIIHHIIIIII', 
    40,  # 信息头大小
    width,  # 宽度
    height * 2,  # 高度（ICO需要上下翻转）
    1,  # 平面数
    32,  # 每像素位数
    0,  # 压缩类型
    4 * width * height,  # 图像大小
    2835,  # 水平分辨率
    2835,  # 垂直分辨率
    0,  # 颜色数
    0   # 重要颜色数
)

# 转换像素数据（BMP是BGRA格式，且上下翻转）
bmp_data = b''
for y in range(height-1, -1, -1):
    for x in range(width):
        r, g, b, a = pixels[y*width + x]
        bmp_data += struct.pack('<BBBB', b, g, r, a)

# 创建ICO文件
ico_file = b''

# ICO文件头
ico_header = struct.pack('<HHH', 
    0,  # 保留
    1,  # 类型（1=ICO）
    1   # 图像数
)

# ICO目录项
ico_directory = struct.pack('<BBBBHHII', 
    width,  # 宽度
    height,  # 高度
    0,  # 颜色数
    0,  # 保留
    1,  # 位数
    32,  # 每像素位数
    4 * width * height,  # 图像大小
    6 + 16  # 数据偏移
)

# 合并所有部分
ico_file = ico_header + ico_directory + bmp_header + bmp_info_header + bmp_data

# 保存为ico文件
with open('icon.ico', 'wb') as f:
    f.write(ico_file)

print('ICO图标创建成功！')