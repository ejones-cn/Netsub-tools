from PIL import Image, ImageDraw

# 创建包含多种尺寸的标准Windows图标
def create_standard_icon():
    # 定义不同尺寸（Windows推荐的图标尺寸）
    sizes = [16, 32, 48, 64, 128]
    
    # 创建一个临时列表来存储所有尺寸的图像
    icon_images = []
    
    for size in sizes:
        # 创建新图像
        image = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 计算比例因子
        scale = size / 64.0
        
        # 绘制简单网络图标
        # 背景圆
        radius = int(24 * scale)
        center = size // 2
        draw.ellipse((center-radius, center-radius, center+radius, center+radius), fill=(0, 128, 255, 255))
        
        # 内圆
        inner_radius = int(16 * scale)
        draw.ellipse((center-inner_radius, center-inner_radius, center+inner_radius, center+inner_radius), fill=(255, 255, 255, 255))
        
        # 网络节点（4个小圆）
        node_radius = int(4 * scale)
        spacing = int(16 * scale)
        
        nodes = [
            (center - spacing//2, center - spacing//2),  # 左上
            (center + spacing//2, center - spacing//2),  # 右上
            (center - spacing//2, center + spacing//2),  # 左下
            (center + spacing//2, center + spacing//2)   # 右下
        ]
        
        for x, y in nodes:
            draw.ellipse((x-node_radius, y-node_radius, x+node_radius, y+node_radius), fill=(0, 128, 255, 255))
        
        # 连接线
        line_width = int(2 * scale)
        draw.line((center - spacing//2, center - spacing//2, center + spacing//2, center + spacing//2), 
                  fill=(0, 128, 255, 255), width=line_width)
        draw.line((center + spacing//2, center - spacing//2, center - spacing//2, center + spacing//2), 
                  fill=(0, 128, 255, 255), width=line_width)
        
        # 添加到图标列表
        icon_images.append(image)
    
    # 保存为ICO文件（包含所有尺寸）
    icon_images[0].save('standard_icon.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=icon_images[1:])
    print("标准Windows图标创建成功！")
    print(f"包含尺寸: {', '.join([f'{s}x{s}' for s in sizes])}")

if __name__ == "__main__":
    create_standard_icon()