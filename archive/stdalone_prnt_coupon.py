from PIL import Image
from escpos.printer import Usb

MAX_WIDTH = 384

def print_png_image(png_path):
    """Print a PNG image to the ESC/POS printer, resizing if necessary."""

    # Initialize the printer
    VENDOR_ID = 0x6868
    PRODUCT_ID = 0x0200
    p = Usb(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    # Open the PNG image
    img = Image.open(png_path)

    # Resize the image if its width exceeds MAX_WIDTH
    if img.width > MAX_WIDTH:
        new_height = int(MAX_WIDTH * img.height / img.width)
        img = img.resize((MAX_WIDTH, new_height))

    # Print the image
    p.image(img)

    # Cut the paper
    p.cut()

# Usage
#print_png_image('OlGlorpy_ChewySoup_1.png')
print_png_image('coupons/Weatherman_Coupon.png')


