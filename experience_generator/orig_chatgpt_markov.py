import random
import re

def build_markov_chain(corpus, chain={}):
    words = corpus.split()
    for i in range(len(words) - 2):
        bigram = (words[i], words[i + 1])
        if bigram in chain:
            chain[bigram].append(words[i + 2])
        else:
            chain[bigram] = [words[i + 2]]
    return chain

def generate_story(chain, length=50):
    bigram = random.choice(list(chain.keys()))
    story = list(bigram)
    for i in range(length):
        if bigram in chain:
            next_word = random.choice(chain[bigram])
            story.append(next_word)
            bigram = (story[-2], story[-1])
        else:
            break
    return ' '.join(story)

def trim_to_complete_sentence(story):
    # Use regex to find the last sentence boundary
    match = re.search(r'([.!?])\s', story[::-1])
    if match:
        # Return the story up to the last complete sentence
        return story[:-(match.start() + 1)]
    else:
        # If no sentence boundary is found, return the original story
        return story

# Load your corpuses
party_db = open("PARTY_DB.txt", 'r').read()
tescreal_db = open("TESCREAL_DB.txt", 'r').read()

# Build Markov Chain
chain = build_markov_chain(party_db)
chain = build_markov_chain(tescreal_db, chain)

# Generate a new story and trim to the last complete sentence
story = generate_story(chain)
print(trim_to_complete_sentence(story))

