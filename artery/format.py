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


def header1(text):
    preformat = "\x1D\x21\x10"


# MEGAVIBE 9000 in a very large font
p.set(align='center')
p.text("\x1D\x21\x11")  # Set text to double height and width
p.text("MEGAVIBE 9000\n")
p.text("\x1D\x21\x00")  # Reset text size to normal

p.ln()  # Line feed

# YOUR EXPERIENCE: in a smaller, but still large font
p.set(align='center', bold=True)
p.text("\x1D\x21\x10")  # Set text to double width
p.text("YOUR EXPERIENCE:\n")
p.text("\x1D\x21\x00")  # Reset text size to normal
p.set(bold=False)

p.ln()

# In a normal font
p.set(align='center')
p.text("If we now are as gods, we live in a large maintenance closet.\n")

p.ln()

# Cut the paper
p.cut()

# Close the connection
p.close()

