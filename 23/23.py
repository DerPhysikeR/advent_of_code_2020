from collections import deque
from sys import argv


def read_cups(filename):
    with open(filename) as stream:
        return [int(n) for n in list(stream.read().strip())]


def wrap_range(interval, num, step):
    """
    >>> list(wrap_range((1, 3), 2, -1))
    [2, 1, 3]
    """
    min_, max_ = interval
    for _ in range(max_ - min_ + 1):
        yield num
        num += step
        if num > max_:
            num = min_
        elif num < min_:
            num = max_


def evolve_cups(cups):
    cup_range = min(cups), max(cups)
    cups = deque(cups)
    while True:
        # take 3
        yield cups
        cups.append(cups.popleft())
        taken_cups = [cups.popleft() for _ in range(3)]
        cups.appendleft(cups.pop())
        # find destination cup
        for label in wrap_range(cup_range, cups[0] - 1, -1):
            try:
                destination_idx = cups.index(label)
                destination = cups[destination_idx]
                break
            except ValueError:
                pass
        # insert taken cups after destination
        for _ in range(destination_idx + 1):
            cups.append(cups.popleft())
        for _ in range(len(taken_cups)):
            cups.appendleft(taken_cups.pop())
        for _ in range(destination_idx + 1):
            cups.appendleft(cups.pop())
        # select new current cup
        cups.append(cups.popleft())


if __name__ == "__main__":
    cups = read_cups(argv[-1])
    for i, cups in enumerate(evolve_cups(cups)):
        print(cups)
        if i >= 100:
            break
    for _ in range(cups.index(1)):
        cups.append(cups.popleft())
    cups.popleft()
    print(list(cups))
