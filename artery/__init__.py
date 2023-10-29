from .command import ArteryPrinter, ArteryPrinterTest
from .base import MockArteryPrinter
from .receipt import ExperienceReceipt, ReceiptImage, ReceiptText

import os, random

def pick_coupon(directory):
	return os.path.join(directory, random.choice(os.listdir(directory)))
	
