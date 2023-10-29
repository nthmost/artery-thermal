from PIL import Image, ImageDraw, ImageFont

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
    def __init__(self, width=384, height=1000):  # Adjust height as needed
        self.img = Image.new('L', (width, height), color=255)
        self.draw = ImageDraw.Draw(self.img)
        self.y_position = 0  # Keep track of where to draw next

    def print_image(self, img):
        self.img.paste(img, (0, self.y_position))
        self.y_position += img.height

    def set_style(self, bold=False, underline=0):
        # For simplicity, we'll ignore this in the mock
        pass

    def set_font_size(self, size):
        # For simplicity, we'll ignore this in the mock
        pass

    def print_text(self, text, font_size=None, font_path=None, align="left", bold=False, underline=0):
        # For simplicity, use a default font and size
        font = ImageFont.load_default()
        text_width, text_height = self.draw.textsize(text, font=font)
        
        if align == "center":
            x_position = (self.img.width - text_width) // 2
        else:
            x_position = 0

        self.draw.text((x_position, self.y_position), text, font=font, fill=0)
        self.y_position += text_height

    def reset_settings(self):
        # For simplicity, we'll ignore this in the mock
        pass

    def finish(self):
        # You can save the image or display it
        self.img.show()
