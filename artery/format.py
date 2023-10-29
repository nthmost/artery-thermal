from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 384



def text_to_img(text, font_path, font_size, align="left", max_width=MAX_WIDTH):
    """Convert text to an image using a specific TTF font."""
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text width
    text_width = font.getlength(text)

    # Estimate text height using sample text
    _, text_height = ImageDraw.Draw(Image.new('L', (1, 1))).multiline_textsize("gjpqy|[]", font=font)

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


def resize_image(img_path, max_width=MAX_WIDTH):
    """Returns a PNG image loaded from img_path, resizing if necessary."""

    # Open the image
    img = Image.open(img_path)

    # Resize the image if its width exceeds MAX_WIDTH
    if img.width > max_width:
        new_height = int(max_width * img.height / img.width)
        img = img.resize((max_width, new_height))

    return img
