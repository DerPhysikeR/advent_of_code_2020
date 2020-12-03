from sys import argv


def read_tree_pattern(file_):
    with open(file_, "r") as stream:
        return stream.read().strip().split("\n")


def walk_tree_pattern(tree_pattern, direction):
    d_col, d_row = direction
    tree_count = 0
    row, col = 0, 0
    while row < len(tree_pattern):
        if tree_pattern[row][col % len(tree_pattern[0])] == "#":
            tree_count += 1
        row, col = row + d_row, col + d_col
    return tree_count


if __name__ == "__main__":
    tree_pattern = read_tree_pattern(argv[-1])
    print(walk_tree_pattern(tree_pattern, (3, 1)))
    print(
        walk_tree_pattern(tree_pattern, (1, 1))
        * walk_tree_pattern(tree_pattern, (3, 1))
        * walk_tree_pattern(tree_pattern, (5, 1))
        * walk_tree_pattern(tree_pattern, (7, 1))
        * walk_tree_pattern(tree_pattern, (1, 2))
    )
