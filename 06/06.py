from sys import argv


def read_group_answers(filename):
    with open(filename) as stream:
        answers = stream.read().strip().split("\n\n")
        return [group.split("\n") for group in answers]


if __name__ == "__main__":
    answers = read_group_answers(argv[-1])

    # part 1
    answered_yes_sum = 0
    for group in answers:
        answered_yes = set.union(*[set(individual) for individual in group])
        answered_yes_sum += len(answered_yes)
    print(
        f"The sum of all the questions that were answerered `yes`"
        f"by anyone in a group is: {answered_yes_sum}"
    )

    # part 2
    answered_yes_sum = 0
    for group in answers:
        answered_yes = set.intersection(*[set(individual) for individual in group])
        answered_yes_sum += len(answered_yes)
    print(
        f"The sum of all the questions that were answerered `yes` "
        f"by everyone in a group is: {answered_yes_sum}"
    )
