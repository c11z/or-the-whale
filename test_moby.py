from moby import Moby
from typing import Optional

TEST_PATH = "/script/data/test.txt"


def test_init_no_limit():
    t = Moby("testbook", TEST_PATH)
    assert len(t.ch_text.keys()) == 2
    assert len(t.ch_doc["chapter_1"]) == 12
    assert len(t.ch_doc["chapter_2"]) == 12


def test_init_w_limit():
    t = Moby("testbook", TEST_PATH, 1)
    assert len(t.ch_text.keys()) == 1
    assert len(t.ch_doc["chapter_1"]) == 12
