import os
from PIL import Image


def concat_images(img):
    """
    Copy and paste  one image three times and
    make it becomes a 2*2 image.
    """
    dst = Image.new("RGB", (img.width * 2, img.height * 2))
    dst.paste(img, (0, 0))
    dst.paste(img, (0, img.height))
    dst.paste(img, (img.width, 0))
    dst.paste(img, (img.width, img.height))

    return dst


files = [f for f in os.listdir('images/scene')]

for file in files:
    file_name = file.split('.')[0]
    origin_img = Image.open(os.path.join('images', 'scene', file_name + '.png'))
    concat_images(origin_img).save(f'big_{file_name}.bmp')
