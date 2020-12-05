import os
import re
import multiprocessing as mp

from american_soundex import AmericanSoundex


class MatchFinder:
    """Class for finding matches of word in file.

        The only public method here should be get_matches(...), but
        process_chunk(...) had to be opened for multiprocessing and
        validate_input(...) for testing (so shut up already, pylint!).
        It also removes all numbers and special symbols from the matches,
        I'm not sure whether it's ok or not.
    """

    def __init__(self):
        self.__match_dict = {}

    def get_matches(
            self,
            filepath: str,
            target_word: str,
            chunk_size: int = 1024,
            num_results: int = 5
    ) -> list[str]:
        """Scans filename for matches of target_word and returns List of top num_results matches

            Args:
                filepath: File to look matches in.
                target_word: Word to look matches for.
                chunk_size: File chunk size to read and process at one time.
                num_results: Number of results to return

            Returns:
                List of top num_results matches of target_word in filename

            """
        self.validate_input(filepath, target_word)

        target_code = AmericanSoundex.get_word_code(target_word)

        pool = mp.Pool(mp.cpu_count() - 2)

        with open(filepath, 'r', encoding="utf-8") as file:
            for chunk in self.__read_file_in_chunks(file, chunk_size):
                pool.apply_async(
                    self.process_chunk,
                    (chunk, target_code),
                    callback=self.__on_chunk_processed
                )

        pool.close()
        pool.join()

        matches = list(dict(sorted(
            self.__match_dict.items(),
            key=lambda item: item[1],
            reverse=True
        )).keys())

        return [matches[i] for i in range(min(num_results, len(matches)))]

    @staticmethod
    def __read_file_in_chunks(file, chunk_size: int) -> str:
        while True:
            chunk = file.read(chunk_size)

            if not chunk:
                break

            last_symbol = chunk[len(chunk) - 1]
            while last_symbol not in (' ', '\n'):
                last_symbol = file.read(1)
                if not last_symbol:
                    break
                chunk += last_symbol

            yield chunk

    @staticmethod
    def process_chunk(chunk: str, target_code: str) -> dict[str, int]:
        chunk = re.sub('[^A-Za-z \n]+', '', chunk)
        words = chunk.split()

        chunk_matches = {}

        for word in words:
            if word == '':
                continue

            for i in range(len(target_code), 0, -1):
                if AmericanSoundex.get_word_code(word)[:i] == target_code[:i]:
                    if word not in chunk_matches.keys():
                        chunk_matches[word] = i

        return chunk_matches

    def __on_chunk_processed(self, chunk_matches: dict[str, int]) -> None:
        for word, threshold in chunk_matches.items():
            if word not in self.__match_dict.keys():
                self.__match_dict[word] = threshold

    @staticmethod
    def validate_input(filepath: str, target_word: str) -> None:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"'{filepath}' doesn't exist")

        if not target_word.isalpha():
            raise TypeError("Target word should only contain letters")
