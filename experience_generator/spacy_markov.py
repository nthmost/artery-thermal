import spacy
import markovify
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def build_model(corpus):
    return POSifiedText(corpus, state_size=2)  #  If problems, reduce from 2 to 1


# Load your corpuses
party_db = open("PARTY_DB.txt").read()
tescreal_db = open("TESCREAL_DB.txt").read()

# Build Markov models
party_model = build_model(party_db)
tescreal_model = build_model(tescreal_db)

# Combine the models
combined_model = markovify.combine([party_model, tescreal_model], [3, 1])


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
        (r"\bca n't\b", "can't"),  # contractions
        (r"\bdo n't\b", "don't"),
        (r"\bare n't\b", "aren't"),
        (r"\byou 're\b", "you're"),
        # ... add more as needed
    ]

    # Apply the replacements
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    return text


def ensure_subject(sentence):
    doc = nlp(sentence)
    has_subject = any([word.dep_ == "nsubj" for word in doc])
    return sentence if has_subject else None

def generate_paragraph(model, num_sentences=5):
    paragraph = []
    for _ in range(num_sentences):
        sentence = model.make_sentence()
        if sentence and ensure_subject(sentence):  # Ensure a valid sentence was generated
            paragraph.append(sentence)
    return ' '.join(paragraph)

# Generate a paragraph with 5 sentences from the combined model
print(format_text(generate_paragraph(combined_model)))

def corpus_insights(corpus):
    # Tokenize using spaces
    tokens = corpus.split()
    unique_tokens = set(tokens)
    
    # Count sentences
    sentence_count = corpus.count('.') + corpus.count('!') + corpus.count('?')
    
    print(f"Total tokens: {len(tokens)}")
    print(f"Unique tokens: {len(unique_tokens)}")
    print(f"Total sentences: {sentence_count}")
    print(f"Average tokens per sentence: {len(tokens) / sentence_count if sentence_count else 0}")
    print(f"Sample tokens: {list(unique_tokens)[:50]}")  # Print 50 sample unique tokens

#print("Party DB Insights:")
#corpus_insights(party_db)

#print("\nTESCREAL DB Insights:")
#corpus_insights(tescreal_db)


#def generate_experience(party_weight, tescreal_weight):
#    return 

def generate_experience():
    return format_text(generate_paragraph(combined_model))


