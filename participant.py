import streamlit as st
import os
import random
import requests

from artery import ArteryPrinter
from artery import pick_coupon
from artery import ExperienceReceipt, ReceiptImage, ReceiptText, CrazyText


FLASK_SERVICE_URL = "http://192.168.2.2:5000/generate"

with open( "streamlit_style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Display a fixed image at the top of the screen
top_image_path = "ccc/MEGAVIBE_teal.png"
st.image(top_image_path, use_column_width=True)

st.header("EXPERIENCE GENERATOR")

# set up a placeholder for a very simple layout
placeholder = st.empty()

# CCC logo at top left hand corner:
st.sidebar.image("ccc/ccc-cyber-teal.png")

# Password input
password_input = st.sidebar.text_input("ENTER THE PASSWORD", type="password", key="password",
                                       help="The four most commonly used passwords are...",)


def random_gif():
    return os.path.join("animated_gifs", random.choice(os.listdir("animated_gifs")))



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
        elif isinstance(obj, CrazyText):
            printer.print_crazy_text(obj.text, **obj.to_dict())

    printer.finish()

def full_receipt(text):
    coupon1 = pick_coupon("coupons")
    coupon2 = pick_coupon("coupons")

    receipt = ExperienceReceipt(experience_text=text, coupon1=coupon1, coupon2=coupon2)
    receipt.build_receipt()
    return receipt



def generate_and_send_message():
    # Make an HTTP GET request to the Flask service
    response = requests.get(FLASK_SERVICE_URL)
    generated_text = response.json()['experience']  # Extract the experience from the response

    try:
        full_message = generated_text
        send_to_discord(full_message)
        print("Message sent to Discord!")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

    return generated_text

# Check if the correct password is entered
if password_input in ("love", "secret", "sex", "God", "password"):
    st.sidebar.text("ACCESS GRANTED.")
    placeholder.image(random_gif(), width=300)  # use_column_width=True)  # Display a loading gif
    generated_text = generate_and_send_message()
    placeholder.write(generated_text)

    # Display the PRINT button
    if st.button("PRINT"):
        receipt = full_receipt(generated_text)
        try:
            print_receipt(receipt)
            st.write("Receipt printed successfully!")
        except Exception as e:
            st.write(f"Failed to print receipt: {e}")

        #TODO
        # play some music
        # reset the page

