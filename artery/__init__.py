from .command import ArteryPrinter, ArteryPrinterTest
from .base import MockArteryPrinter
from .receipt import ExperienceReceipt, ReceiptImage, ReceiptText, CrazyText

import os, random

def pick_coupon(directory):
	return os.path.join(directory, random.choice(os.listdir(directory)))

def simple_test():
    printer = ArteryPrinter()
    printer.p.text("\x1D\x21\x11")  # Set text to double height and width
    printer.p.text("MEGAVIBE 9000\n")
    printer.p.text("\x1D\x21\x00")  # Reset text size to normal
    printer.finish()


def every_font_test():
    # Create an instance
    printer_test = ArteryPrinterTest()

    # Run the test
    printer_test.test_font_map()

    # Finish the printing
    printer_test.finish()


def main():
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "hello":
            simple_test()
        elif command == "test":
            every_font_test()
        else:
            print(f"Unknown command: {command}")
    else:
        print("Usage: artery <command>")
        print("Available commands: hello, test")

if __name__ == "__main__":
    main()

	
