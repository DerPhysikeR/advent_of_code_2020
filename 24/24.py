from collections import defaultdict, namedtuple
from sys import argv

Point = namedtuple("Point", "x, y")

DIRECTION_DICT = {
    "e": Point(1, 0),
    "se": Point(0.5, -1),
    "sw": Point(-0.5, -1),
    "w": Point(-1, 0),
    "nw": Point(-0.5, 1),
    "ne": Point(0.5, 1),
}


def read_tile_flips(filename):
    with open(filename) as stream:
        return [split_instructions(line) for line in stream.read().strip().split("\n")]


def split_instructions(instructions):
    """
    >>> split_instructions("esew")
    ['e', 'se', 'w']
    >>> split_instructions("nwwswee")
    ['nw', 'w', 'sw', 'e', 'e']
    """
    instructions = list(reversed(instructions))
    split_instructions_ = []
    while len(instructions) > 0:
        current = ""
        while current not in DIRECTION_DICT:
            current += instructions.pop()
        split_instructions_.append(current)
    return split_instructions_


def initialize_tiles(tile_flips):
    black_tiles = set()
    for instructions in tile_flips:
        position = Point(0, 0)
        for instruction in instructions:
            move = DIRECTION_DICT[instruction]
            position = Point(position.x + move.x, position.y + move.y)
        if position in black_tiles:
            black_tiles.remove(position)
        else:
            black_tiles.add(position)
    return black_tiles


if __name__ == "__main__":
    tile_flips = read_tile_flips(argv[-1])
    black_tiles = initialize_tiles(tile_flips)
    print(black_tiles)
    print(len(black_tiles))
