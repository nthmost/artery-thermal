from datetime import datetime
from artery import ArteryPrinter
from artery import ExperienceReceipt

# Sample experience text for when none is provided
SAMPLE_EXPERIENCE = "This is a sample experience text to be printed on the receipt."

# Function to print the receipt
def print_receipt(receipt):
    printer = ArteryPrinter()
    
    for obj in receipt.receipt:
        if obj.__name__ == "ReceiptImage":
            printer.print_image(obj.filepath)

        elif obj.__name__ == "ReceiptText":
            printer.print_text(text, font_size=obj.font_size, bold=obj.bold, underline=obj.underline)    

    printer.finish()

# Example of how to use the ExperienceReceipt class and the print_receipt function
receipt = ExperienceReceipt(title="MEGAVIBE9000")
receipt.build_receipt()

print_receipt(receipt)


