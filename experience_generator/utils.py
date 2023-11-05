import re

def capitalize_sentences(text):
    # Split the text into sentences based on common sentence-ending punctuation
    sentences = re.split('(?<=[.!?]) +', text)
    
    # Capitalize the first letter of each sentence
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    
    # Join the sentences back into a single string
    return ' '.join(capitalized_sentences)
    
    
def contraction_replacer(match):
    word = match.group(1)
    contraction = match.group(2).replace(" ", "")
    return f"{word}{contraction}"


def format_text(text):
    # Standardize straight apostrophes to curly ones
    text = text.replace("'", "’")
    
    # Define a list of patterns and their replacements
    replacements = [
        (r" \,", ","),  # spaces before commas
        (r" \.", "."),  # spaces before periods
        (r" \?", "?"),  # spaces before question marks
        (r" \!", "!"),  # spaces before exclamation marks
        (r" ’", "’"),   # spaces before apostrophes
        (r" ;", ";"),   # spaces before semicolons
        (r" \:", ":"),  # spaces before colons
    ]

    # Apply the replacements
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    # Fix dashes surrounded by spaces
    text = re.sub(r' - ', '-', text)

    # Handle contractions
    contraction_patterns = [
        r"\b(\w+) (’[a-z]{1,2})\b",  # for contractions like "you ’re"
        r"\b(\w+ n) ’t\b",  # for contractions like "do n’t"
        r"\b(\w+) (n’t)\b"  # for contractions like "do n’t" with a different pattern
    ]
    for pattern in contraction_patterns:
        text = re.sub(pattern, contraction_replacer, text)
    
    text = capitalize_sentences(text)

    # Capitalize standalone 'i'
    text = re.sub(r'\b i(?=[.!?])', ' I', text)

    return text
