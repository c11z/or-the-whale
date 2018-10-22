from .counters import *
from spacy import tokens


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


def flesch_reading_ease(text: str, doc: tokens.Doc) -> float:
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
    asw = count_syllables(doc) / count_words(text)
    return 206.835 - (1.015 * asl) - (84.6 * asw)


def flesch_kincaid_reading_age(text: str, doc: tokens.Doc) -> float:
    """
    Flesch Kincaid reading age is based on the Flesch Reading Ease formula
    but corrosponds to grade school levels in the United States.

    FKRA = (0.39 x ASL) + (11.8 x ASW) - 15.59
    FKRA: Flesch Kincaid Reading Age
    ASL: Average Sentence Length
    ASW: Average number of Syllables per Word
    """
    asl = count_words(text) / count_sentences(text)
    asw = count_syllables(doc) / count_words(text)
    return (0.39 * asl) + (11.8 * asw) - 15.59


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
