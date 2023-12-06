import streamlit as st
import os
import random
import requests


FLASK_SERVICE_URL = "http://192.168.2.2:5000/generate"

PRINT_SERVICE_URL = "http://192.168.2.3:5000/print"


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

def generate_and_send_message():
    # Make an HTTP GET request to the Flask service
    response = requests.get(FLASK_SERVICE_URL)
    generated_text = response.json()['experience']  # Extract the experience from the response

    try:
        full_message = generated_text
        #send_to_discord(full_message)
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

    return generated_text


def print_receipt(text):
    print("SENDING TO FLASK")
    # Preparing the data payload
    data = {"text": text}

    # Sending the POST request
    response = requests.post(PRINT_SERVICE_URL, json=data)
    # Checking the response
    if response.status_code == 200:
        print("Print request successful.")
    else:
        print(f"Print request failed. Status code: {response.status_code}, Message: {response.text}")



# Check if the correct password is entered
if password_input in ("love", "secret", "sex", "God", "password"):
    st.sidebar.text("ACCESS GRANTED.")
    placeholder.image(random_gif(), width=300)  # use_column_width=True)  # Display a loading gif
    generated_text = generate_and_send_message()
    placeholder.write(generated_text)

    # Display the PRINT button
    if st.button("PRINT"):
        try:
            print_receipt(generated_text)
            st.write("Receipt printed successfully!")
        except Exception as e:
            st.write(f"Failed to print receipt: {e}")

        #TODO
        # play some music
        # reset the page

