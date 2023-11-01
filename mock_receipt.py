from datetime import datetime
from artery import MockArteryPrinter, ArteryPrinter
from artery import ExperienceReceipt, ReceiptImage, ReceiptText
from artery import pick_coupon


coupon1 = pick_coupon("coupons")
coupon2 = pick_coupon("coupons")


# Function to print the receipt
def print_receipt(receipt):
    printer = MockArteryPrinter()

    for obj in receipt.receipt:
        if isinstance(obj, ReceiptImage):
            printer.print_image(obj.filepath)
        elif isinstance(obj, ReceiptText):
            printer.print_text(obj.text, **obj.to_dict())

    printer.finish()

# Example of how to use the ExperienceReceipt class and the print_receipt function

exp_text = "You rocked your head to the most amazing DJ set in your life wondering how much acid you took as the blindfold came off. You 'll always wonder who she was -- such a great painter. You found a serene oasis where your doppelganger gave several different names and claimed to be the destruction of the planet itself. The best proof is that you are still disappointed."

receipt = ExperienceReceipt(title="MEGAVIBE\n9000", experience_text=exp_text, coupon1=coupon1, coupon2=coupon2)
receipt.build_receipt()

print_receipt(receipt)

