import main


def test_noop():
    assert main.noop() == None


def test_naive_syllables_in_word():
    assert main.naive_syllables_in_word("hello") == 2
    assert main.naive_syllables_in_word(";") == 0
