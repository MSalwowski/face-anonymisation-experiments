from PIL import Image
import os

def convert_png_to_jpg(dir, out_dir, png_file):

    # Open the PNG image
    png_image = Image.open(os.path.join(dir, png_file))

    # Convert the image to RGB mode (remove alpha channel if present)
    rgb_image = png_image.convert("RGB")

    jpg_file = os.path.splitext(png_file)[0] + ".jpg"

    # Save the image in JPEG format
    rgb_image.save(os.path.join(out_dir, jpg_file), "JPEG")


dir = '../sample'
out_dir = 'jpg_sample'

image_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

for i, image_file in enumerate(image_files):
    convert_png_to_jpg(dir, out_dir, image_file)
