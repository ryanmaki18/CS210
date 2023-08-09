"""Boggler:  Boggle game solver. CS 210, Fall 2022.
Ryan Maki
Credits: Help hours multiple times
"""


import doctest
import config
import sys
import board_view


# Boggle rules
MIN_WORD = 3   # A word must be at least 3 characters to count


# Possible search outcomes
NOPE = "Nope"       # Not a match, nor a prefix of a match
MATCH = "Match"     # Exact match to a valid word
PREFIX = "Prefix"   # Not an exact match, but a prefix (keep searching!)


# Board dimensions
N_ROWS = 4
N_COLS = N_ROWS
BOARD_SIZE = N_ROWS * N_COLS


# Special character in position that is
# already in use
IN_USE = "@"


def allowed(s: str) -> bool:
    """Is s a legal Boggle word?

    >>> allowed("am")  ## Too short
    False

    >>> allowed("de novo")  ## Non-alphabetic
    False

    >>> allowed("about-face")  ## Non-alphabetic
    False
    """
    
    if len(s) >= MIN_WORD and s.isalpha():
        return True
    return False


def normalize(s: str) -> str:
    """Canonical for strings in dictionary or on board
    >>> normalize("filter")
    'FILTER'
    """
    return s.upper()


def read_dict(path: str) -> list[str]:
    """Returns ordered list of valid, normalized words from dictionary.

    >>> read_dict("data/shortdict.txt")
    ['ALPHA', 'BETA', 'DELTA', 'GAMMA', 'OMEGA']
    """
    with open(path, newline="") as dict_file:
        location = []
        for element in dict_file:
            word = element.strip()
            if not allowed(word):
                pass
            else:
                location.append(normalize(word))
        return sorted(location)


def search(candidate: str, word_list: list[str]) -> str:
    """Determine whether candidate is a MATCH, a PREFIX of a match, or a big NOPE
    Note word list MUST be in sorted order.

    >>> search("ALPHA", ['ALPHA', 'BETA', 'GAMMA']) == MATCH
    True

    >>> search("BE", ['ALPHA', 'BETA', 'GAMMA']) == PREFIX
    True

    >>> search("FOX", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True

    >>> search("ZZZZ", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True
    """
    low = 0
    high = len(word_list) - 1
    while low <= high:
        mid = high + low // 2
        if word_list[mid] == candidate:
            return MATCH
        elif word_list[mid] < candidate:
            low = mid + 1
        elif word_list[mid] > candidate:
            high = mid - 1
    if low < len(word_list) and word_list[low].startswith(candidate):
        return PREFIX 
    return NOPE


def get_board_letters() -> str:
    """Get a valid string to form a Boggle board
    from the user.  May produce diagnostic
    output and quit.
    """
    while True:
        board_string = input("Boggle board letters (or 'return' to exit)> ")
        if allowed(board_string) and len(board_string) == BOARD_SIZE:
            return board_string
        elif len(board_string) == 0:
            print(f"OK, sorry it didn't work out")
            sys.exit(0)
        else:
            print(f'"{board_string}" is not a valid Boggle board')
            print(f'Please enter exactly 16 letters (or empty to quit)')


def unpack_board(letters: str) -> list[list[str]]:
    """Unpack a single string of characters into
    a matrix of individual characters, N_ROWS x N_COLS.

    >>> unpack_board("abcdefghijklmnop")
    [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
    """
    new_list = [[] for x in range(N_ROWS)]
    row_i = 0
    list_i = 0
    for i in range(len(letters)):
        new_list[row_i].append(letters[i])
        list_i += 1
        if list_i == N_ROWS:
            row_i += 1
            list_i = 0
    return new_list


def boggle_solve(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all the words that can be made by traversing
    the boggle board in all 8 directions.  Returns sorted list without
    duplicates.

    >>> board = unpack_board("PLXXMEXXXAXXSXXX")
    >>> words = read_dict("data/dict.txt")
    >>> boggle_solve(board, words)
    ['AMP', 'AMPLE', 'AXE', 'AXLE', 'ELM', 'EXAM', 'LEA', 'MAX', 'PEA', 'PLEA', 'SAME', 'SAMPLE', 'SAX']
    """
    solutions = []

    def solve(row: int, col: int, prefix: str):
        """One solution step"""
        if not (row < 0 or row >= N_ROWS or col < 0 or col >= N_COLS):
            if board[row][col] == IN_USE:
                return
            letter = board[row][col]
            prefix = prefix + letter
            status = search(prefix, words)
            if status == NOPE:
                return
            if status == MATCH:
                solutions.append(prefix)
            if status == MATCH or status == PREFIX:
                # Keep searching
                board[row][col] = IN_USE  # Prevent reusing
                board_view.mark_occupied(row, col)
                # *** Recursive calls go here ***
                for d_row in [0, -1, 1]:
                    for d_col in [0, -1, 1]:
                        solve(row + d_row, col + d_col, prefix)         ## Make recursive col with row+d_row, col+d_col
                # Restore letter for further search
                board_view.mark_unoccupied(row, col)
                board[row][col] = letter
        return

    # Look for solutions starting from each board position
    for row_i in range(N_ROWS):
        for col_i in range(N_COLS):
            solve(row_i, col_i, "")

    # Return solutions without duplicates, in sorted order
    solutions = list(set(solutions))
    return sorted(solutions)


# Max word length is 16, so we can just list all
# the point values.
#
#         0  1  2  3  4  5  6  7   8   9  10  11  12  13  14  15  16
POINTS = [0, 0, 0, 1, 1, 2, 3, 5, 11, 11, 11, 11, 11, 11, 11, 11, 11 ]


def word_score(word: str) -> int:
    """Standard point value in Boggle"""
    assert len(word) <= 16
    return POINTS[len(word)]


def score(solutions: list[str]) -> int:
    """Sum of scores for each solution

    >>> score(["ALPHA", "BETA", "ABSENTMINDED"])
    14
    """
    total_score = 0
    for word in solutions:
        total_score += word_score(word)
    return total_score


def main():
    words = read_dict(config.DICT_PATH)
    board_string = get_board_letters()
    board_string = normalize(board_string)
    board = unpack_board(board_string)
    board_view.display(board)
    solutions = boggle_solve(board, words)
    print(solutions)
    print(f"{score(solutions)} points")
    board_view.prompt_to_close()


if __name__ == "__main__":
    doctest.testmod()
    print("Doctests complete")
    main()
