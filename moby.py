import os
import re
import numpy
import string
import pathlib
import logging
import cmudict
from typing import List, Dict, Optional, Any
from functools import lru_cache
from collections import Counter
import spacy
from spacy import attrs
from spacy import tokens
from spacy import vocab

# Average reading speeds of people.
CHILD_WPM = 180
ADULT_WPM = 265

log = logging.getLogger("moby")

_nlp: spacy.lang.en.English = spacy.load("en_core_web_lg")
# _nlp: spacy.lang.en.English = spacy.load("en_core_web_sm")

# Handy for syllable counting.
phoneme_dict: Dict = cmudict.dict()


class Moby:
    """
    Base class for source texts.
    """

    def __init__(self, text_path: str, limiter: Optional[int] = None):
        text = self._load_text(text_path)
        self.ch_text = self._split_by_chapter(text, limiter)
        self.ch_doc = self._make_ch_doc(self.ch_text)

    @staticmethod
    def _split_by_chapter(text: str, limiter: Optional[int]) -> Dict[str, str]:
        p = re.compile(r"(CHAPTER \d\d?\d?)")
        # split and toss the first title item
        # limiter truncates the number of chapters for faster feedback
        if limiter:
            sp = p.split(text)[1 : (2 * limiter + 1)]
        else:
            sp = p.split(text)[1:]
        # odd items are chapters, even is the text
        # construct dictionary with chapters keyed to dict for the text and doc
        chapters = dict(zip([s.replace(" ", "_").lower() for s in sp[::2]], sp[1::2]))
        return chapters

    @staticmethod
    def _load_text(path: str) -> str:
        """Loads and reads the book file."""
        with open(path, "r") as f:
            text = f.read()
        return text

    @staticmethod
    def _make_ch_doc(ch_text: Dict[str, str]) -> Dict[str, tokens.doc.Doc]:
        """Make docs for each chapter."""
        ch_doc = {}
        for chapter, text in ch_text.items():
            log.debug(f"generating doc for {chapter}")
            ch_doc[chapter] = _nlp(text)
        return ch_doc

    @staticmethod
    def cmu_syl(word: str) -> int:
        """
        Look up the word in the cmu phoneme dictionary and use the first option
        count the hard vowels that end in a digit.
        """
        return len(
            [ph for ph in phoneme_dict[word][0] if ph.strip(string.ascii_letters)]
        )

    @staticmethod
    def naive_syl(word: str) -> int:
        """
        Look up word in pyphen dictionary and count hyphens in result.
        """
        return len(re.findall(r"[aiouy]+e*|e(?!d$|ly).|[td]ed|le$", word))

    @lru_cache(maxsize=None)
    def count_letters(self) -> int:
        """Counts the number of words in a document."""
        letters: int = 0
        for doc in self.ch_doc.values():
            for t in doc:
                if not t.is_punct and not t.is_space:
                    letters += len(t)
        return letters

    @lru_cache(maxsize=None)
    def count_words(self) -> int:
        """Counts the number of words in a document."""
        words: int = 0
        for doc in self.ch_doc.values():
            for t in doc:
                if not t.is_punct and not t.is_space:
                    words += 1
        return words

    @lru_cache(maxsize=None)
    def count_sentences(self) -> int:
        """Counts the number of sentences in a document."""
        sentences: int = 0
        for doc in self.ch_doc.values():
            for sent in doc.sents:
                sentences += 1
        return sentences

    @lru_cache(maxsize=None)
    def count_syllables(self) -> int:
        syllables: int = 0
        for doc in self.ch_doc.values():
            for t in doc:
                if not t.is_punct and not t.is_space:
                    word = t.norm_
                    if phoneme_dict.get(word):
                        syllables += self.cmu_syl(word)
                    else:
                        syllables += self.naive_syl(word)
        return syllables

    def automated_readablitity_index(self) -> float:
        """
        The Automated Readability Index is derived from ratios representing word
        difficulty (number of letters per word) and sentence difficulty (number of
        words per sentence). The first consideration in developing the Automated
        Readability Index was to establish that the factors used relate to those
        found in other indices. The factor relating to sentence structure (average
        number of words per sentence) is identical to that found in most currently
        used indices , such as the Coleman-Liau Index, so no verification was
        required. The verification of the relationship between the word structure
        factor was also virtually self-evident.

        ARI = 4.71 * (L/W) + 0.5 * (W/S) - 21.43
        ARI: automated Readability Index
        L: number of letters
        W: number of words
        S: number of sentences
        """
        l = self.count_letters()
        w = self.count_words()
        s = self.count_sentences()
        return 4.71 * (l / w) + 0.5 * (w / s) - 21.43

    def flesch_kincaid_reading_age(self) -> float:
        """
        Flesch Kincaid reading age is based on the Flesch Reading Ease formula
        but corrosponds to grade school levels in the United States.

        FKRA = (0.39 x ASL) + (11.8 x ASW) - 15.59
        FKRA: Flesch Kincaid Reading Age
        ASL: Average Sentence Length
        ASW: Average number of Syllables per Word
        """
        asl = self.count_words() / self.count_sentences()
        asw = self.count_syllables() / self.count_words()
        return (0.39 * asl) + (11.8 * asw) - 15.59

    def flesch_reading_ease(self) -> float:
        """
        The Flesch Reading Ease Formula is a simple approach to assess the
        grade-level of the reader. It’s also one of the few accurate measures
        around that we can rely on without too much scrutiny. This formula is best
        used on school text. It has since become a standard readability formula
        used by many US Government Agencies, including the US Department of
        Defense. However, primarily, we use the formula to assess the difficulty
        of a reading passage written in English.

        RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)
        RE: Reading Ease
        ASL: Average Sentence Length
        ASW: Average number of Syllables per Word
        """
        asl = self.count_words() / self.count_sentences()
        asw = self.count_syllables() / self.count_words()
        return 206.835 - (1.015 * asl) - (84.6 * asw)

    def propn(self) -> Counter:
        propn_freq: Counter = Counter()
        for doc in self.ch_doc.values():
            for t in doc:
                if t.pos_ == "PROPN":
                    propn_freq[t.norm_] += 1
        return propn_freq

    def statistics(self) -> Dict[str, Any]:
        return {
            "# chapters": len(self.ch_doc.keys()),
            "# sentences": self.count_sentences(),
            "# words": self.count_words(),
            "reading time (adult)": f"{(self.count_words() / ADULT_WPM) / 60:0.2f} hours",
            "reading time (child)": f"{(self.count_words() / CHILD_WPM) / 60:0.2f} hours",
        }

    def indexes(self) -> Dict[str, Any]:
        return {
            "flesch reading ease": self.flesch_reading_ease(),
            "flesch kincaid reading age": self.flesch_kincaid_reading_age(),
            "automated readability index": self.automated_readablitity_index(),
        }
