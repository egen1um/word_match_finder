import sys

from match_finder import MatchFinder

if __name__ == '__main__':
    try:
        if len(sys.argv) < 3:
            raise Exception("Mandatory parameters are missing. Use tool this way: 'find.py <filename> <target word>'")

        filename = sys.argv[1]
        target_word = sys.argv[2]

        matches = MatchFinder().get_matches(filename, target_word, 1024, 5)

        for match in matches:
            print(match)
    except Exception as e:
        print(e)
