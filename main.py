"""
My Great Illustrated Classic Text Analysis

MAINTAINER = c11z <corydominguez@gmail.com>
WEBSITE = https://github.com/c11z/great_illustrated_classic
LICENSE = MIT

Comparison between origin and abridged versions of the Moby Dick novel.
"""
from typing import Tuple


def load_texts() -> Tuple[str, str]:
    """Loads and reads the book files into variables."""
    # Original Source
    # https://www.gutenberg.org/files/2701/old/moby10b.txt
    original = ""
    with open("/script/data/moby_dick.txt", "r") as f:
        original = f.read()
    abridged = ""
    # Abridged not processed yet
    return original, abridged


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


if __name__ == "__main__":
    main()
