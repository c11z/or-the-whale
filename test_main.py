import main


def test_main():
    assert main.main() == None


def test_naive_syllables_in_word():
    assert main.naive_syllables_in_word("hello") == 2
    assert main.naive_syllables_in_word(";") == 0
