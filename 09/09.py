from itertools import permutations
from sys import argv


def read_numbers(filename):
    with open(filename) as stream:
        return [int(num) for num in stream.read().strip().split("\n")]


def find_first_invalid_number_in_xmas_encoding(numbers, preamble_length):
    for i, number in enumerate(numbers[preamble_length:], preamble_length):
        slice_ = numbers[i - preamble_length : i]
        if number in (sum(p) for p in permutations(slice_, 2)):
            continue
        return number


def find_contiguous_range_summing_to(numbers, expected_sum):
    """
    >>> find_contiguous_range_summing_to([1, 10, 100, 1000], 1100)
    (2, 4)
    >>> find_contiguous_range_summing_to([1, 10, 100, 1000], 1110)
    (1, 4)
    >>> find_contiguous_range_summing_to([1, 10, 100, 1000], 1111)
    (0, 4)
    """
    summed_numbers = numbers[:]
    for offset in range(1, len(numbers)):
        for i in range(offset, len(numbers)):
            summed_numbers[i] += numbers[i - offset]
            if summed_numbers[i] == expected_sum:
                return i - offset, i + 1


if __name__ == "__main__":
    # part 1 `python 09.py input.txt 25`
    numbers = read_numbers(argv[-2])
    first_invalid_number = find_first_invalid_number_in_xmas_encoding(
        numbers, int(argv[-1])
    )
    print(first_invalid_number)

    # part 2
    range_ = find_contiguous_range_summing_to(numbers, first_invalid_number)
    contiguous_set = [numbers[i] for i in range(*range_)]
    print(sum(contiguous_set))
    print(f"The range ist range{range_}.")
    print(f"The sum of min and max is {min(contiguous_set) + max(contiguous_set)}.")
