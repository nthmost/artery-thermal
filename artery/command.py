from escpos.printer import Usb
from datetime import datetime

from .format import text_to_img


KNOWN_PRINTERS = {
        "artery": {'vendor_id': 0x6868, 'product_id': 0x0200}
}

DEFAULT_ALIGN = "left"


def get_printer(vendor_id, product_id):
    return Usb(vendor_id, product_id)


class ArteryPrinter:

    FONT_MAP = {
        'xlarge': "\x1D\x21\x11",
        'large': "\x1D\x21\x10",
        'medium': "\x1D\x21\x01",
        'normal': "\x1D\x21\x00",
        'small': "\x1B\x4D\x01",  # Using Font B
        'bold': "\x1B\x45\x01",
        'underline': "\x1B\x2D\x01",
        'double_underline': "\x1B\x2D\x02"
    }

    def __init__(self, printer="artery", **kwargs):
        self.p = get_printer(*KNOWN_PRINTERS[printer].values())

    def print_image(self, img):
        self.p.image(img)
        self.p.ln()

    def set_style(self, bold=False, underline=0):
        if bold:
            self.p.text(self.FONT_MAP["bold"])

        if underline==1:
            self.p.text(self.FONT_MAP["underline"])

        if underline==2:
            self.p.text(self.FONT_MAP["double_underline"])

    def set_font_size(self, size):
        if size in self.FONT_MAP:
            self.p.text(self.FONT_MAP[size])
        else:
            raise ValueError(f"Font size '{size}' not recognized. Must be one of: xlarge, large, medium, normal, small")

    def print_text(self, text, font_size=None, font_path=None, align=DEFAULT_ALIGN, bold=False, underline=0):
        # Reset all settings at the start for a clean slate
        self.reset_settings()
        
        self.p.set(align=align)
        
        if font_path:
            if not font_size:
                raise Exception("print_text: You need to set font_size when using font_path keyword.")
            img = text_to_img(font_path, font_size)
            self.print_image(img)
            return

        # 1. Set size
        if font_size:
            self.set_font_size(font_size)
        
        # 2. Set other styles
        if bold:
            self.set_style(bold=True)
        if underline:
            self.set_style(underline=underline)
        
        # 3. Print text
        self.p.text(text + "\n")
        
        # 4. Reset to default styles and size
        self.reset_settings()
        self.p.ln()

    def reset_settings(self):
        """Reset settings to the printer's default."""
        self.p.text(self.FONT_MAP['normal'])
        self.p.text("\x1B\x45\x00")  # Turn off bold
        self.p.text("\x1B\x2D\x00")  # Turn off underline

    def finish(self):
        self.p.ln()
        self.p.cut()
        self.p.close()


class ArteryPrinterTest(ArteryPrinter):
    """ Subclass for testing purposes """

    def test_font_map(self):
        """ Print a line for each command in FONT_MAP to check which ones work """
        for size, command in self.FONT_MAP.items():
            # Set the font command
            self.p.text(command)
            # Print the size label
            self.p.text(f"Testing {size}\n")
            # Reset text size and style to default
            self.p.text("\x1D\x21\x00")
            self.p.set(bold=False)
            self.p.ln()

