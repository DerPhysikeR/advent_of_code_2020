from sys import argv


def read_jolt_ratings(filename):
    with open(filename) as stream:
        return [int(n) for n in stream.read().strip().split("\n")]


if __name__ == "__main__":
    # part 1
    jolt_ratings = read_jolt_ratings(argv[-1])
    jolt_ratings = [0] + sorted(jolt_ratings) + [max(jolt_ratings) + 3]
    differences = [
        jolt_ratings[i + 1] - jolt_ratings[i] for i in range(len(jolt_ratings) - 1)
    ]
    print(differences)
    diff1, diff3 = differences.count(1), differences.count(3)
    print(
        f"There are {diff1} differences of 1 jolt and {diff3} differences of 3 jolts."
    )
    print(f"Their product is {diff1 * diff3}")

    # part 2
    groups_of_ones = []
    count = 0
    for i in differences:
        if i == 1:
            count += 1
        if i == 3:
            if count > 0:
                groups_of_ones.append(count)
            count = 0
    print(groups_of_ones)

    num_possibilities = 1
    possible_variations = {1: 1, 2: 2, 3: 4, 4: 7}
    for g in groups_of_ones:
        num_possibilities *= possible_variations[g]
    print(num_possibilities)

    # 0 - 3 - 4 - 7
    #   3   1   3
    # only one possibility, no variation possible

    # 0 - 3 - 4 - 5 - 8
    #   3   1   1   3
    # two possibilities
    # 0 - 3 - 5 - 8
    # 0 - 3 - 4 - 5 - 8

    # 0 - 3 - 4 - 5 - 6 - 9
    #   3   1   1   1   3
    # four possibilities
    # 0 - 3 - 6 - 9
    # 0 - 3 - 4 - 6 - 9
    # 0 - 3 - 5 - 6 - 9
    # 0 - 3 - 4 - 5 - 6 - 9

    # 0 - 3 - 4 - 5 - 6 - 7 - 10
    #   3   1   1   1   1   3
    # seven posibilities
    # 0 - 3 - 4 - 7 - 10
    # 0 - 3 - 5 - 7 - 10
    # 0 - 3 - 6 - 7 - 10
    # 0 - 3 - 4 - 5 - 7 - 10
    # 0 - 3 - 4 - 6 - 7 - 10
    # 0 - 3 - 5 - 6 - 7 - 10
    # 0 - 3 - 4 - 5 - 6 - 7 - 10
