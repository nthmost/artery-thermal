from escpos.printer import Usb

# Use the correct vendor ID and product ID
VENDOR_ID = 0x6868
PRODUCT_ID = 0x0200

p = Usb(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

p.text("Hello, ZJ58!\n")
p.cut()
