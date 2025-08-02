import os

import natsort
from PIL import Image

# Set folder path and PDF output path
folder_path = r'D:\中文\作品合集\SP_XXX\我和爱豆交换了\我跟爱豆交换了2'
output_pdf_path = r'D:\中文\作品合集\SP_XXX\我和爱豆交换了\我跟爱豆交换了2.pdf'

# Get all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif','webp'))]

# Sort by filename (if images are named in order)
image_files = natsort.natsorted(image_files)

# Create an empty list to save images
images = []

# Open each image and add to list
for image_file in image_files:
    img_path = os.path.join(folder_path, image_file)
    img = Image.open(img_path)
    images.append(img.convert('RGB'))  # Convert to RGB format

# Save images as one PDF
if images:
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])

print(f"PDF已保存至 {output_pdf_path}")
