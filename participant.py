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

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = MarkovGenerator(party_db_path, tescreal_db_path)
    st.session_state.gifs = os.listdir("animated_gifs")

generator = st.session_state.generator

# st.write("### MEGAVIBE 9000")

st.image("ccc/MEGAVIBE.png")

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

