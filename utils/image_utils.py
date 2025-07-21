from PIL import Image

def resize_image(image_file, size=(640, 640)):
    image = Image.open(image_file)
    image = image.resize(size)
    return image