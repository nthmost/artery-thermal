from PIL import Image, ImageDraw, ImageFont
import textwrap

from .format import text_to_img, resize_image


DEFAULT_FONT = "fonts/MerchantCopy.ttf"
SOME_SPACING_VALUE = 10

class BasePrinter:
    def print_image(self, img):
        raise NotImplementedError

    def set_style(self, bold=False, underline=0):
        raise NotImplementedError

    def set_font_size(self, size):
        raise NotImplementedError

    def print_text(self, text, font_size=None, font_path=None, align="left", bold=False, underline=0):
        raise NotImplementedError

    def reset_settings(self):
        raise NotImplementedError

    def finish(self):
        raise NotImplementedError


class MockArteryPrinter(BasePrinter):

    def _ensure_space(self, additional_height):
        """Expand the main receipt image if necessary."""
        if self.y_position + additional_height > self.img.height:
            new_img = Image.new('L', (self.max_width, self.y_position + additional_height), color=255)
            new_img.paste(self.img, (0, 0))
            self.img = new_img
    
    def __init__(self, width=384, height=1000):  # Adjust height as needed
        self.img = Image.new('L', (width, height), color=255)
        self.draw = ImageDraw.Draw(self.img)
        self.y_position = 0  # Keep track of where to draw next
        
        self.max_width = 384

    def set_letter_spacing(self, spacing=0):
        """ Set the letter spacing for the printer """
        if 0 <= spacing <= 255:
            self.p.text(chr(27) + chr(32) + chr(spacing))
        else:
            raise ValueError("Spacing must be between 0 and 255")

    def print_image(self, img_path):
        img = Image.open(img_path)
        img = resize_image(img, max_width=self.max_width)
    
        # Use the image's alpha channel as the mask
        mask = img.convert("L")
    
        # Calculate the box for pasting
        right = img.width
        lower = self.y_position + img.height
        box = (0, self.y_position, right, lower)

        self.img.paste(img, box, mask)
        self.y_position += img.height + SOME_SPACING_VALUE

    def print_text(self, text, font_size="normal", font_path=None, align="left", 
            letter_spacing=None, bold=False, underline=0):
        
        # font_path will come in as None from the ReceiptText class for "normal"
        # thermal printer text, but to mock one up we need to specify a font.
        if font_path is None:
            font_path = DEFAULT_FONT
        
        # Wrap the text
        wrapped_text = "\n".join(textwrap.wrap(text, width=self.max_width))
        # Generate text as an image
        text_img = text_to_img(wrapped_text, font_path, font_size, align)
        
        # Ensure there's enough space for the image
        self._ensure_space(text_img.height)

        # Paste the text image onto the main receipt image
        self.img.paste(text_img, (0, self.y_position))

        # Update the y_position for the next item
        self.y_position += text_img.height

    def finish(self):
        self.img.save("mock_receipt.png")
        self.img.show()
