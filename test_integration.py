from datetime import datetime
from artery import MockArteryPrinter, ArteryPrinter
from artery import ExperienceReceipt, ReceiptImage, ReceiptText

from experience_generator import generate_experience


# Function to print the receipt
def print_receipt(receipt):
    printer = ArteryPrinter()

    for obj in receipt.receipt:
        if isinstance(obj, ReceiptImage):
            printer.print_image(obj.filepath)
        elif isinstance(obj, ReceiptText):
            printer.print_text(obj.text, font_size=obj.size, bold=obj.bold, underline=obj.underline)

    printer.finish()

# Example of how to use the ExperienceReceipt class and the print_receipt function

exp_text = generate_experience()

receipt = ExperienceReceipt(title="MEGAVIBE9000", experience_text=exp_text)
receipt.build_receipt()

print_receipt(receipt)

