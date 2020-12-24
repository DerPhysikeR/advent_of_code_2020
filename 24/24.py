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


def find_neighbors(point):
    for direction in DIRECTION_DICT.values():
        yield Point(point.x + direction.x, point.y + direction.y)


def evolve_tiles(black_tiles):
    black_neighbor_count = defaultdict(int)
    for tile in black_tiles:
        for neighbor in find_neighbors(tile):
            if neighbor in black_tiles:
                black_neighbor_count[tile] += 1
            else:
                black_neighbor_count[neighbor] += 1
    new_black_tiles = set()
    for tile, count in black_neighbor_count.items():
        if tile in black_tiles and count in set([1, 2]):
            new_black_tiles.add(tile)
        if tile not in black_tiles and count == 2:
            new_black_tiles.add(tile)
    return new_black_tiles


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

    # part 1
    black_tiles = initialize_tiles(tile_flips)
    print(len(black_tiles))

    # part 2
    for day in range(1, 100 + 1):
        black_tiles = evolve_tiles(black_tiles)
        print(f"Day {day}: {len(black_tiles)}")
