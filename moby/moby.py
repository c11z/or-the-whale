import os
import numpy
import spacy
from typing import List
from spacy import attrs
from spacy import tokens
from spacy import vocab

# Original Source
# https://www.gutenberg.org/files/2701/old/moby10b.txt
ORIGINAL_TEXT_PATH = "/script/data/original_moby_dick.txt"
ABRIDGED_TEXT_PATH = "/script/data/abridged_moby_dick.txt"

ORIGINAL_DOC_PATH = "/script/data/original_moby_dick.doc"
ABRIDGED_DOC_PATH = "/script/data/abridged_moby_dick.doc"


_nlp: spacy.lang.en.English = spacy.load("en")


class Text(object):
    """
    Base class for source texts.
    """

    def _make_doc(self, text: str, chunk_size: int = 100000) -> tokens.Doc:
        """
        Make single spaCy document from 1 or more chunks of text, to get around
        heavy memory requirements.
        """
        words: List = []
        spaces: List = []
        np_arrays: List = []
        cols: List = [
            attrs.POS,
            attrs.TAG,
            attrs.DEP,
            attrs.HEAD,
            attrs.ENT_IOB,
            attrs.ENT_TYPE,
        ]
        text_length: int = len(text)
        i: int = 0
        while i < text_length:
            chunk_doc = _nlp(text[i : i + chunk_size])
            words.extend(tok.text for tok in chunk_doc)
            spaces.extend(bool(tok.whitespace_) for tok in chunk_doc)
            np_arrays.append(chunk_doc.to_array(cols))
            i += chunk_size
        # Initialize the dock from words and spaces.
        doc = tokens.Doc(_nlp.vocab, words=words, spaces=spaces)
        doc = doc.from_array(cols, numpy.concatenate(np_arrays, axis=0))
        return doc

    def _load_text(self, path: str) -> str:
        """Loads and reads the book file."""
        with open(path, "r") as f:
            text = f.read()
        return text

    def _load_doc(self, doc_path: str, text: str) -> tokens.doc.Doc:
        """If doc file exists, then unpickle, else make the doc."""

        if os.path.isfile(doc_path):
            doc = tokens.Doc(vocab.Vocab()).from_disk(doc_path)
        else:
            doc = self._make_doc(text)
            doc.to_disk(doc_path)
        return doc


class Original(Text):
    def __init__(self):
        self.text = self._load_text(ORIGINAL_TEXT_PATH)
        self.doc = self._load_doc(ORIGINAL_DOC_PATH, self.text)


class Abridged(Text):
    def __init__(self):
        self.text = self._load_text(ABRIDGED_TEXT_PATH)
        self.doc = self._load_doc(ABRIDGED_DOC_PATH, self.text)
