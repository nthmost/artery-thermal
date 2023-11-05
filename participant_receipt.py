import streamlit as st
import time
import os
import random
from datetime import datetime
from artery import MockArteryPrinter, ArteryPrinter
from artery import ExperienceReceipt, ReceiptImage, ReceiptText
from experience_generator import MarkovGenerator, send_to_discord
from artery import pick_coupon

# Configuration variables
STATE_SIZE = 3
TRIES = 10
NUM_SENTENCES = 7

party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = MarkovGenerator(party_db_path, tescreal_db_path)
    st.session_state.gifs = os.listdir("animated_gifs")

generator = st.session_state.generator

def prep_text(text):
    """Replace curly apostrophes with straight ones."""
    return text.replace('\u2018', "'").replace('\u2019', "'")


# Function to print the receipt
def print_receipt(receipt):
    printer = ArteryPrinter()

    for obj in receipt.receipt:
        if isinstance(obj, ReceiptImage):
            printer.print_image(obj.filepath)
        elif isinstance(obj, ReceiptText):
            printer.print_text(prep_text(obj.text), **obj.to_dict())

    printer.finish()

def full_receipt(text):
    coupon1 = pick_coupon("coupons")
    coupon2 = pick_coupon("coupons")

    receipt = ExperienceReceipt(experience_text=text, coupon1=coupon1, coupon2=coupon2)
    receipt.build_receipt()
    return receipt

st.write("### MEGAVIBE 9000")

if st.button("Generate"):
    # Place to show the GIF
    placeholder = st.empty()

    # Select a random gif
    random_gif = os.path.join("animated_gifs", random.choice(st.session_state.gifs))
    with open(random_gif, "rb") as f:
        gif_bytes = f.read()

    placeholder.image(gif_bytes)

    start_time = time.time()
    generated_text = generator.generate_experience(num_sentences=NUM_SENTENCES)
    end_time = time.time()

    # Send the message to Discord
    try:
        state_info = f"State Size: {STATE_SIZE}  Tries: {TRIES}  Sentences: {NUM_SENTENCES}"
        full_message = generated_text + "\n\n" + state_info
        send_to_discord(full_message)
        st.write("Message sent to Discord!")
    except Exception as e:
        st.write(f"Failed to send to Discord: {e}")

    placeholder.write(generated_text)
    st.write("Generated in {:.2f} seconds.".format(end_time - start_time))

    # Store the generated text in session state for printing
    st.session_state.generated_text = generated_text

# Print Receipt
if 'generated_text' in st.session_state and st.button("Print Receipt"):
    receipt = full_receipt(st.session_state.generated_text)
    try:
        print_receipt(receipt)
        st.write("Receipt printed successfully!")
    except Exception as e:
        st.write(f"Failed to print receipt: {e}")

