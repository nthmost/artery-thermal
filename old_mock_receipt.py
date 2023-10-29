from PIL import Image, ImageDraw, ImageFont
from artery.receipt import ExperienceReceipt
import os
import random

from experience_generator.spacy_markov import generate_experience

# Constants for Image Creation
IMAGE_MAX_WIDTH = 300
FONT_PATH = "fonts/MerchantCopy.ttf"
FONT_SIZE = 16


# Constants
IMAGE_MAX_WIDTH = 382  # Max width for the image (in pixels)


def wrap_text_line_by_line(text, width, font):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getlength(line + ' ' + words[0]) <= width:
        #while words and font.getsize(line + words[0])[0] <= width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return '\n'.join(lines)

def add_image_to_canvas(draw, img, y_offset):
    """Draws the given image on canvas at the specified y_offset."""
    img_width = min(IMAGE_MAX_WIDTH, img.width)
    img = img.resize((img_width, int((img_width / img.width) * img.height)))
    draw.bitmap((0, y_offset), img)
    return y_offset + img.height

def add_text_to_canvas(draw, font, text, y_offset):
    """Draws the given text on canvas at the specified y_offset."""
    wrapped_text = wrap_text_line_by_line(text, IMAGE_MAX_WIDTH - 20, font)
    lines = wrapped_text.split('\n')
    max_width = 0
    total_height = 0
    for line in lines:
        # this line written by ChatGPT is totally broken (this function returns int)
        #w, h = font.getlength(line)

        width = font.getlength(line)

        draw.text((10, y_offset + total_height), line, font=font, fill="black")
        max_width = max(max_width, w)
        total_height += h
    return y_offset + total_height

def create_receipt_image(receipt):
    # Initialize font
    font = ImageFont.truetype(FONT_PATH, 24)

    # Determine height of the image
    total_height = 1200
    """
    for item in receipt:
        if item['type'] == 'image':
            img = Image.open(item['data'])
            img_width = min(IMAGE_MAX_WIDTH, img.width)
            total_height += int((img_width / img.width) * img.height)
        elif item['type'] == 'text':
            wrapped_text = wrap_text_line_by_line(item['data'], IMAGE_MAX_WIDTH - 20, font)
            for line in wrapped_text.split('\n'):
                _, h = font.getsize(line)
                total_height += h
    """

    # Create canvas
    canvas = Image.new('RGB', (IMAGE_MAX_WIDTH, total_height), 'white')
    draw = ImageDraw.Draw(canvas)

    # Add items to canvas
    y_offset = 0

    for obj in receipt:
        if obj.TYPE == 'image':
            print(obj.filepath)
            img = Image.open(obj.filepath)
            y_offset = add_image_to_canvas(draw, img, y_offset)

        elif obj.TYPE == 'text': 
            #TODO: respect obj.size here
            font = ImageFont.truetype(obj.font, 24)
            if obj.align == "center":
                # TODO: separate function for centered / nonwrapped
                y_offset = add_text_to_canvas(draw, font, obj.text, y_offset)

            else:
                # longer, left-justified, wrapped
                y_offset = add_text_to_canvas(draw, font, obj.text, y_offset)

    # Save the image
    canvas.save("mock_receipt.png")


def get_random_coupon():
    return os.path.join("coupons", random.choice(os.listdir("coupons")))


def main():
    experience = generate_experience()

    coupon1 = get_random_coupon()
    coupon2 = get_random_coupon()

    mottos = ["We've got you. ;)", "Feels like home -- whether you like it or not."]

    receipt = ExperienceReceipt(experience_text=experience, coupon1=coupon1, 
                                    coupon2=coupon2, motto=random.choice(mottos))
    receipt.build_receipt()

    create_receipt_image(receipt.receipt)

if __name__ == "__main__":
    main()

