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

    @property
    def shape(self):
        return (len(self.data), len(self.data[0]))

    def check_mask_in_image(self, mask):
        assert self.shape == mask.shape
        for line, mline in zip(self.data, mask.data):
            for letter, mletter in zip(line, mline):
                if mletter == "#" and letter != "#":
                    return False
        return True

    def apply_mask_to_points(self, points, mask):
        list_data = [list(line) for line in self.data]
        list_mask = [list(line) for line in mask.data]
        for point in points:
            for row in range(mask.shape[0]):
                for col in range(mask.shape[1]):
                    if list_mask[row][col] == "#":
                        list_data[row + point[0]][col + point[1]] = "O"
        return Image(["".join(line) for line in list_data])

    def find_mask_in_image(self, mask):
        nrows = self.shape[0] - mask.shape[0]
        ncols = self.shape[1] - mask.shape[1]
        points = []
        for row in range(nrows):
            for col in range(ncols):
                subimage = self.extract_subimage((row, col), mask.shape)
                if subimage.check_mask_in_image(mask):
                    points.append(Point(row, col))
        return points

    def extract_subimage(self, position, shape):
        return Image(
            [
                line[position[1] : position[1] + shape[1]]
                for line in self.data[position[0] : position[0] + shape[0]]
            ]
        )

    def __eq__(self, other):
        if self.shape == other.shape:
            return all(s == o for s, o in zip(self.data, other.data))
        return False

    @classmethod
    def from_tiles(cls, tiles):
        tile_data_without_borders = []
        for row in tiles:
            tile_data_without_borders.append([])
            for tile in row:
                tile_data_without_borders[-1].append(tile.get_data_without_borders())
        data = []
        for tile_row in tile_data_without_borders:
            for all_rows in zip(*tile_row):
                data.append("".join(all_rows))
        return Image(data)


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

    def get_data_without_borders(self):
        return [line[1:-1] for line in self.data[1:-1]]


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
    yield from generate_rotations(tile)
    tile = tile.flip_horizontal()
    yield from generate_rotations(tile)


def generate_rotations(tile):
    for _ in range(4):
        yield (tile := tile.rotate_right())


def convert_tile_dict_to_tile_list(tile_dict):
    rows, cols = [p.row for p in tile_dict], [p.col for p in tile_dict]
    minrow, maxrow = min(rows), max(rows)
    mincol, maxcol = min(cols), max(cols)
    list_image = []
    for row in range(minrow, maxrow + 1):
        list_image.append([])
        for col in range(mincol, maxcol + 1):
            list_image[-1].append(tile_dict[Point(row, col)])
    return list_image


if __name__ == "__main__":
    tiles = read_tiles(argv[-1])
    list_image = convert_tile_dict_to_tile_list(assemble_image_from_tiles(tiles))

    # part 1
    corner_tile_ids = [
        list_image[row][col].id_ for row, col in product([0, -1], [0, -1])
    ]
    print(reduce(lambda id1, id2: id1 * id2, corner_tile_ids))

    # part 2
    image = Image.from_tiles(list_image)
    with open("sea_monster.txt") as stream:
        sea_monster = Image(stream.read().strip("\n").split("\n"))
    for orientation in generate_orientations(image):
        if (points := orientation.find_mask_in_image(sea_monster)) :
            image = orientation
            break
    # print(points)
    masked_image = image.apply_mask_to_points(points, sea_monster)
    print(sum(line.count("#") for line in masked_image.data))
