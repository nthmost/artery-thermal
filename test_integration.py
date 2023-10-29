from datetime import datetime
from artery import ArteryPrinter
from artery import ExperienceReceipt, ReceiptImage, ReceiptText

# Sample experience text for when none is provided
SAMPLE_EXPERIENCE = "This is a sample experience text to be printed on the receipt."

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
receipt = ExperienceReceipt(title="MEGAVIBE9000")
receipt.build_receipt()

print_receipt(receipt)

