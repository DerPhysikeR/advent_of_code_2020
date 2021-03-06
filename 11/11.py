from itertools import product
from sys import argv


def read_seat_layout(filename):
    with open(filename) as stream:
        return [list(line) for line in stream.read().strip().split("\n")]


def count_occupied_neighbors(seat_layout, row, col):
    """
    >>> count_occupied_neighbors([list("###"), list("###"), list("###")], 1, 1)
    8
    >>> count_occupied_neighbors([list("#.#"), list("#L#"), list("#.#")], 1, 1)
    6
    """
    n_rows, n_cols = len(seat_layout), len(seat_layout[0])
    sum_ = 0
    for r in [row - 1, row, row + 1]:
        if r < 0 or r >= n_rows:
            continue
        for c in [col - 1, col, col + 1]:
            if c < 0 or c >= n_cols:
                continue
            if r == row and c == col:
                continue
            if seat_layout[r][c] == "#":
                sum_ += 1
    return sum_


def evolve_seat_layout(
    seat_layout, counting_function=count_occupied_neighbors, emptying_threshold=4
):
    result = []
    for row, line in enumerate(seat_layout):
        result.append([])
        for col, letter in enumerate(line):
            if letter == ".":
                result[-1].append(".")
                continue
            on = counting_function(seat_layout, row, col)
            if letter == "L" and on == 0:
                result[-1].append("#")
            elif letter == "#" and on >= emptying_threshold:
                result[-1].append("L")
            else:
                result[-1].append(letter)
    return result


def count_visibly_occupied_neighbors(seat_layout, row, col):
    n_rows, n_cols = len(seat_layout), len(seat_layout[0])
    sum_ = 0
    for drow, dcol in product([-1, 0, 1], [-1, 0, 1]):
        if drow == dcol == 0:
            continue
        r, c = row + drow, col + dcol
        while 0 <= r < n_rows and 0 <= c < n_cols:
            if seat_layout[r][c] == "L":
                break
            if seat_layout[r][c] == "#":
                sum_ += 1
                break
            r, c = r + drow, c + dcol
    return sum_


def evolve_seat_layout_by_visibility(seat_layout):
    return evolve_seat_layout(seat_layout, count_visibly_occupied_neighbors, 5)


def to_string(seat_layout):
    return "\n".join("".join(row) for row in seat_layout)


def print_evolution(seat_layout, evolution_function):
    previous_string_layout = ""
    while previous_string_layout != (sl := to_string(seat_layout)):
        print(sl)
        print()
        previous_string_layout = sl
        seat_layout = evolution_function(seat_layout)
    return seat_layout


if __name__ == "__main__":
    original_seat_layout = read_seat_layout(argv[-1])

    # part 1
    seat_layout = print_evolution(original_seat_layout, evolve_seat_layout)
    print(
        f"The final seat layout has {sum(r.count('#') for r in seat_layout)} occupied seats."
    )

    breakpoint()

    # part 2
    seat_layout = print_evolution(
        original_seat_layout, evolve_seat_layout_by_visibility
    )
    print(
        f"The final seat layout has {sum(r.count('#') for r in seat_layout)} occupied seats."
    )
