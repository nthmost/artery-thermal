import streamlit as st
import time
import os
import re
import random
import pandas as pd
from experience_generator import MarkovGenerator, send_to_discord


party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"


def evaluate_corpus(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tokenize the content to extract words
    words = re.findall(r'\b\w+\b', content.lower())

    # Count unique words
    unique_word_counts = {}
    for word in words:
        if word not in unique_word_counts:
            unique_word_counts[word] = 1
        else:
            unique_word_counts[word] += 1

    return unique_word_counts


# Sidebar button
if st.sidebar.button("Evaluate Corpus"):
    # Evaluate PARTY_DB
    party_word_counts = evaluate_corpus(party_db_path)
    party_df = pd.DataFrame(list(party_word_counts.items()), columns=['Word', 'Frequency'])
    party_df = party_df.sort_values(by='Frequency', ascending=False)  # Sort by frequency by default

    # Evaluate TESCREAL_DB
    tescreal_word_counts = evaluate_corpus(tescreal_db_path)
    tescreal_df = pd.DataFrame(list(tescreal_word_counts.items()), columns=['Word', 'Frequency'])
    tescreal_df = tescreal_df.sort_values(by='Frequency', ascending=False)  # Sort by frequency by default

    # Display dataframes
    st.write("### PARTY_DB Unique Words")
    st.write(party_df)

    st.write("\n")  # Add a separator

    st.write("### TESCREAL_DB Unique Words")
    st.write(tescreal_df)


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

