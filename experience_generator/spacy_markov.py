import spacy
import markovify
from markovify.text import ParamError

from functools import lru_cache
import re

from .utils import format_text



def has_verb(sentence, nlp):
    """Check if the sentence has a verb."""
    doc = nlp(sentence)
    return any(token.pos_ == "VERB" for token in doc)


def is_sentence_complete(sentence, nlp):
    doc = nlp(sentence)
    
    # Check if sentence ends with a conjunction
    if doc[-1].pos_ in ["CONJ"]:
        return False
    
    return True

def is_dangling_clause(sentence, nlp):
    """Check if the sentence is a dangling clause."""
    # Check for ending conjunctions or relative pronouns
    if re.search(r'\b(and|or|but|because|if|that|which|when|where|while)\b[.!?]?$', sentence, re.I):
        return True
    # Check for missing verbs
    if not has_verb(sentence, nlp):
        return True
    return False

    
def handle_dangling_clause(sentence, model):
    """Attempt to complete a sentence with a dangling clause."""
    if re.search(r'\b(and|or|but|because|if|that|which|when|where|while)\b[.!?]?$', sentence, re.I):
        additional_clause = model.make_sentence(tries=5)
        if additional_clause:
            return sentence + " " + additional_clause
    return sentence



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

    def generate_sentence(self, model, start_with=None, max_retries=10, max_overlap_ratio=0.9, max_overlap_total=15):
        """Generate a valid sentence using the model."""
        sentence = None
        retries = 0
    
        while retries < max_retries:
            
            if start_with:
                try:
                    sentence = model.make_sentence_with_start(start_with, tries=self.tries,
                                 max_overlap_ratio=max_overlap_ratio, max_overlap_total=max_overlap_total)
                except ParamError:
                    sentence = model.make_sentence(tries=self.tries, max_overlap_ratio=max_overlap_ratio, 
                                                    max_overlap_total=max_overlap_total)
            else:
                sentence = model.make_sentence(tries=self.tries, max_overlap_ratio=max_overlap_ratio, 
                                                    max_overlap_total=max_overlap_total)
        
            print(sentence)
            # Validate the generated sentence
            if sentence and self.ensure_subject(sentence) and is_sentence_complete(sentence, self.nlp):
                if is_dangling_clause(sentence, self.nlp):
                    sentence = handle_dangling_clause(sentence, model)
                return sentence
            retries += 1
        
        # Handle case where max_retries is reached
        return sentence

    
    def generate_paragraph(self, model, num_sentences, start_with=None):
        paragraph = []
        generated_sentences = set()  # to keep track of generated sentences
    
        # Generate the first sentence with the given start, if provided
        if start_with:
            sentence = self.generate_sentence(model, start_with)
            if sentence:
                paragraph.append(sentence)
                generated_sentences.add(sentence)
                num_sentences -= 1  # Decrement num_sentences as we've already generated one sentence
    
        # Generate the remaining sentences
        while len(paragraph) < num_sentences:
            sentence = self.generate_sentence(model)
            if sentence and sentence not in generated_sentences:
                paragraph.append(sentence)
                generated_sentences.add(sentence)
    
        return ' '.join(paragraph)

    def generate_experience(self, num_sentences=7):
        return format_text(self.generate_paragraph(self.combined_model(), num_sentences=num_sentences, start_with="You"))




