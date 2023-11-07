import streamlit as st
import time
import os
import random
from experience_generator import MarkovGenerator, send_to_discord

# Configuration variables
STATE_SIZE = 3
TRIES = 10
NUM_SENTENCES = 7

party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"

# Display a fixed image at the top of the screen
top_image_path = "ccc/MEGAVIBE.png"
st.image(top_image_path, use_column_width=True)

# Password input
password_input = st.text_input("ENTER THE PASSWORD", type="password", key="password")

generator = MarkovGenerator(party_db_path, tescreal_db_path)


def random_gif():
    return os.path.join("animated_gifs", random.choice(os.listdir("animated_gifs")))

def generate_and_send_message():
    start_time = time.time()
    generated_text = generator.generate_experience(num_sentences=NUM_SENTENCES)
    end_time = time.time()

    try:
        state_info = f"State Size: {STATE_SIZE}  Tries: {TRIES}  Sentences: {NUM_SENTENCES}"
        full_message = generated_text + "\n\n" + state_info
        send_to_discord(full_message)
        st.write("Message sent to Discord!")
    except Exception as e:
        st.write(f"Failed to send to Discord: {e}")

    return generated_text, end_time - start_time

# Check if the correct password is entered
if password_input in ("love", "secret", "sex", "God", "password"):
    st.text("ACCESS GRANTED.")
    st.image(random_gif(), use_column_width=True)  # Display a loading gif
    generated_text, generation_time = generate_and_send_message()

    st.write("Generated Text:")
    st.write(generated_text)

    # Display the PRINT button
    if st.button("PRINT"):
        # Define the action for the PRINT button here
        print("PRINTING RECEIPT!")
        pass  # You can specify what you want to do when the button is clicked

        #TODO
        # play some music
        # reset the page

