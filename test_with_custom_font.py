from PIL import Image, ImageDraw, ImageFont
from escpos.printer import Usb


def text_to_img(text, font_path, font_size):
    """Convert text to an image using a specific TTF font."""
    font = ImageFont.truetype(font_path, font_size)
    width, height = font.getsize(text)
    
    # Create the actual image with the correct size
    img = Image.new('L', (width, height), color=255)
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, font=font, fill=0)
    return img


# Your printer's USB IDs
VENDOR_ID = 0x6868
PRODUCT_ID = 0x0200

# Create an image from text with a custom font
FONT_PATH = "zig.ttf"  # Adjust this to the path of your TTF font
img = text_to_img("MEGAVIBE 9000", FONT_PATH, 32)  # Adjust font size as needed

# Print the image using escpos
printer = Usb(VENDOR_ID, PRODUCT_ID)
printer.image(img)
printer.cut()
printer.close()

