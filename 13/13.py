from sys import argv


def read_puzzle_input(filename):
    with open(filename) as stream:
        earliest_departure = int(stream.readline().strip())
        bus_schedule = [
            item if item == "x" else int(item)
            for item in stream.readline().strip().split(",")
        ]
        return earliest_departure, bus_schedule


def find_waiting_times(earliest_departure, bus_schedule):
    waiting_times = {}
    for bus in bus_schedule:
        if bus == "x":
            continue
        cycle_times = earliest_departure // bus
        if cycle_times * bus == earliest_departure:
            waiting_times[bus] = 0
            continue
        waiting_times[bus] = (cycle_times + 1) * bus - earliest_departure
    return waiting_times


def find_offset_product(a, b, offset=1, start=1, step=1):
    """
    >>> (find_offset_product(3, 7) + 1) % 7
    0
    >>> (find_offset_product(3, 7, 1, 2, 7) + 1) % 7
    0
    >>> (find_offset_product(1789, 37) + 1) % 37
    0
    >>> (find_offset_product(1005, 1001) + 1) % 1001
    0
    >>> (find_offset_product(1005, 1001, 2) + 2) % 1001
    0
    >>> (find_offset_product(1005, 1001, 3) + 3) % 1001
    0
    >>> find_offset_product(1005, 1002, 1)
    """
    for i in range(b):
        if (((start + i * step) * a) + offset) % b == 0:
            return (start + i * step) * a
    return None


def find_earliest_continuous_departure(bus_schedule):
    """
    >>> find_earliest_continuous_departure([3, 7, 5, 2])
    153
    >>> find_earliest_continuous_departure([17, "x", 13, 19])
    3417
    >>> find_earliest_continuous_departure([67, 7, 59, 61])
    754018
    >>> find_earliest_continuous_departure([67, "x", 7, 59, 61])
    779210
    >>> find_earliest_continuous_departure([67, 7, "x", 59, 61])
    1261476
    >>> find_earliest_continuous_departure([1789, 37, 47, 1889])
    1202161486
    """
    start, step = 1, 1
    for i, bus in enumerate(bus_schedule[1:], 1):
        if bus == "x":
            continue
        result = find_offset_product(bus_schedule[0], bus, i, start, step)
        step *= bus
        start = result // bus_schedule[0]
    return result


if __name__ == "__main__":
    earliest_departure, bus_schedule = read_puzzle_input(argv[-1])

    # part 1
    bus_waiting_times = find_waiting_times(earliest_departure, bus_schedule)
    earliest_bus = min(bus_waiting_times, key=bus_waiting_times.get)
    shortest_waiting_time = bus_waiting_times[earliest_bus]
    print(
        f"The earliest bus is {earliest_bus} with a waiting time of {shortest_waiting_time}."
    )
    print(
        f"The product of bus ID and waiting time is {earliest_bus * shortest_waiting_time}."
    )

    # part 2
    print(find_earliest_continuous_departure(bus_schedule))
