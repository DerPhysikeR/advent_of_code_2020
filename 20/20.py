from collections import namedtuple
from copy import deepcopy
from functools import reduce
from itertools import product
from sys import argv


def read_tiles(filename):
    with open(filename) as stream:
        return [Tile.from_string(t) for t in stream.read().strip().split("\n\n")]


class Image:
    def __init__(self, data, modifications=None):
        self.data = data
        if not modifications:
            self._modifications = []
        else:
            self._modifications = modifications

    def __repr__(self):
        return f"Image(({len(self.data)}, {len(self.data[0])}))"

    def __str__(self):
        return "\n".join(self.data)

    def flip_horizontal(self):
        new_data = []
        for line in self.data:
            new_data.append(line[::-1])
        return Image(new_data, self._modifications + ["fh"])

    def rotate_right(self):
        new_data = []
        for column in zip(*self.data):
            new_data.append("".join(column[::-1]))
        return Image(new_data, self._modifications + ["rr"])


class Tile(Image):
    def __init__(self, id_, data, modifications=None):
        self.id_ = id_
        super().__init__(data, modifications)

    def __repr__(self):
        return f"Tile({self.id_}, ({len(self.data)}, {len(self.data[0])}))"

    def flip_horizontal(self):
        new_image = super().flip_horizontal()
        return Tile(self.id_, new_image.data, new_image._modifications)

    def rotate_right(self):
        new_image = super().rotate_right()
        return Tile(self.id_, new_image.data, new_image._modifications)

    @classmethod
    def from_string(cls, tile_string):
        lines = tile_string.split("\n")
        return cls(int(lines[0].split(" ")[1][:-1]), lines[1:])

    def fits(self, other, direction):
        if direction == (0, 1):  # right
            return "".join(l[-1] for l in self.data) == "".join(
                l[0] for l in other.data
            )
        if direction == (-1, 0):  # up
            return self.data[0] == other.data[-1]
        if direction == (0, -1):  # left
            return "".join(l[0] for l in self.data) == "".join(
                l[-1] for l in other.data
            )
        if direction == (1, 0):  # down
            return self.data[-1] == other.data[0]
        raise ValueError(f"Invalid direction `{direction}`.")


Point = namedtuple("Point", "row, col")


def get_neighbors(point):
    return set(
        [
            Point(point.row, point.col + 1),
            Point(point.row - 1, point.col),
            Point(point.row, point.col - 1),
            Point(point.row + 1, point.col),
        ]
    )


def fits_in_grid(grid, new_point, tile):
    neighbors_to_check = get_neighbors(new_point).intersection(grid)
    for neighbor in neighbors_to_check:
        direction = (neighbor.row - new_point.row, neighbor.col - new_point.col)
        if not tile.fits(grid[neighbor], direction):
            return False
    return True


def place_fitting_tile(tile_grid, tiles, point_to_check):
    for i, tile in enumerate(tiles):
        for oriented_tile in generate_orientations(tile):
            if fits_in_grid(tile_grid, point_to_check, oriented_tile):
                tile_grid[point_to_check] = oriented_tile
                del tiles[i]
                return get_neighbors(point_to_check).difference(tile_grid)
    return set()


def assemble_image_from_tiles(tiles):
    tiles = deepcopy(tiles)
    tile_grid = {Point(0, 0): tiles.pop()}
    to_search = get_neighbors(Point(0, 0))
    while len(to_search) > 0:
        point_to_check = to_search.pop()
        new_points_to_search = place_fitting_tile(tile_grid, tiles, point_to_check)
        to_search = to_search.union(new_points_to_search)
    assert len(tiles) == 0
    return tile_grid


def generate_orientations(tile):
    yield tile
    yield (tile := tile.rotate_right())
    yield (tile := tile.rotate_right())
    yield (tile := tile.rotate_right())
    tile = tile.rotate_right().flip_horizontal()
    yield tile
    yield (tile := tile.rotate_right())
    yield (tile := tile.rotate_right())
    yield (tile := tile.rotate_right())


if __name__ == "__main__":
    tiles = read_tiles(argv[-1])
    image = assemble_image_from_tiles(tiles)
    rows, cols = [p.row for p in image], [p.col for p in image]
    minrow, maxrow = min(rows), max(rows)
    mincol, maxcol = min(cols), max(cols)
    corner_tile_ids = [
        image[Point(r, c)].id_ for r, c in product([minrow, maxrow], [mincol, maxcol])
    ]
    print(reduce(lambda id1, id2: id1 * id2, corner_tile_ids))
