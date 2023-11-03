import re

def capitalize_sentences(text):
    # Split the text into sentences based on common sentence-ending punctuation
    sentences = re.split('(?<=[.!?]) +', text)
    
    # Capitalize the first letter of each sentence
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    
    # Join the sentences back into a single string
    return ' '.join(capitalized_sentences)

def format_text(text):
    # Define a list of patterns and their replacements
    replacements = [
        (r" \,", ","),  # spaces before commas
        (r" \.", "."),  # spaces before periods
        (r" \?", "?"),  # spaces before question marks
        (r" \!", "!"),  # spaces before exclamation marks
        (r" ’", "’"),   # spaces before apostrophes
        (r" ;", ";"),   # spaces before semicolons
        (r" \:", ":"),  # spaces before colons
        (r"\bca n’t\b", "can’t"),  # contractions
        (r"\bdo n’t\b", "don’t"),
        (r"\bare n’t\b", "aren’t"),
        (r"\byou ’re\b", "you’re"),
        (r"\bwas n’t\b", "wasn’t"),
        (r"\bcould n’t\b", "couldn’t"),
        # ... add more as needed
    ]

    # Apply the replacements
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    return capitalize_sentences(text)

