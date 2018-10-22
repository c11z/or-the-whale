import cmudict
import string
from spacy import tokens
from typing import Dict, Set
from curses.ascii import isdigit

# Average reading speeds of people.
CHILD_WPM = 180
ADULT_WPM = 265
# Handy for syllable counting.
phoneme_dict: Dict = cmudict.dict()
# A transition that replaces dashes with spaces and removes all special
# characters except for punctuation.
clean_trans = str.maketrans("-", " ", '"#$%&()*+,/:;<=>@[\\]^_`{|}~')
# A transition that removes punctiation.
punct_trans = str.maketrans("", "", ".!?")
# Don't forget the y
vowels: Set = set("aeiouy")


def adult_reading_time(text: str) -> int:
    """Calculates the reading time of the text by an average adult in minutes"""
    return int(count_words(text) / ADULT_WPM)


def child_reading_time(text: str) -> int:
    """Calclulates the reading time of the text by a child in minutes"""
    return int(count_words(text) / CHILD_WPM)


def count_syllables(doc: tokens.doc.Doc) -> int:
    """
    Count all the syllables in piece of text. Try to use the cmu phoneme
    Dictionary if possible otherwise fall back to naive algorithm that is
    not as accurate.
    """
    syllable_count = 0
    for word in doc:
        clean_word = word.lower()
        if phoneme_dict.get(clean_word):
            syllable_count += cmu_syllables_in_word(clean_word)
        else:
            syllable_count += naive_syllables_in_word(clean_word)
    return syllable_count


def cmu_syllables_in_word(word: str) -> int:
    """
    Look up the word in the cmu phoneme dictionary and use the first option
    count the hard vowels that end in a digit.
    """
    return len([ph for ph in phoneme_dict[word][0] if ph.strip(string.ascii_letters)])


def naive_syllables_in_word(word: str) -> int:
    """
    Use the number of vowels in a word as a proxy for the number of syllables.
    """
    return len([char for char in word if char in vowels])


def count_letters(text: str) -> int:
    """Counts the number of letter in a document."""
    return len(text.translate(punct_trans)) - text.count(" ") - text.count("\n")


def count_words(text: str) -> int:
    """Counts the number of words in a document."""
    return len(text.split())


def count_sentences(text: str) -> int:
    """Counts the number of sentences in a document."""
    return text.count(".") + text.count("!") + text.count("?")


def count_paragraphs(text: str) -> int:
    """Counts the number of paragraphs in a document."""
    return text.count("\n\n")
