"""Flood-fill to count chambers in a cave.
CS 210 project.
Ryan Maki, 10/24/22
Credits: Francis's and Eliza's Help Hours
"""


import doctest
import cave
import config
import cave_view


def scan_cave(cavern: list[list[str]]) -> int:
    """Scan the cave for air pockets.  Return the number of
    air pockets encountered.

    >>> cavern_1 = cave.read_cave("data/tiny-cave.txt")
    >>> scan_cave(cavern_1)
    1
    >>> cavern_2 = cave.read_cave("data/cave.txt")
    >>> scan_cave(cavern_2)
    3
    """
    chamber_count = 0
    for row_i in range(len(cavern)):
        for col_i in range(len(cavern[0])):
            if cavern[row_i][col_i] == cave.AIR:
                chamber_count += 1
                fill(cavern, row_i, col_i)
                cave_view.change_water()
    return chamber_count


'''
def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Pour water into cell at row_i, col_i"""
    cavern[row_i][col_i] = cave.WATER
    cave_view.fill_cell(row_i, col_i)
'''


def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
    if (row_i >= 0 and row_i < len(cavern)
        and col_i >= 0 and col_i < len(cavern[0])
        and cavern[row_i][col_i] == cave.AIR):
        cavern[row_i][col_i] = cave.WATER
        cave_view.fill_cell(row_i, col_i)
        fill(cavern, row_i + 1, col_i)
        fill(cavern, row_i - 1, col_i)
        fill(cavern, row_i, col_i + 1)
        fill(cavern, row_i, col_i - 1)
    else:
        return


'''
def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
    if (row_i < 0 or row_i >= len(cavern)
        or col_i < 0 or col_i >= len(cavern[0])
        or cavern[row_i][col_i] != cave.AIR):
        return
    else:
        cavern[row_i][col_i] = cave.WATER
        cave_view.fill_cell(row_i, col_i)
        fill(cavern, row_i + 1, col_i)
        fill(cavern, row_i - 1, col_i)
        fill(cavern, row_i, col_i + 1)
        fill(cavern, row_i, col_i - 1)
'''


def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern, config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.prompt_to_close()


if __name__ == "__main__":
    main()
