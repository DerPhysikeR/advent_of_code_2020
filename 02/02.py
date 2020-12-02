def parse_line(line):
    count_interval, letter, password = line.split()
    count_interval = (int(c) for c in count_interval.split("-"))
    return count_interval, letter[0], password


def is_password_valid(line):
    (min_, max_), letter, password = parse_line(line)
    return min_ <= password.count(letter) <= max_


def is_password_actually_valid(line):
    (pos1, pos2), letter, password = parse_line(line)
    return (password[pos1 - 1] == letter) ^ (password[pos2 - 1] == letter)


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        puzzle_input = stream.read().strip().split("\n")

    # part 1
    num_valid_passwords = 0
    for line in puzzle_input:
        if is_password_valid(line):
            num_valid_passwords += 1

    print(f"The number of valid passwords is: {num_valid_passwords}")

    # part 2
    num_valid_passwords = 0
    for line in puzzle_input:
        if is_password_actually_valid(line):
            num_valid_passwords += 1

    print(f"The number of actual valid passwords is: {num_valid_passwords}")
