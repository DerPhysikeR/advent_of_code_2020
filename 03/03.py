from sys import argv


def read_tree_pattern(file_):
    with open(file_, "r") as stream:
        return stream.read().strip().split("\n")


if __name__ == "__main__":
    tree_pattern = read_tree_pattern(argv[-1])
    d_row, d_col = 1, 3
    tree_count = 0
    row, col = 0, 0
    while row < len(tree_pattern):
        if tree_pattern[row][col % len(tree_pattern[0])] == "#":
            tree_count += 1
        row, col = row + d_row, col + d_col
    print(tree_count)
