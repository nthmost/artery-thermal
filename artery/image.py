from PIL import Image

MAX_WIDTH = 384

def get_image_from_path(png_path, max_width=MAX_WIDTH):
    """Print a PNG image to the ESC/POS printer, resizing if necessary."""

    # Open the PNG image
    img = Image.open(png_path)

    # Resize the image if its width exceeds MAX_WIDTH
    if img.width > MAX_WIDTH:
        new_height = int(MAX_WIDTH * img.height / img.width)
        img = img.resize((MAX_WIDTH, new_height))

    return img


