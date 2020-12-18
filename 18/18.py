from sys import argv
from functools import reduce
from collections import deque


def read_expressions(filename):
    with open(filename) as stream:
        return stream.read().strip().split("\n")


def find_matching_paren_idx(expression):
    """
    >>> find_matching_paren_idx("(1 + 2)")
    6
    >>> find_matching_paren_idx("((1 + 2))")
    8
    >>> find_matching_paren_idx("(1 + 2) * (3 * 4)")
    6
    >>> find_matching_paren_idx("((1 + 2) * (3 * 4))")
    18
    """
    count = 0
    for i, letter in enumerate(expression):
        if letter == "(":
            count += 1
        elif letter == ")":
            count -= 1
        if count == 0:
            return i
    raise ValueError(f"Invalid Expression `{expression}`.")


def evaluate_expression(expression):
    """
    >>> evaluate_expression("1 * 2 + 3")
    5
    >>> evaluate_expression("(1 * 2 + 3)")
    5
    >>> evaluate_expression("((1 * 2) + 3)")
    5
    """
    if not "(" in expression:
        if "+" not in expression:
            return int(reduce(lambda x, y: int(x) * int(y), expression.split(" ")[::2]))
        before, _, after = expression.partition(" + ")
        before, _, num1 = before.rpartition(" ")
        num2, _, after = after.partition(" ")
        return evaluate_expression(
            f"{before.strip()} {int(num1) + int(num2)} {after.strip()}".strip()
        )
    opening_paren_idx = expression.index("(")
    closing_paren_idx = (
        find_matching_paren_idx(expression[opening_paren_idx:]) + opening_paren_idx
    )
    before = expression[:opening_paren_idx].strip()
    evaluated_expression = evaluate_expression(
        expression[opening_paren_idx + 1 : closing_paren_idx]
    )
    after = (
        ""
        if closing_paren_idx >= len(expression)
        else expression[closing_paren_idx + 1 :]
    ).strip()
    return evaluate_expression(f"{before} {evaluated_expression} {after}".strip())


if __name__ == "__main__":
    expressions = read_expressions(argv[-1])
    results = [evaluate_expression(e) for e in expressions]
    print(results)
    print(sum(results))
