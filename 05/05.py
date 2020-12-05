from sys import argv


def read_boarding_passes(filename):
    with open(filename) as stream:
        return stream.read().strip().split("\n")


def calc_seat_id(row, col):
    """
    >>> calc_seat_id(44, 5)
    357
    """
    return row * 8 + col


def to_binary_string(string, encoding):
    """
    >>> to_binary_string("BFFF", "FB")
    '1000'
    """
    assert len(set(string).difference(set(encoding))) == 0
    zero, one = encoding
    return string.replace(zero, "0").replace(one, "1")


def find_boarding_pass_row_col(boarding_pass):
    """
    >>> find_boarding_pass_row_col("BFFFBBFRRR")
    (70, 7)
    >>> find_boarding_pass_row_col("FFFBBBFRRR")
    (14, 7)
    >>> find_boarding_pass_row_col("BBFFBBFRLL")
    (102, 4)
    """
    row_part, col_part = boarding_pass[:-3], boarding_pass[-3:]
    return (
        int(to_binary_string(row_part, "FB"), 2),
        int(to_binary_string(col_part, "LR"), 2),
    )


if __name__ == "__main__":
    # part 1
    boarding_passes = read_boarding_passes(argv[-1])
    seat_ids = [calc_seat_id(*find_boarding_pass_row_col(bp)) for bp in boarding_passes]
    print(f"The highest seat ID is: {max(seat_ids)}")

    # # part 2
    seat_ids = sorted(seat_ids)
    for i, seat_id in enumerate(seat_ids[1:-1], 1):
        if seat_ids[i - 1] == seat_id - 1 and seat_ids[i + 1] == seat_id + 1:
            continue
        print(seat_id)
