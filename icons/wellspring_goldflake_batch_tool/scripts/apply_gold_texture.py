from PIL import Image, ImageChops
import sys, os

input_path = sys.argv[1]
output_path = sys.argv[2]

img = Image.open(input_path).convert("RGBA")
texture = Image.open("textures/gold_flake_texture.png").convert("RGB").resize(img.size)
background = Image.open("textures/background - 01.png").convert("RGBA").resize(img.size)

gray = img.convert("L")
mask = gray.point(lambda p: 255 if p > 190 else 0)

texture_overlay = Image.composite(texture, Image.new("RGB", img.size, (0,0,0)), mask)
texture_overlay = texture_overlay.convert("RGBA")

final = Image.alpha_composite(background, texture_overlay)
final.save(output_path)
print(f"✅ Saved: {output_path}")
