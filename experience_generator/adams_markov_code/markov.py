import pickle
import string
import random

def markov_primer(corpus, database, wordchunk=2, new_db=True):
    '''
    Takes a corpus (text), creates a phrase-frequency table, and puts that table into the named database file.
    word_chunk is the number of words in each phrase; the default is 2, and it can't be smaller than 1. 
    new_db is a boolean indicating whether the database is new, or if we're extending an old one.
    '''
    
    # Let's open the files.
    with open(corpus, "r", newline=None) as ftext, open(database, "wb+") as fdb:
        # Read in the entire text file.
        text = ftext.read()
        
        # Create the place where the frequency table will live.
        if new_db:
            db = {}
        else:
            db = pickle.load(fdb)
        
        # Split the text into words
        words = text.split()
        
        numchunks = len(words) - wordchunk + 1
        numpairs = numchunks - 1
        
        # Iterate over the words to create the database
        for i in range(numpairs):
            chunk = tuple(words[i:i+wordchunk])
            nextchunk = tuple(words[i+wordchunk:i+2*wordchunk])
            
            chunklist = db.get(chunk, [])
            chunklist.append(nextchunk)
            db[chunk] = chunklist
        
        # Save the database.
        pickle.dump(db, fdb)
    
    # print("Database successfully created.\nDon't hold me accountable for what you do with it.")


def markov_output(database, seed="", output_length=30, encoding="utf8"):
    '''
    Uses a Markov chain with the given database to generate a random output in the style of the original text.
    seed will seed the chain; it must be a tuple of strings. If no seed is given, one will be chosen at random.
    output_length is the number of steps in the output; the step size depends on the database given.
    encoding is the character encoding, set to UTF-8 (8-bit Unicode) by default.
    '''

    # Load the database.
    with open(database, "rb") as fdb:
        db = pickle.load(fdb)

    # Initialize the Markov chain.
    if not seed:
        keys = list(db.keys())
        rs = random.randint(0, len(keys) - 1)
        seed = keys[rs]
        next_chunk = db[seed]
    else:
        try:
            next_chunk = db[seed]
        except KeyError:
            print("Sorry, that seed doesn't appear in the requested database.\nTry another word as your seed.")
            return []

    # Making a place for the output to go.
    output = list(seed)

    # Markov chain generation
    while len(output) < output_length:
        r = random.randint(0, len(next_chunk) - 1)
        newchunk = next_chunk[r]
        output.extend(newchunk)

        # Check if newchunk exists in the database
        if newchunk in db:
            next_chunk = db[newchunk]
        else:
            # If not, choose a new random seed and continue
            keys = list(db.keys())
            rs = random.randint(0, len(keys) - 1)
            newchunk = keys[rs]
            next_chunk = db[newchunk]

    # Post-processing.
    nonsense = " ".join(output)
    nonsense = str(nonsense)

    return nonsense

