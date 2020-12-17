from sys import argv
from collections import namedtuple, defaultdict

Cube = namedtuple("Cube", "x, y, z")


def read_puzzle_input(filename):
    with open(filename) as stream:
        active_cubes = set()
        for row, line in enumerate(stream.read().strip().split("\n")):
            for col, letter in enumerate(line):
                if letter == "#":
                    active_cubes.add(Cube(row, col, 0))
        return active_cubes


def generate_neighbors(cube):
    for x in range(cube.x - 1, cube.x + 2):
        for y in range(cube.y - 1, cube.y + 2):
            for z in range(cube.z - 1, cube.z + 2):
                if (new_cube := Cube(x, y, z)) != cube:
                    yield new_cube


def evolve_cubes(active_cubes):
    new_active_cubes = set()
    empty_neighbor_count = defaultdict(int)
    for cube in active_cubes:
        active_neighbor_count = 0
        for neighbor in generate_neighbors(cube):
            if neighbor in active_cubes:
                active_neighbor_count += 1
            else:
                empty_neighbor_count[neighbor] += 1
        if 2 <= active_neighbor_count <= 3:
            new_active_cubes.add(cube)
    for cube, count in empty_neighbor_count.items():
        if count == 3:
            new_active_cubes.add(cube)
    return new_active_cubes


def print_cubes(cubes):
    xx, yy, zz = [c.x for c in cubes], [c.y for c in cubes], [c.z for c in cubes]
    for z in range(min(zz), max(zz) + 1):
        print(f"z={z}")
        for x in range(min(xx), max(xx) + 1):
            line = []
            for y in range(min(yy), max(yy) + 1):
                if Cube(x, y, z) in cubes:
                    line.append("#")
                else:
                    line.append(".")
            print("".join(line))
        print()


if __name__ == "__main__":
    active_cubes = read_puzzle_input(argv[-1])
    print("Before any cycles:")
    print_cubes(active_cubes)
    for i in range(6):
        active_cubes = evolve_cubes(active_cubes)
        print(f"After {i+1} cycles:")
        print_cubes(active_cubes)
    print(len(active_cubes))
