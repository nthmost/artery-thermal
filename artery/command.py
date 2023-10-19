from escpos.printer import Usb
from datetime import datetime

from .fonts import text_to_img


KNOWN_PRINTERS = {
        "artery": {'vendor_id': 0x6868, 'product_id': 0x0200}
}


def get_printer(vendor_id, product_id):
    return Usb(vendor_id, product_id)


class ArteryPrinter:

    def __init__(self, printer="artery", **kwargs):
        self.printer = get_printer(KNOWN_PRINTERS[printer])

    def print_image(self, img):
        self.printer.image(img)


    def print_text(self, text, font_size=None, font=None):
        if custom_font:
            img = text_to_img(font)
            self.print_image(img)


    def finish(self):
        self.printer.cut()
        self.printer.close()



class ExperienceReceipt:
    def __init__(self, title="MEGAVIBE9000", title_font="zig.ttf", logo=None, coupon=None):
        # Setting mandatory attributes
        self.title_image = text_to_img(title, title_font)
        self.logo = logo
        self.coupon = coupon
        
        # Default values for other attributes
        self.date = None
        self.time = None
        self.header1 = None
        self.body = []
        self.header2 = None
        self.motto = None
        self.receipt_no = None

    def set_date_time(self, date=None, time=None):
        """ If date and time are not provided, use current date and time. """
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')
        self.time = time if time else datetime.now().strftime('%H:%M:%S')

    def set_header1(self, header1):
        self.header1 = header1

    def add_body_element(self, element):
        self.body.append(element)

    def set_header2(self, header2):
        self.header2 = header2

    def set_motto(self, motto):
        self.motto = motto

    def set_receipt_no(self):
        #todo: change this to 2999 epoch timestamp
        self.receipt_no = datetime.timestamp()

    def build_receipt(self):
        """ This function will build and return the document as a string (or however you want to represent it) """
        # You would format this however you'd like, this is just a basic representation.
        # Note: The actual formatting and setting font styles would depend on the library/printer you're using.
        #       Here, we're just building a conceptual string representation.
        
        receipt = []

        self.set_date_time()

        receipt.append(f"[IMAGE]{self.title_image}[/IMAGE]")
        receipt.append(f"Date: {self.date}")
        receipt.append(f"Time: {self.time}")
        receipt.append(f"[FONT size=16 bold=True]{self.header1}[/FONT]")
        
        for element in self.body:
            receipt.append(element)

        receipt.append(f"[FONT size=14]{self.header2}[/FONT]")
        receipt.append(self.motto)
        receipt.append(f"[IMAGE]{self.logo}[/IMAGE]")
        receipt.append(f"[IMAGE]{self.coupon}[/IMAGE]")
        receipt.append(f"Receipt No.: {self.receipt_no}")

        return '\n'.join(receipt)


