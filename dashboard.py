import streamlit as st
from experience_generator import MarkovGenerator 
from experience_generator import send_to_discord

st.title("Markov Text Generator")

# Sidebar for settings
st.sidebar.header("Settings")
state_size = st.sidebar.slider("State Size", 1, 5, 2)  # Default value is 2
tries = st.sidebar.slider("Tries", 1, 20, 10)  # Default value is 10

party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"
generator = MarkovGenerator(party_db_path, tescreal_db_path, state_size=state_size, tries=tries)

send_to_discord_option = st.checkbox("Send to Discord")

if st.button("Generate Text"):
    generated_text = generator.generate_experience()
    st.write(generated_text)


    if send_to_discord_option:
        send_to_discord(generated_text)

