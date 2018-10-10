"""
My Great Illustrated Classic Text Analysis

MAINTAINER = c11z <corydominguez@gmail.com>
WEBSITE = https://github.com/c11z/great_illustrated_classic
LICENSE = MIT

Comparison between origin and abridged versions of the Moby Dick novel.
"""
import string
import cmudict  # type: ignore
from nltk.tokenize import word_tokenize, sent_tokenize  # type: ignore
from typing import Tuple
from curses.ascii import isdigit

# Average reading speed of an adult
CHILD_WPM = 180
ADULT_WPM = 265

phoneme_dict = cmudict.dict()

vowels = set("aeiou")

# A transition that replaces dashes with spaces and removes all special
# characters except for punctuation.
clean_trans = str.maketrans("-", " ", '"#$%&()*+,/:;<=>@[\\]^_`{|}~')
# A transition that removes punctiation.
punct_trans = str.maketrans("", "", ".!?")


def count_syllables(text: str) -> int:
    syllable_count = 0
    for word in word_tokenize(text):
        clean_word = word.lower()
        if phoneme_dict.get(clean_word):
            syllable_count += cmu_syllables_in_word(clean_word)
        else:
            syllable_count += naive_syllables_in_word(clean_word)
    return syllable_count


def cmu_syllables_in_word(word: str) -> int:
    return len([ph for ph in phoneme_dict[word][0] if ph.strip(string.ascii_letters)])


def naive_syllables_in_word(word: str) -> int:
    return len([char for char in word if char in vowels])


def load_texts() -> Tuple[str, str]:
    """Loads and reads the book files into variables."""
    # Original Source
    # https://www.gutenberg.org/files/2701/old/moby10b.txt
    original = ""
    with open("/script/data/moby_dick.txt", "r") as f:
        original = f.read()  # .translate(clean_trans)
    # Abridged not processed yet
    abridged = ""
    return original, abridged


def flesch_reading_ease(text: str) -> int:
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
    pass


def calculate_adult_reading_time(text: str) -> int:
    """Calculates the reading time of the text by an average adult in minutes"""
    return int(count_words(text) / ADULT_WPM)


def calculate_child_reading_time(text: str) -> int:
    """Calclulates the reading time of the text by a child in minutes"""
    return int(count_words(text) / CHILD_WPM)


def count_words(text: str) -> int:
    """Counts the number of words in a document."""
    return len(text.split())


def count_sentences(text: str) -> int:
    """Counts the number of sentences in a document."""
    return text.count(".") + text.count("!") + text.count("?")


def count_paragraphs(text: str) -> int:
    """Counts the number of paragraphs in a document."""
    return text.count("\n\n")


def main() -> None:
    original, abridged = load_texts()
    print(count_words(original))
    print(count_sentences(original))
    print(count_paragraphs(original))
    print(calculate_adult_reading_time(original))
    print(count_syllables(original))


if __name__ == "__main__":
    main()
