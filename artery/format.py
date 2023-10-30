from PIL import Image, ImageDraw, ImageFont

import textwrap

MAX_WIDTH = 384

    
FONT_MAP = {
        'xlarge': 48,
        'large': 36,
        'medium': 24,
        'normal': 14,
        'small': 10,
}
    

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)
    

def text_to_img(text, font_path, font_size, align="left", max_width=MAX_WIDTH):
    """Convert text to an image using a specific TTF font."""
    
    if isinstance(font_size, str):
        font_size = FONT_MAP[font_size]

    font = ImageFont.truetype(font_path, font_size)

    # Wrap the text if it's too wide
    wrapped_lines = textwrap.wrap(text, width=max_width, break_long_words=False)

    line_widths = [get_text_dimensions(line, font)[0] for line in wrapped_lines]
    line_heights = [get_text_dimensions(line, font)[1] for line in wrapped_lines]

    # Calculate total image height
    total_height = sum(line_heights)

    # Create the actual image with the correct size
    img = Image.new('L', (max_width, total_height), color=255)
    d = ImageDraw.Draw(img)

    # Initialize vertical position
    y_position = 0

    for i, line in enumerate(wrapped_lines):
        # Calculate starting position based on alignment
        if align == "center":
            start_x = (max_width - line_widths[i]) // 2
        elif align == "right":
            start_x = max_width - line_widths[i]
        else:  # default to left alignment
            start_x = 0

        # Draw the line on the image
        d.text((start_x, y_position), line, font=font, fill=0)

        # Update the vertical position for the next line
        y_position += line_heights[i]

    return img




def old_text_to_img(text, font_path, font_size, align="left", max_width=MAX_WIDTH):
    """Convert text to an image using a specific TTF font."""
    
    if isinstance(font_size, str):
        font_size = FONT_MAP[font_size]

    font = ImageFont.truetype(font_path, font_size)

    # Split text into lines
    lines = text.split("\n")
    line_widths = [get_text_dimensions(line, font)[0] for line in lines]
    line_heights = [get_text_dimensions(line, font)[1] for line in lines]

    # Calculate total image height
    total_height = sum(line_heights)

    # Create the actual image with the correct size
    img = Image.new('L', (max_width, total_height), color=255)
    d = ImageDraw.Draw(img)

    # Initialize vertical position
    y_position = 0

    for i, line in enumerate(lines):
        # Calculate starting position based on alignment
        if align == "center":
            start_x = (max_width - line_widths[i]) // 2
        elif align == "right":
            start_x = max_width - line_widths[i]
        else:  # default to left alignment
            start_x = 0

        # Draw the line on the image
        d.text((start_x, y_position), line, font=font, fill=0)

        # Update the vertical position for the next line
        y_position += line_heights[i]

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


