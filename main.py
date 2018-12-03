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
import shutil
import logging
import moby
import altair as alt
import pandas as pd
from typing import Optional, Dict
from collections import defaultdict

OUTPUT_DIR: str = "/script/output/"
# original source
# https://www.gutenberg.org/files/2701/old/moby10b.txt
ORIGINAL_TEXT_PATH = "/script/data/original_moby_dick.txt"
ABRIDGED_TEXT_PATH = "/script/data/abridged_moby_dick.txt"
# limit the number of chapters to anaylize, None is all chapters
LIMITER: Optional[int] = None

log = logging.getLogger("main")


def plot() -> None:
    data = alt.Data(
        values=[
            {"x": "A", "y": 5},
            {"x": "B", "y": 3},
            {"x": "C", "y": 6},
            {"x": "D", "y": 7},
            {"x": "E", "y": 2},
        ]
    )
    alt.Chart(data).mark_bar().encode(x="x:O", y="y:Q").save(OUTPUT_DIR + "test.html")


def propn() -> None:
    log.info("collecting proper nouns")
    a = moby.Moby(ABRIDGED_TEXT_PATH, LIMITER)
    o = moby.Moby(ORIGINAL_TEXT_PATH, LIMITER)
    combined: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"original": 0, "abridged": 0}
    )
    for noun, count in a.propn().items():
        combined[noun]["abridged"] += count
    for noun, count in o.propn().items():
        combined[noun]["original"] += count
    result = pd.DataFrame(combined).T.sort_values(
        by=["abridged", "original"], ascending=False
    )
    log.info("Proper nouns\n" + str(result))
    return None


def table() -> None:
    log.info("building statistics table")
    a = moby.Moby(ABRIDGED_TEXT_PATH, LIMITER)
    o = moby.Moby(ORIGINAL_TEXT_PATH, LIMITER)
    result = pd.DataFrame(
        [a.statistics(), o.statistics()], index=["Abridged", "Original"]
    )
    log.info("statistics\n" + str(result.T))
    result = pd.DataFrame([a.indexes(), o.indexes()], index=["Abridged", "Original"])
    log.info("indexes\n" + str(result.T))
    return None


def noop() -> None:
    log.info("No operation.")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%dT%I:%M:%S",
    )
    fire.Fire()
