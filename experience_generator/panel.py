import streamlit as st

from spacy_markov import generate_paragraph as spacy_generate

#from adam_markov import 


# Define the two scripts
def script_a(weight_party, weight_tescreal):
    # Implement Script A logic here
    return "Generated text from Script A\nParty DB Weight: {}\nTESCREAL DB Weight: {}".format(weight_party, weight_tescreal)

def script_b(weight_party, weight_tescreal):
    # Implement Script B logic here
    return "Generated text from Script B\nParty DB Weight: {}\nTESCREAL DB Weight: {}".format(weight_party, weight_tescreal)

# Sidebar controls
st.sidebar.header("Settings")
selected_script = st.sidebar.radio("Select Script:", ("Script A", "Script B"))
weight_party = st.sidebar.slider("Party DB Weight:", min_value=0, max_value=100, value=50)
weight_tescreal = st.sidebar.slider("TESCREAL DB Weight:", min_value=0, max_value=100, value=50)


go_btn = st.sidebar.button("GENERATE")

# Generate button
if go_btn:
    if selected_script == "Script A":
        generated_text = script_a(weight_party, weight_tescreal)
    else:
        generated_text = script_b(weight_party, weight_tescreal)

# Main section
st.title("Your Experience")
if go_btn:
    st.write(generated_text)

