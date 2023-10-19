from PIL import Image, ImageDraw, ImageFont

def text_to_img(text, font_path, font_size):
    """Convert text to an image using a specific TTF font."""
    font = ImageFont.truetype(font_path, font_size)
    width, height = font.getsize(text)
    
    # Create the actual image with the correct size
    img = Image.new('L', (width, height), color=255)
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, font=font, fill=0)
    return img


