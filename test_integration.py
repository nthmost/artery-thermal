from datetime import datetime
from artery import ArteryPrinter
from artery import ExperienceReceipt

# Sample experience text for when none is provided
SAMPLE_EXPERIENCE = "This is a sample experience text to be printed on the receipt."

# Function to print the receipt
def print_receipt(receipt):
    printer = ArteryPrinter()
    
    for line in receipt.receipt:
        if "[IMAGE]" in line and "[/IMAGE]" in line:
            img_path = line.split("[IMAGE]")[1].split("[/IMAGE]")[0]
            printer.print_image(img_path)
        elif "[FONT " in line and "[/FONT]" in line:
            font_info = line.split("[FONT ")[1].split("]")[0]
            # Process the font_info here if needed, e.g., to extract size, boldness, etc.
            text = line.split("[/FONT]")[1]
            # Adjust the below print_text function as needed
            printer.print_text(text, font_size='medium')
        else:
            printer.print_text(line)
    
    printer.finish()

# Example of how to use the ExperienceReceipt class and the print_receipt function
receipt = ExperienceReceipt(title="MEGAVIBE9000")
receipt.build_receipt()

print_receipt(receipt)


