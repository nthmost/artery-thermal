"""Convert images to glitchy receipt character art."""

from PIL import Image, ImageDraw, ImageFont
import random

# Glitch characters ordered roughly by visual density (light to dark)
GLITCH_CHARS_BY_DENSITY = [
    '°', '·', '`', "'", '.', ',',  # Lightest
    'ñ', 'n', 'L', 'l', 'ı', 'i',
    'a', 'c', 'o', 'e', 'u', 'ú', 'ü', 'û',
    'C', 'Ç', '?', '¿', '=', '≡',
    '■', '▪', '▫', '□', '█', '▓', '▒', '░'  # Darkest
]


def image_to_glitch_art(image_path_or_pil, width=384, char_width=6, char_height=10, invert=False):
    """Convert an image to glitchy receipt character art.

    Args:
        image_path_or_pil: Path to image file or PIL Image object
        width: Target width in pixels (default 384 for thermal printer)
        char_width: Width of each character in pixels
        char_height: Height of each character in pixels
        invert: If True, invert the image (white becomes black)

    Returns:
        PIL Image of the character art
    """
    # Load image
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil)
    else:
        img = image_path_or_pil

    # Convert to grayscale
    img = img.convert('L')

    # Optionally invert
    if invert:
        img = Image.eval(img, lambda x: 255 - x)

    # Calculate dimensions
    num_chars_wide = width // char_width
    num_chars_high = int((img.height / img.width) * num_chars_wide * (char_width / char_height))

    # Resize image to match character grid
    img_resized = img.resize((num_chars_wide, num_chars_high), Image.Resampling.LANCZOS)

    # Create output image
    output_height = num_chars_high * char_height
    output = Image.new('L', (width, output_height), color=255)
    draw = ImageDraw.Draw(output)

    # Load font
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 10)
    except:
        font = ImageFont.load_default()

    # Convert each pixel to a character based on brightness
    pixels = img_resized.load()
    for y in range(num_chars_high):
        for x in range(num_chars_wide):
            brightness = pixels[x, y]

            # Map brightness to character density
            # Darker pixels = denser characters
            char_index = int((1 - brightness / 255) * (len(GLITCH_CHARS_BY_DENSITY) - 1))
            char = GLITCH_CHARS_BY_DENSITY[char_index]

            # Only draw if not completely white
            if brightness < 250:
                # Add some randomness to make it glitchy
                if random.random() < 0.1:  # 10% chance of random char
                    char = random.choice(GLITCH_CHARS_BY_DENSITY)

                # Position on output
                pos_x = x * char_width
                pos_y = y * char_height

                # Draw character
                draw.text((pos_x, pos_y), char, fill=0, font=font)

    return output


def create_swan_silhouette():
    """Create a simple swan silhouette image.

    Returns:
        PIL Image of a swan
    """
    # Create a simple swan shape
    width, height = 200, 200
    img = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(img)

    # Swan body (ellipse)
    draw.ellipse([60, 100, 140, 160], fill=0)

    # Swan neck (curved path approximated with multiple circles)
    neck_points = [
        (90, 100), (85, 90), (80, 80), (75, 70),
        (70, 60), (68, 50), (70, 40), (75, 35)
    ]
    for i, (x, y) in enumerate(neck_points):
        size = 12 - i * 0.5
        draw.ellipse([x - size/2, y - size/2, x + size/2, y + size/2], fill=0)

    # Swan head (circle)
    draw.ellipse([70, 25, 88, 43], fill=0)

    # Beak
    draw.polygon([
        (88, 33),  # base of beak
        (100, 32),  # tip
        (88, 36)   # bottom of beak
    ], fill=0)

    # Wing detail (curved lines on body)
    draw.arc([65, 105, 135, 155], 180, 360, fill=128, width=2)
    draw.arc([70, 110, 130, 150], 180, 360, fill=128, width=1)

    return img


def generate_glitch_swan(width=384):
    """Generate a glitchy receipt art swan.

    Args:
        width: Width in pixels (default 384 for thermal printer)

    Returns:
        PIL Image of glitch swan
    """
    swan = create_swan_silhouette()
    return image_to_glitch_art(swan, width=width, invert=False)
