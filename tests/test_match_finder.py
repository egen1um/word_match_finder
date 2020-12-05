import os

import pytest

from match_finder import MatchFinder

filename = "dummy_file.txt"


def test_filename_input_validation():
    if os.path.isfile(filename):
        os.remove(filename)

    with pytest.raises(FileNotFoundError):
        MatchFinder().get_matches(filename, "dummy")


def test_target_word_input_validation():
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            file.write("dummy")

    with pytest.raises(TypeError):
        MatchFinder().validate_input(filename, "")

    with pytest.raises(TypeError):
        MatchFinder().validate_input(filename, "b@d data")

    with pytest.raises(TypeError):
        MatchFinder().validate_input(filename, "333")

    os.remove(filename)


def test_match_finder():
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            file.write("dummy brocolli damy lasagna dimu d7mk")

    assert ["dummy", "damy", "dimu", "dmk"] == MatchFinder().get_matches(filename, "dummy")

    os.remove(filename)
