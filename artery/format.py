from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 384

def text_to_img(text, font_path, font_size):
    """Convert text to an image using a specific TTF font."""
    font = ImageFont.truetype(font_path, font_size)

    # this line doesn't work, so fudging it for now.
    #width, height = font.getsize(text)

    width = MAX_WIDTH
    height = 100
    
    # Create the actual image with the correct size
    img = Image.new('L', (width, height), color=255)
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, font=font, fill=0)
    return img


def resize_image(img_path, max_width=MAX_WIDTH):
    """Returns a PNG image loaded from img_path, resizing if necessary."""

    # Open the image
    img = Image.open(png_path)

    # Resize the image if its width exceeds MAX_WIDTH
    if img.width > MAX_WIDTH:
        new_height = int(MAX_WIDTH * img.height / img.width)
        img = img.resize((MAX_WIDTH, new_height))

    return img
