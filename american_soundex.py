import re


class AmericanSoundex:
    __consonant_map: dict[int, str] = {
        1: "bfpv",
        2: "cgjkqsxz",
        3: "dt",
        4: "l",
        5: "mn",
        6: "r"
    }
    __unpronounced_consonants = "hw"
    __vowels = "aeiouy"

    @staticmethod
    def get_word_code(word: str, length: int = 4) -> str:
        """Generates American Soundex code of given length for given word.

            Args:
                word: Word to generate code for.
                length: Code length. By standard American Soundex code uses 4 symbol length.

            Returns:
                American Soundex code of given length for given word

            """
        first_letter = word[0].upper()
        code = word.lower()
        # replace mapped consonants
        for i, chars in AmericanSoundex.__consonant_map.items():
            code = re.sub(f"[{chars}]", str(i), code)
        # remove unpronounced consonants
        code = re.sub(f"[{AmericanSoundex.__unpronounced_consonants}]", '', code)
        # replace same adjacent numbers with one number
        code = re.sub(r'([1-6])\1+', r'\1', code)
        # remove vowels
        code = first_letter + re.sub(f"[{AmericanSoundex.__vowels}]", '', code[1:])
        # add zeroes if necessary
        while len(code) < length:
            code += '0'
        code = code[:length]
        return code
