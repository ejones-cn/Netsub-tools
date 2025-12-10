from PIL import Image, ImageDraw

# Create a new image with white background
image = Image.new('RGBA', (64, 64), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

# Draw a simple network icon
# Background circle
draw.ellipse((8, 8, 56, 56), fill=(0, 128, 255, 255))

# Inner circle
draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255, 255))

# Network nodes (4 small circles)
nodes = [
    (24, 24),  # Top left
    (40, 24),  # Top right
    (24, 40),  # Bottom left
    (40, 40)   # Bottom right
]

for x, y in nodes:
    draw.ellipse((x-4, y-4, x+4, y+4), fill=(0, 128, 255, 255))

# Connecting lines
draw.line((24, 24, 40, 40), fill=(0, 128, 255, 255), width=2)
draw.line((40, 24, 24, 40), fill=(0, 128, 255, 255), width=2)

# Save as ICO file
image.save('simple_icon.ico', format='ICO')
print("Simple icon created successfully!")