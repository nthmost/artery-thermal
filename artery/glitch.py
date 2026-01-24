"""Generate glitchy receipt-style patterns for thermal printer."""

import random
from PIL import Image, ImageDraw, ImageFont

# Characters commonly seen in receipt glitches
GLITCH_CHARS = [
    'a', 'n', 'C', '?', 'L', '■', '°', '=', 'ú', 'ü', 'â', 'û',
    'Ç', 'ï', 'å', 'ñ', 'É', 'ë', 'è', 'î', 'ì', 'Ñ', 'ö', 'ò',
    '¿', '¡', '█', '▓', '▒', '░', '│', '─', '┐', '└', '┘', '┌',
    '╣', '║', '╗', '╝', '┤', '├', '¢', '£', '¥', '₧', 'ƒ', 'á',
    'í', 'ó', 'ú', 'Á', 'Í', 'Ó', 'Ú', '▀', '▄', '█', '▌', '▐'
]

# Lighter set for less dense glitches
LIGHT_GLITCH_CHARS = ['a', 'n', 'C', '?', 'L', '■', '°', '=', 'ú', 'ñ', 'Ç']


def generate_glitch_pattern(width=384, height=50, density='medium'):
    """Generate a glitchy pattern image for thermal printer.

    Args:
        width: Image width in pixels (default 384 for thermal printer)
        height: Image height in pixels
        density: 'light', 'medium', or 'heavy' - how dense the glitch is

    Returns:
        PIL Image object
    """
    # Create blank white image
    img = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(img)

    # Choose character set based on density
    if density == 'light':
        chars = LIGHT_GLITCH_CHARS
        char_count = int((width / 8) * (height / 12) * 0.15)  # 15% filled
    elif density == 'heavy':
        chars = GLITCH_CHARS
        char_count = int((width / 8) * (height / 12) * 0.6)  # 60% filled
    else:  # medium
        chars = GLITCH_CHARS
        char_count = int((width / 8) * (height / 12) * 0.35)  # 35% filled

    # Try to use a monospace font, fallback to default
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 10)
    except:
        font = ImageFont.load_default()

    # Randomly place glitch characters
    for _ in range(char_count):
        x = random.randint(0, width - 10)
        y = random.randint(0, height - 12)
        char = random.choice(chars)

        # Randomly vary the character appearance
        color = random.choice([0, 32, 64, 96])  # varying shades of black/gray

        draw.text((x, y), char, fill=color, font=font)

    return img


def generate_glitch_bands(width=384, num_bands=3, band_height=40, density='medium'):
    """Generate multiple horizontal bands of glitch patterns.

    Args:
        width: Image width in pixels
        num_bands: Number of glitch bands to generate
        band_height: Height of each band
        density: 'light', 'medium', or 'heavy'

    Returns:
        List of PIL Image objects
    """
    bands = []
    for _ in range(num_bands):
        # Vary the density slightly for each band
        band_density = random.choice(['light', 'medium']) if density == 'medium' else density
        bands.append(generate_glitch_pattern(width, band_height, band_density))

    return bands


def generate_sparse_glitch_line(width=384, height=20):
    """Generate a sparse single line of glitch characters.

    Perfect for subtle separation between text and logo.
    """
    return generate_glitch_pattern(width, height, density='light')
