from itertools import islice, count, repeat
import pytest


def rambunctious_recitation(starting_numbers):
    """
    >>> gen = rambunctious_recitation([0, 3, 6])
    >>> list(islice(gen, 24))
    [0, 3, 6, 0, 3, 3, 1, 0, 4, 0, 2, 0, 2, 2, 1, 8, 0, 5, 0, 2, 6, 18, 0, 4]
    >>> gen = rambunctious_recitation([0, 3, 6])
    >>> next(islice(gen, 2019, 2020))
    436
    """
    last_appearance_dict = {n: i for i, n in enumerate(starting_numbers[:-1])}
    yield from starting_numbers
    last_number_spoken = starting_numbers[-1]
    for i in count(len(starting_numbers)):
        if last_number_spoken in last_appearance_dict:
            n = i - last_appearance_dict[last_number_spoken] - 1
            yield n
            last_appearance_dict[last_number_spoken] = i - 1
            last_number_spoken = n
        else:
            yield 0
            last_appearance_dict[last_number_spoken] = i - 1
            last_number_spoken = 0


@pytest.mark.parametrize(
    "starting_numbers, number",
    [
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    ],
)
def test_rambunctious_recitation(starting_numbers, number):
    gen = rambunctious_recitation(starting_numbers)
    assert next(islice(gen, 2019, 2020)) == number


if __name__ == "__main__":
    puzzle_input = [1, 12, 0, 20, 8, 16]

    # part 1
    gen = rambunctious_recitation(puzzle_input)
    print(next(islice(gen, 2019, 2020)))

    # part 2
    gen = rambunctious_recitation(puzzle_input)
    print(next(islice(gen, 29999999, 30000000)))
