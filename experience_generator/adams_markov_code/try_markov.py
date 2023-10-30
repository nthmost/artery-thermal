from markov import *

FULLDB_FILENAME = "fulldb.txt"

buf = "{}\n\n{}".format(
    open("PARTY_DB.txt").read(), open("TESCREAL_DB.txt").read())
open(FULLDB_FILENAME, 'w').write(buf)
                
markov_primer(FULLDB_FILENAME, "fulldb.pkl")

# Generate random text using the created database
#seed_phrase = ("You", "heard",)

seed_phrase = input("What's the seed phrase this time? ")
phrase = tuple(seed_phrase.split(" "))

output = markov_output("fulldb.pkl", seed=phrase, output_length=150)
print(output)


