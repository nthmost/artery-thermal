from datetime import datetime
from tempfile import NamedTemporaryFile
from .format import text_to_img

DEFAULT_COMPANY = "Community Capture Corporation"
DEFAULT_MOTTO = "We've got you. ;)"
DEFAULT_LOGO = "wings.png"
DEFAULT_TITLE = "MEGAVIBE 9000"
DEFAULT_TITLE_FONT = "fonts/zig.ttf"
DEFAULT_COUPON1 = "coupons/OlGlorpy_ChewySoup_1.png"
DEFAULT_COUPON2 = "busts/Weatherman_Coupon.png"

SAMPLE_EXPERIENCE = "You rocked your head in the most amazing DJ set in your life wondering how much acid you took as the blindfold came off. You 'll always wonder who she was -- such a great painter. You found a serene oasis in the same level as Aristotle, while he’s so smart. Your doppelganger gave several different names and claimed to be the destruction of the planet itself. The best proof is that you are still disappointed."

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
        self.title_image = text_to_img(title, title_font, 32)
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
        """ This function will build and return the document as a string (or however you want to represent it) """
        # You would format this however you'd like, this is just a basic representation.
        # Note: The actual formatting and setting font styles would depend on the library/printer you're using.
        #       Here, we're just building a conceptual string representation.
        
        self.receipt = []

        self.set_date_time()

        self.receipt.append("[IMAGE]{}[/IMAGE]".format(self.save_image_temp(self.title_image)))
        self.receipt.append(f"Date: {self.date}")
        self.receipt.append(f"Time: {self.time}")
        self.receipt.append(f"[FONT size=16 bold=True]{self.header}[/FONT]")

        # break the body down into parts so that coupons can be inserted.
        if not self.body:
            self.body = SAMPLE_EXPERIENCE

        part1 = self.body.split(".")[0:3]
        part2 = self.body.split(".")[4:]
        self.receipt.append("{}".format((". ").join(part1) + ". "))
        self.receipt.append(f"[IMAGE]{self.coupon1}[/IMAGE]")
        self.receipt.append("{}".format((". ").join(part2) + ". "))
        
        self.receipt.append(f"[FONT size=medium]{self.company}[/FONT]")
        self.receipt.append(self.motto)
        self.receipt.append(f"[IMAGE]{self.logo}[/IMAGE]")
        self.receipt.append(f"[IMAGE]{self.coupon2}[/IMAGE]")
        self.receipt.append(f"Receipt No.: {self.receipt_no}")

    def save_image_temp(self, img):
        """ Save a PIL Image to a temporary file and return its path. """
        temp_file = NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_file, "PNG")
        return temp_file.name

