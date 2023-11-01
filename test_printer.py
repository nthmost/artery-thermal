from artery import ArteryPrinter, ArteryPrinterTest


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



if __name__=='__main__':
    # simple_test()

    every_font_test()

