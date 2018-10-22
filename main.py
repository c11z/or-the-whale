"""
My Great Illustrated Classic Text Analysis

MAINTAINER = c11z <corydominguez@gmail.com>
WEBSITE = https://github.com/c11z/great_illustrated_classic
LICENSE = MIT

Comparison between original and an abridged version of the Moby Dick novel.
"""
import os
import sys
import fire
import logging
import moby


def cache() -> None:
    """
    Remove data/*.doc files and recache spaCy doc data structures for the
    Original and Abridged texts.
    """
    if os.path.exists(moby.ORIGINAL_DOC_PATH):
        os.remove(moby.ORIGINAL_DOC_PATH)
    if os.path.exists(moby.ABRIDGED_DOC_PATH):
        os.remove(moby.ABRIDGED_DOC_PATH)
    moby.Abridged()
    logging.info("Cached abridged Moby Dick as spaCy doc.")
    moby.Original()
    logging.info("Cached original Moby Dick as spaCy doc.")


def noop() -> None:
    logging.info("No operation.")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%dT%I:%M:%S",
    )
    fire.Fire()
