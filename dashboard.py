import streamlit as st
import time
import os
import random
from experience_generator import MarkovGenerator, send_to_discord


party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"

# Check if 'generator' exists in the session state and the previous values of state_size and tries
if 'generator' not in st.session_state:
    st.session_state.generator = MarkovGenerator(party_db_path, tescreal_db_path)
    st.session_state.prev_state_size = 2  # default value
    st.session_state.prev_tries = 5      # default value


# Reference to the generator in session state
generator = st.session_state.generator

# Sidebar Configurations
st.sidebar.title("Configuration")

# Sliders in the sidebar
state_size = st.sidebar.slider("State Size", 1, 5, st.session_state.prev_state_size)
tries = st.sidebar.slider("Tries", 1, 10, st.session_state.prev_tries)

# If state_size or tries values have changed, reset the generator
if state_size != st.session_state.prev_state_size or tries != st.session_state.prev_tries:
    st.session_state.generator = MarkovGenerator(party_db_path, tescreal_db_path)
    generator = st.session_state.generator  # update the reference

# Update the current values in session_state
st.session_state.prev_state_size = state_size
st.session_state.prev_tries = tries

# Update generator parameters
generator.state_size = state_size
generator.tries = tries


# Slider to adjust the number of sentences
num_sentences = st.sidebar.slider('Number of Sentences', 1, 20, 6)

send_to_discord_flag = st.sidebar.checkbox("Send to Discord")

# Generate button and timer in the main section
st.write("### Generate Experience Text")

if st.button("Generate"):
    # Place to show the GIF
    placeholder = st.empty()

    random_gif = os.path.join(("animated_gifs"), random.choice(os.listdir("animated_gifs")))

    with open(random_gif, "rb") as f:
        gif_bytes = f.read()
    placeholder.image(gif_bytes)        #, caption="Generating...")

    start_time = time.time()
    generated_text = generator.generate_experience(num_sentences=num_sentences)
    end_time = time.time()

    if send_to_discord_flag:
        # Format the message
        state_info = f"State Size: {state_size}  Tries: {tries}  Sentences: {num_sentences}"
        full_message = generated_text + "\n\n" + state_info
        
        # Send the message to Discord
        send_to_discord(full_message)

    st.write("Generated in {:.2f} seconds.".format(end_time - start_time))
    st.write(generated_text)

