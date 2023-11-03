import spacy
import markovify
from markovify.text import ParamError

from functools import lru_cache
from .utils import format_text



class POSifiedText(markovify.Text):
    def __init__(self, input_text, nlp=None, **kwargs):
        self.nlp = nlp or spacy.load("en_core_web_sm")
        super().__init__(input_text, **kwargs)

    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in self.nlp(sentence)]

    def word_join(self, words):
        return " ".join(word.split("::")[0] for word in words)



class MarkovGenerator:
    def __init__(self, party_db_path, tescreal_db_path, state_size=2, tries=10):
        self.state_size = state_size
        self.tries = tries
        self.nlp = spacy.load("en_core_web_sm")
        self._party_db_path = party_db_path
        self._tescreal_db_path = tescreal_db_path

    @property
    @lru_cache(maxsize=None)
    def party_model(self):
        with open(self._party_db_path, 'r') as f:
            party_db = f.read()
        return self.build_model(party_db)

    @property
    @lru_cache(maxsize=None)
    def tescreal_model(self):
        with open(self._tescreal_db_path, 'r') as f:
            tescreal_db = f.read()
        return self.build_model(tescreal_db)

    @lru_cache(maxsize=None)
    def combined_model(self):
        return markovify.combine([self.party_model, self.tescreal_model], [2, 1])

    def build_model(self, corpus):
        return POSifiedText(corpus, nlp=self.nlp, state_size=self.state_size)

    def ensure_subject(self, sentence):
        doc = self.nlp(sentence)
        has_subject = any([word.dep_ == "nsubj" for word in doc])
        return sentence if has_subject else None

    def generate_paragraph(self, model, num_sentences, start_with=None):
        paragraph = []

        # Generate the first sentence with the given start, if provided
        if start_with:
            try:
                sentence = model.make_sentence_with_start(start_with, tries=self.tries)
            except ParamError:
                sentence = model.make_sentence(tries=self.tries)

            if sentence and self.ensure_subject(sentence):
                paragraph.append(sentence)
                num_sentences -= 1  # Decrement num_sentences as we've already generated one sentence

        # Generate the remaining sentences
        for _ in range(num_sentences):
            sentence = model.make_sentence(tries=self.tries)
            if sentence and self.ensure_subject(sentence):
                paragraph.append(sentence)

        return ' '.join(paragraph)

    def generate_experience(self, num_sentences=6):
        return format_text(self.generate_paragraph(self.combined_model(), num_sentences=6, start_with="You"))



