from datetime import datetime
from tempfile import NamedTemporaryFile
from .format import text_to_img, resize_image

DEFAULT_COMPANY = "Community Capture Corporation"
DEFAULT_MOTTO = "We've got you. ;)"
DEFAULT_LOGO = "wings.png"
DEFAULT_TITLE = "MEGAVIBE 9000"
DEFAULT_TITLE_FONT = "fonts/zig.ttf"
DEFAULT_COUPON1 = "coupons/OlGlorpys_ChewySoup.png"
DEFAULT_COUPON2 = "busts/Weatherman_Coupon.png"

SAMPLE_EXPERIENCE = "You rocked your head in the most amazing DJ set in your life wondering how much acid you took as the blindfold came off. You 'll always wonder who she was -- such a great painter. You found a serene oasis in the same level as Aristotle, while he’s so smart. Your doppelganger gave several different names and claimed to be the destruction of the planet itself. The best proof is that you are still disappointed."



class ReceiptImage:

    TYPE = "image"

    def __init__(self, filepath):
        self.filepath = filepath
        self.img = None
        self.img_tmp = None

"""
    def save_image_temp(self):
        " Save a PIL Image to a temporary file and return its path. "
        temp_file = NamedTemporaryFile(delete=False, suffix=".png")

        # load the image object if we haven't already
        if not self.img:
            return            

        self.img.save(temp_file, "PNG")
        return temp_file.name
"""

class ReceiptText:

    TYPE = "text"

    def __init__(self, text, size="normal", font=None, bold=False, underline=0, align="left"):
        self.text = text
        self.size = size
        self.font = font
        self.underline = underline
        self.bold = bold
        self.align = align

    def render(self):
        "Returns an image generated by PIL with this text."
        return text_to_img(text, self.font, self.size, align=self.align) #  max_width=
    

class ExperienceReceipt:
    def __init__(self, title="MEGAVIBE9000", title_font=DEFAULT_TITLE_FONT, 
                    motto=DEFAULT_MOTTO, company=DEFAULT_COMPANY, logo=DEFAULT_LOGO,
                    coupon1=DEFAULT_COUPON1, coupon2=DEFAULT_COUPON2, experience_text=None,
                    date=None, time=None, receipt_no=None,
                ):

        # this array will hold the sequence of elements to be printed.
        self.receipt = []

        self.title = title
        self.title_font = title_font
        self.logo = logo
        self.motto = motto
        self.coupon1 = coupon1
        self.coupon2 = coupon2
        self.header = "Your Experience"
        self.body = experience_text
        self.company = company
        self.motto = motto
        self.receipt_no = receipt_no

        # date and time can be provided, or they will be set upon self.build_receipt()
        self.date = None
        self.time = None

    def set_date_time(self, date=None, time=None):
        """ If date and time are not provided, use current date and time. """
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')
        self.time = time if time else datetime.now().strftime('%H:%M:%S')

    def set_receipt_no(self):
        #todo: change this to 2999 epoch timestamp
        if not self.receipt_no:
            self.receipt_no = datetime.timestamp()

    def build_receipt(self):
        """ This function builds the receipt as a sequential array of Receipt* objects,
        which can be rendered using a ReceiptRenderer object (e.g. through PIL to an 
        image, or through an ESC/POS thermal printer.
        """

        self.receipt = []
        self.set_date_time()

        # Top matter: store name, date, time.
        self.receipt.append(ReceiptText(self.title, font=self.title_font, size="large"))
        self.receipt.append(ReceiptText("Date: {self.date}"))
        self.receipt.append(ReceiptText("Time: {self.time}"))

        self.receipt.append(ReceiptText(self.header, size="large", bold=True))

        # -- Experience section begins -- 
        # 
        # break the body down into parts so that coupons can be inserted.
        if not self.body:
            self.body = SAMPLE_EXPERIENCE

        part1 = self.body.split(".")[0:2]
        part2 = self.body.split(".")[3:]

        self.receipt.append(ReceiptText("{}".format((". ").join(part1) + ". ")))
        self.receipt.append(ReceiptImage(self.coupon1))
        self.receipt.append(ReceiptText("{}".format((". ").join(part2) + ". ")))

        # -- end of Experience section --
        
        # -- Company footer should be centered. Name -> "motto" -> logo.
        self.receipt.append(ReceiptText(self.company, size="medium"))
        self.receipt.append(ReceiptText(self.motto))
        self.receipt.append(ReceiptImage(self.coupon2))
        self.receipt.append(ReceiptText(f"Receipt No.: {self.receipt_no}"))

