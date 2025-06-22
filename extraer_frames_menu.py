from PIL import Image, ImageSequence
import os


gif_path = "space-pixel.gif" 
gif_path = "asteroide.gif"
output_dir = "img/asteroid_frames" 
output_dir = "img/menu_fondo"


os.makedirs(output_dir, exist_ok=True)


with Image.open(gif_path) as im:
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        frame = frame.convert("RGBA")
        frame.save(os.path.join(output_dir, f"frame_{i:03}.png"))

print(f"Frames extraídos en: {output_dir}")
