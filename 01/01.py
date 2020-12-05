from itertools import product


with open("input.txt", "r") as stream:
    puzzle_input = [int(line) for line in stream.read().strip().split("\n")]


# part 1
puzzle_input = sorted(puzzle_input)

i, j = 0, len(puzzle_input) - 1
while i < j:
    sum_ = puzzle_input[i] + puzzle_input[j]
    if sum_ < 2020:
        i += 1
    elif sum_ > 2020:
        j -= 1
    else:
        a, b = puzzle_input[i], puzzle_input[j]
        print(f"The two numbers are {a} and {b}")
        print(f"Their sum is: {sum_}")
        print(f"and their product is: {a * b}")
        break

# part 2
for a, b, c in product(puzzle_input, puzzle_input, puzzle_input):
    if a + b + c == 2020:
        print(f"The three numbers are {a}, {b} and {c}")
        print(f"Their sum is: {a + b + c}")
        print(f"and their product is: {a * b * c}")
