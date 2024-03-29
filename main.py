"""
My Great Illustrated Classic Text Analysis

MAINTAINER = c11z <corydominguez@gmail.com>
WEBSITE = https://github.com/c11z/great_illustrated_classic
LICENSE = MIT

Comparison between original and an abridged version of the Moby Dick novel.
"""
import csv
import json
import logging
import random
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Set

import altair as alt  # type: ignore
import fire  # type: ignore
import gensim as gen  # type: ignore
import pandas as pd  # type: ignore

from moby import Moby

OUTPUT_DIR: str = "/script/output"
# constant variables for book names
ABRIDGED = "abridged"
ORIGINAL = "original"
FRANKENSTEIN = "frankenstein"
# original source
# https://www.gutenberg.org/files/2701/old/0b.txt
ORIGINAL_TEXT_PATH = "/script/data/original_moby_dick.txt"
ABRIDGED_TEXT_PATH = "/script/data/abridged_moby_dick.txt"
FRANKENSTEIN_TEXT_PATH = "/script/data/frankenstein.txt"
# limit the number of chapters to anaylize, None is all chapters
LIMITER: Optional[int] = None

log = logging.getLogger("main")


def pytext() -> None:
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    train_data = []
    test_data = []
    eval_data = []
    for ch, doc in o.ch_doc.items():
        for s in doc.sents:
            r = random.random()
            if r <= 0.1:
                eval_data.append(
                    [
                        ch,
                        " ".join(
                            [
                                t.lemma_
                                for t in s
                                if not t.is_space and not t.is_punct and not t.is_stop
                            ]
                        ),
                    ]
                )
            elif r > 0.1 and r <= 0.3:
                test_data.append(
                    [
                        ch,
                        " ".join(
                            [
                                t.lemma_
                                for t in s
                                if not t.is_space and not t.is_punct and not t.is_stop
                            ]
                        ),
                    ]
                )
            else:
                train_data.append(
                    [
                        ch,
                        " ".join(
                            [
                                t.lemma_
                                for t in s
                                if not t.is_space and not t.is_punct and not t.is_stop
                            ]
                        ),
                    ]
                )
    with open("/script/moby_nn/train.tsv", "w") as train_fh:
        writer = csv.writer(train_fh, delimiter="\t")
        for row in train_data:
            writer.writerow(row)
    with open("/script/moby_nn/test.tsv", "w") as test_fh:
        writer = csv.writer(test_fh, delimiter="\t")
        for row in test_data:
            writer.writerow(row)
    with open("/script/moby_nn/eval.tsv", "w") as test_fh:
        writer = csv.writer(test_fh, delimiter="\t")
        for row in eval_data:
            writer.writerow(row)
    return None


def topic() -> None:
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    data: List = []
    data += o.sent_data()
    data += a.sent_data()
    df = pd.DataFrame(data)

    bigram_model = gen.models.Phrases(df.loc[:, "unigram_text"])
    df["bigram_text"] = df["unigram_text"].map(lambda s: "".join(bigram_model[s]))
    texts = [s.split() for s in list(df["bigram_text"]) if s]
    dictionary = gen.corpora.Dictionary(texts)
    dictionary.compactify()
    corpus = [dictionary.doc2bow(text) for text in texts]
    log.info(corpus)
    tfidf = gen.models.TfidfModel(corpus, id2word=dictionary, normalize=True)
    corpus_tfidf = tfidf[corpus]
    lda = gen.models.ldamulticore.LdaMulticore(
        corpus_tfidf, num_topics=3, id2word=dictionary
    )
    return None


def bago() -> None:
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    texts = []
    for ch, doc in o.ch_doc.items():
        texts.append(
            [
                t.lemma_
                for t in doc
                if not t.is_stop and not t.is_punct and not t.is_space
            ]
        )
    freq: Dict[str, int] = defaultdict(int)
    for text in texts:
        for t in text:
            freq[t] += 1

    log.debug([k for k, v in freq.items() if v < 3])
    return None


def vec() -> None:
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    doc = o.ch_doc["chapter_1"]
    good: Set[str] = set()
    unknown: Set[str] = set()
    for t in doc:
        if not t.is_stop and t.has_vector:
            good.add(t.text)
        if not t.is_stop and not t.has_vector:
            unknown.add(t.text)
    log.info(f"words with vectors\n{sorted(good)}")
    log.info("\n")
    log.info(f"words without vectors\n{unknown}")
    log.info(f"{doc.similarity(a.ch_doc['chapter_1'])}")
    log.info(f"{doc.vector}")
    return None


def sim() -> None:
    log.info("similarity by chapter")
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    # o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    f = Moby(FRANKENSTEIN, FRANKENSTEIN_TEXT_PATH, LIMITER)
    for a_ch, a_doc in a.ch_doc.items():
        log.info("\n")
        for o_ch, o_doc in f.ch_doc.items():
            cos = a_doc.similarity(o_doc)
            log.info(f"A({a_ch}), F({o_ch})\t{cos}")

    return None


def freq_data() -> None:

    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    search = set(
        [
            "ahab",
            "stubb",
            "queequeg",
            "starbuck",
            "pequod",
            "flask",
            "nantucket",
            "moby",
            "peleg",
            "tashtego",
            "daggoo",
            "fedallah",
            "jonah",
            "bildad",
            "pip",
            "sperm",
            "right",
            "greenland",
        ]
    )
    tag = "NNP"
    data = a.freq(search, tag) + o.freq(search, tag)

    with open("/script/output/freq.json", "w") as fh:
        json.dump(data, fh)

    scatter = []
    for word in search:
        o_count = 0
        a_count = 0
        for d in data:
            if d["word"] == word:
                if d["title"] == "original":
                    o_count += 1
                else:
                    a_count += 1
        scatter.append(
            {"word": word.capitalize(), "o_count": o_count, "a_count": a_count}
        )

    with open("/script/output/scatter.json", "w") as fh:
        json.dump(scatter, fh)

    return None


def freq_comp() -> None:
    log.info("collecting frequency counts")
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    search = set(["daggoo"])
    search_title = "_".join(search)
    tag = "NNP"
    data = alt.Data(values=(a.freq(search, tag) + o.freq(search, tag)))
    alt.Chart(data).mark_bar().encode(
        x=alt.X(
            title="normalized index",
            bin={"extent": [0, 1]},
            field="norm_index",
            type="quantitative",
        ),
        y=alt.Y(title=f"{search_title} count", aggregate="count", type="quantitative"),
        row=alt.Row(field="title", type="nominal"),
    ).save(f"{OUTPUT_DIR}/{search_title}_hist.html")
    return None


def freq_missing() -> None:
    log.info("collecting frequency counts")
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    search = set(["jonah", "bildad", "pip", "sperm", "right", "greenland"])
    title = "_".join(sorted(search))
    tag = "NNP"
    data = alt.Data(values=(o.freq(search, tag)))
    alt.Chart(data, width=1000).mark_bar().encode(
        x=alt.X(
            title="Chapter",
            bin={"extent": [1, 135], "step": 1},
            field="chapter",
            type="quantitative",
        ),
        y=alt.Y(title=f"word count", aggregate="count", type="quantitative"),
        row=alt.Row(field="word", type="nominal"),
    ).save(f"{OUTPUT_DIR}/{title}_index_hist.html")
    return None


def propn() -> None:
    log.info("collecting proper nouns")
    pd.set_option("display.max_rows", 500)
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    combined: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"original": 0, "abridged": 0}
    )
    for noun, count in a.propn().items():
        combined[noun]["abridged"] += count
    for noun, count in o.propn().items():
        combined[noun]["original"] += count
    top_a = sorted(
        combined.items(), key=lambda kv: kv[1].get("abridged", 0), reverse=True
    )
    result = pd.DataFrame(top_a)
    log.info(f"top abridged proper nouns\n{result}")
    top_o = sorted(
        combined.items(), key=lambda kv: kv[1].get("original", 0), reverse=True
    )
    result = pd.DataFrame(top_o)
    log.info(f"top original proper nouns\n{result}")
    return None


def verb() -> None:
    log.info("collecting proper nouns")
    pd.set_option("display.max_rows", 100)
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
    combined: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"original": 0, "abridged": 0}
    )
    for verb, count in a.verb().items():
        combined[verb]["abridged"] += count
    for verb, count in o.verb().items():
        combined[verb]["original"] += count
    top_a = sorted(
        combined.items(), key=lambda kv: kv[1].get("abridged", 0), reverse=True
    )
    result = pd.DataFrame(top_a)
    log.info(f"top abridged verbs\n{result}")
    top_o = sorted(
        combined.items(), key=lambda kv: kv[1].get("original", 0), reverse=True
    )
    result = pd.DataFrame(top_o)
    log.info(f"top original verbs\n{result}")
    return None


def table() -> None:
    log.info("building statistics table")
    a = Moby(ABRIDGED, ABRIDGED_TEXT_PATH, LIMITER)
    o = Moby(ORIGINAL, ORIGINAL_TEXT_PATH, LIMITER)
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
