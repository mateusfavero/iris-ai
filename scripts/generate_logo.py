from PIL import Image
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', 'public')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'logo.png')

# Create a black square PNG
size = (128, 128)
img = Image.new('RGB', size, color=(0, 0, 0))
img.save(out_path, 'PNG')
print(f'Created {out_path}')
