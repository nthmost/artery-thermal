import streamlit as st
import time
import os
import random
from experience_generator import MarkovGenerator, send_to_discord

with open( "streamlit_style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Configuration variables
STATE_SIZE = 3
TRIES = 10
NUM_SENTENCES = 7

party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"


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

generator = MarkovGenerator(party_db_path, tescreal_db_path)


def random_gif():
    return os.path.join("animated_gifs", random.choice(os.listdir("animated_gifs")))

def generate_and_send_message():
    state_info = f"State Size: {STATE_SIZE}  Tries: {TRIES}  Sentences: {NUM_SENTENCES}\n"
    start_time = time.time()
    generated_text = generator.generate_experience(num_sentences=NUM_SENTENCES)
    end_time = time.time()

    # log what we did to the console
    print("\nGENERATED the previous sentences in {} seconds".format(end_time-start_time))

    try:
        full_message = generated_text + "\n\n" + state_info
        send_to_discord(full_message)
        print("Message sent to Discord!")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

    return generated_text, end_time - start_time

# Check if the correct password is entered
if password_input in ("love", "secret", "sex", "God", "password"):
    st.sidebar.text("ACCESS GRANTED.")
    placeholder.image(random_gif(), width=300)  # use_column_width=True)  # Display a loading gif
    generated_text, generation_time = generate_and_send_message()
    placeholder.write(generated_text)

    # Display the PRINT button
    if st.button("PRINT"):
        # Define the action for the PRINT button here
        print("PRINTING RECEIPT!")
        pass  # You can specify what you want to do when the button is clicked

        #TODO
        # play some music
        # reset the page

