from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 384


def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)
    

def text_to_img(text, font_path, font_size, align="left", max_width=MAX_WIDTH):
    """Convert text to an image using a specific TTF font."""
    font = ImageFont.truetype(font_path, font_size)

    # Get text dimensions
    text_width, text_height = get_text_dimensions(text, font)

    # Calculate starting position for center alignment
    if align == "center":
        start_x = (max_width - text_width) // 2
    else:
        start_x = 0

    # Create the actual image with the correct size
    img = Image.new('L', (max_width, text_height), color=255)
    d = ImageDraw.Draw(img)
    d.text((start_x, 0), text, font=font, fill=0)
    return img
    

def resize_image(img_path_or_obj, max_width=MAX_WIDTH):
    """Returns a PNG image loaded from img_path, resizing if necessary."""

    # Check if the input is a string (file path) or an image object
    if isinstance(img_path_or_obj, str):
        img = Image.open(img_path_or_obj)
    else:
        img = img_path_or_obj

    # Resize the image if its width exceeds MAX_WIDTH
    if img.width > max_width:
        new_height = int(max_width * img.height / img.width)
        img = img.resize((max_width, new_height))

    return img


