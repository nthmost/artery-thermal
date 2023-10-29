from escpos.printer import Usb
from datetime import datetime
import textwrap

from .base import BasePrinter
from .format import text_to_img, resize_image


KNOWN_PRINTERS = {
        "artery": {'vendor_id': 0x6868, 'product_id': 0x0200}
}

DEFAULT_ALIGN = "left"


def get_printer(vendor_id, product_id):
    return Usb(vendor_id, product_id)


class ArteryPrinter(BasePrinter):

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
    
    FONT_SIZE_TO_MAX_CHARS = {
        'xlarge': 16,
        'large': 24,
        'medium': 28,
        'normal': 32,
        'small': 40
    }

    def __init__(self, printer="artery", **kwargs):
        self.p = get_printer(*KNOWN_PRINTERS[printer].values())
        self.max_width=384

    def print_image(self, img):
        self.p.image(resize_image(img, self.max_width))
        self.p.ln()

    def set_print_density(self, density=7, break_time=7):
        """
        Set the print density and break time for the printer.
        
        Parameters:
        - density: Print density. Value between 0 (lightest) to 7 (darkest).
        - break_time: Print break time. Value between 0 (shortest) to 7 (longest).
        """
        if not (0 <= density <= 7):
            raise ValueError("Density must be between 0 and 7 inclusive.")
        if not (0 <= break_time <= 7):
            raise ValueError("Break time must be between 0 and 7 inclusive.")

        # Construct the command
        cmd = bytes([0x1D, 0x28, 0x4C, 2, 0, 11, density, break_time])

        # Send the command to the printer
        self.p._raw(cmd)


    def set_center_alignment(self):
        """Set center alignment using raw ESC/POS commands."""
        self.p.text("\x1B\x61\x01")  # ESC a 1

    def unset_center_alignment(self):
        """Revert to left alignment using raw ESC/POS commands."""
        self.p.text("\x1B\x61\x00")  # ESC a 0

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

        #self.p.set(align=align)
        if align=="center":
            self.set_center_alignment()
        
        if font_path:
            if not font_size:
                raise Exception("print_text: You need to set font_size when using font_path keyword.")
            img = text_to_img(text, font_path, font_size)
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

        # Determine max chars per line based on font size
        max_chars = self.FONT_SIZE_TO_MAX_CHARS.get(font_size, self.FONT_SIZE_TO_MAX_CHARS['normal'])

        # Wrap the text
        wrapped_text = textwrap.fill(text, width=max_chars)

        # 3. Print text
        self.p.text(wrapped_text + "\n")

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

