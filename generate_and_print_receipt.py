from datetime import datetime
from artery import MockArteryPrinter, ArteryPrinter
from artery import ExperienceReceipt, ReceiptImage, ReceiptText, CrazyText

from experience_generator import generate_experience
from experience_generator import send_to_discord

from artery import pick_coupon


# Function to print the receipt
def print_receipt(receipt):
    printer = ArteryPrinter()

    for obj in receipt.receipt:
        if isinstance(obj, ReceiptImage):
            printer.print_image(obj.filepath)
        elif isinstance(obj, ReceiptText):
            printer.print_text(obj.text, **obj.to_dict())
        elif isinstance(obj, CrazyText):
            printer.print_crazy_text(obj.text, **obj.to_dict())

    printer.finish()

# Example of how to use the ExperienceReceipt class and the print_receipt function


def stripped_down_receipt(text):
    receipt = ExperienceReceipt(experience_text=text)
    receipt.build_receipt()
    return receipt


def full_receipt():
    exp_text = generate_experience()
    send_to_discord(exp_text)
    coupon1 = pick_coupon("coupons")
    coupon2 = pick_coupon("coupons")

    receipt = ExperienceReceipt(experience_text=exp_text, coupon1=coupon1, coupon2=coupon2)
    receipt.build_receipt()
    return receipt


print_receipt(stripped_down_receipt("ERRORS"))

#stripped_down_receipt("ERRORS")

#print_receipt(full_receipt())

