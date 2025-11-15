from PIL import Image, ImageDraw
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', 'public')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'logo.png')

size = (128, 128)
img = Image.new('RGBA', size, (0,0,0,0))
draw = ImageDraw.Draw(img)

# Draw a simple white geometric icon similar to the original SVG
# Draw top triangle
triangle = [(64, 10), (18, 42), (110, 42)]
draw.polygon(triangle, fill=(255,255,255,255))
# Draw middle chevron
chev = [(18, 58), (64, 90), (110, 58)]
draw.polygon(chev, fill=(255,255,255,255))
# Draw lower chevron
chev2 = [(18, 86), (64, 118), (110, 86)]
draw.polygon(chev2, fill=(255,255,255,255))

# Optionally add slight inner padding by drawing smaller transparent overlay to create stroke effect

img.save(out_path, 'PNG')
print(f'Created transparent logo: {out_path}')
