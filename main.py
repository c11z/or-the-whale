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
from typing import Dict, Set

# Average reading speed of an adult
CHILD_WPM = 180
ADULT_WPM = 265

phoneme_dict: Dict = cmudict.dict()
vowels: Set = set("aeiouy")

# A transition that replaces dashes with spaces and removes all special
# characters except for punctuation.
clean_trans = str.maketrans("-", " ", '"#$%&()*+,/:;<=>@[\\]^_`{|}~')
# A transition that removes punctiation.
punct_trans = str.maketrans("", "", ".!?")


def count_syllables(text: str) -> int:
    """
    Count all the syllables in piece of text. Try to use the cmu phoneme
    Dictionary if possible otherwise fall back to naive algorithm that is
    not as accurate.
    """
    syllable_count = 0
    for word in word_tokenize(text):
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


def automated_readablitity_index(text: str) -> float:
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
    l = count_letters(text)
    w = count_words(text)
    s = count_sentences(text)
    return 4.71 * (l / w) + 0.5 * (w / s) - 21.43


def coleman_liau_index(text: str) -> float:
    """
    Similar to the Automated Readability Index, but unlike most of the other
    grade-level predictors, the Coleman–Liau relies on characters instead of
    syllables per word. Instead of using syllable/word and sentence length
    indices, Meri Coleman and T. L. Liau believed that computerized assessments
    understand characters more easily and accurately than counting syllables
    and sentence length.

    CLI = (0.0588 x L) - (0.296 x S) - 15.8
    CLI: Coleman Liau Index
    L: average number of Letters per 100 words
    S: average number of sentences per 100 words
    """
    words = text.split()
    word_groups = ["".join(words[i : i + 100]) for i in range(0, len(words), 100)]
    letter_count_list = [len(l) for l in word_groups]
    l = sum(letter_count_list) / len(letter_count_list)
    sentence_count_list = [count_sentences(s) for s in word_groups]
    s = sum(sentence_count_list) / len(sentence_count_list)
    return (0.0588 * l) - (0.296 * s) - 15.8


def flesch_reading_ease(text: str) -> float:
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
    asl = count_words(text) / count_sentences(text)
    asw = count_syllables(text) / count_words(text)
    return 206.835 - (1.015 * asl) - (84.6 * asw)


def flesch_kincaid_reading_age(text: str) -> float:
    """
    Flesch Kincaid reading age is based on the Flesch Reading Ease formula
    but corrosponds to grade school levels in the United States.

    FKRA = (0.39 x ASL) + (11.8 x ASW) - 15.59
    FKRA: Flesch Kincaid Reading Age
    ASL: Average Sentence Length
    ASW: Average number of Syllables per Word
    """
    asl = count_words(text) / count_sentences(text)
    asw = count_syllables(text) / count_words(text)
    return (0.39 * asl) + (11.8 * asw) - 15.59


def calculate_adult_reading_time(text: str) -> int:
    """Calculates the reading time of the text by an average adult in minutes"""
    return int(count_words(text) / ADULT_WPM)


def calculate_child_reading_time(text: str) -> int:
    """Calclulates the reading time of the text by a child in minutes"""
    return int(count_words(text) / CHILD_WPM)


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


def load_texts() -> Tuple[str, str]:
    """Loads and reads the book files into variables."""
    # Original Source
    # https://www.gutenberg.org/files/2701/old/moby10b.txt
    original = ""
    with open("/script/data/moby_dick.txt", "r") as f:
        original = f.read().translate(clean_trans)
    # Abridged not processed yet
    abridged = ""
    return original, abridged


def main() -> None:
    original, abridged = load_texts()
    print(count_words(original))
    print(count_sentences(original))
    print(count_paragraphs(original))
    print(calculate_adult_reading_time(original))
    print(count_syllables(original))
    print(flesch_reading_ease(original))
    print(flesch_kincaid_reading_age(original))
    print(coleman_liau_index(original))
    print(automated_readablitity_index(original))


if __name__ == "__main__":
    main()
