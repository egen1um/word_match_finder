from american_soundex import AmericanSoundex


def test_soundex_code():
    assert AmericanSoundex.get_word_code("JAJJHWJbaj", 10) == "J212000000"


def test_wiki_examples():
    wiki_examples = {
        "Robert": "R163",
        "Rupert": "R163",
        "Rubin": "R150",
        "Ashcraft": "A261",
        "Ashcroft": "A261",
        "Tymczak": "T522",
        "Pfister": "P236",
        "Honeyman": "H555"
    }

    for word, code in wiki_examples.items():
        assert code == AmericanSoundex.get_word_code(word)
