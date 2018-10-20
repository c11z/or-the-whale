from .moby import Text


class FakeText(Text):
    def __init__(self):
        self.text = self._load_text("/script/data/test.txt")
        self.doc = self._make_doc(self.text, chunk_size=1000)


def test_make_doc():
    t = FakeText()
    assert len(list(t.doc.sents)) == 1
    assert len(t.doc) == 11
