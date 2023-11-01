from escpos.printer import Usb

# USB IDs for your printer
VENDOR_ID = 0x6868
PRODUCT_ID = 0x0200

# Initialize the printer
p = Usb(VENDOR_ID, PRODUCT_ID)

# MEGAVIBE 9000 in a very large font
p.set(align='center')
p.text("\x1D\x21\x11")  # Set text to double height and width
p.text("MEGAVIBE 9000\n")
p.text("\x1D\x21\x00")  # Reset text size to normal

p.ln()  # Line feed

# YOUR EXPERIENCE: in a smaller, but still large font
p.set(align='center', bold=True)
p.text("\x1D\x21\x10")  # Set text to double width
p.text("YOUR EXPERIENCE:\n")
p.text("\x1D\x21\x00")  # Reset text size to normal
p.set(bold=False)

p.ln()

# In a normal font
p.set(align='center')
p.text("If we now are as gods, we live in a large maintenance closet.\n")

p.ln()

# Cut the paper
p.cut()

# Close the connection
p.close()

