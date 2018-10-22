from . import counters


def test_naive_syllables_in_word():
    assert counters.naive_syllables_in_word("hello") == 2
    assert counters.naive_syllables_in_word(";") == 0
