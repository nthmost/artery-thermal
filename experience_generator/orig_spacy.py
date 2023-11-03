import spacy
import markovify
import re
from functools import cache

from .utils import format_text

nlp = spacy.load("en_core_web_sm")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class MarkovGenerator:

    def __init__(self, state_size=2):
        self._state_size = state_size
        self._party_model = None
        self._tescreal_model = None
        self._combined_model = None

    @property
    @cache
    def party_db(self):
        return open("PARTY_DB.txt").read()

    @property
    @cache
    def tescreal_db(self):
        return open("TESCREAL_DB.txt").read()

    @property
    @cache
    def party_model(self):
        return POSifiedText(self.party_db, state_size=self._state_size)

    @property
    @cache
    def tescreal_model(self):
        return POSifiedText(self.tescreal_db, state_size=self._state_size)

    @property
    @cache
    def combined_model(self):
        return markovify.combine([self.party_model, self.tescreal_model], [2, 1])

    def ensure_subject(self, sentence):
        doc = nlp(sentence)
        has_subject = any([word.dep_ == "nsubj" for word in doc])
        return sentence if has_subject else None

    def generate_paragraph(self, model, num_sentences=5):
        paragraph = []
        for _ in range(num_sentences):
            sentence = model.make_sentence()
            if sentence and self.ensure_subject(sentence):
                paragraph.append(sentence)
        return ' '.join(paragraph)

    def generate_experience(self):
        return format_text(self.generate_paragraph(self.combined_model))

    def corpus_insights(self, corpus):
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

