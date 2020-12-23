from itertools import chain
from sys import argv


def read_cups(filename):
    with open(filename) as stream:
        return [int(n) for n in list(stream.read().strip())]


class Node:
    def __init__(self, value, after=None, lower=None):
        self.value = value
        self.after = after  # previous -> after
        self.lower = lower  # lower -> higher

    def __repr__(self):
        after = None if self.after is None else self.after.value
        lower = None if self.lower is None else self.lower.value
        return f"Node({self.value}, after={after}, lower={lower})"


def linked_list_to_list(start_node):
    """
    >>> linked_list_to_list(Node(5))
    [Node(5, after=None, lower=None)]
    >>> node = Node(5)
    >>> node.after = Node(7)
    >>> linked_list_to_list(node)
    [Node(5, after=7, lower=None), Node(7, after=None, lower=None)]
    """
    result = [start_node]
    node = start_node
    while node.after is not start_node and node.after is not None:
        result.append(node.after)
        node = node.after
    return result


def initialize_linked_list(beginning_cups, fill_to_value):
    """
    >>> node = initialize_linked_list([3, 2, 1], 5)
    >>> linked_list_to_list(node)
    [Node(3, after=2, lower=2), Node(2, after=1, lower=1), Node(1, after=4, lower=5), Node(4, after=5, lower=3), Node(5, after=3, lower=4)]
    """
    nodes = {
        value: Node(value)
        for value in chain(
            beginning_cups, range(max(beginning_cups) + 1, fill_to_value + 1)
        )
    }
    last_value = (
        fill_to_value if fill_to_value > max(beginning_cups) else beginning_cups[-1]
    )
    previous_node = nodes[last_value]
    for value, node in nodes.items():
        previous_node.after = node
        v = value - 1 if value > 1 else fill_to_value
        node.lower = nodes[v]
        previous_node = node
    return nodes[beginning_cups[0]]


def evolve_linked_list(current_node):
    # find next 3 nodes
    node = current_node
    next_three_nodes = [(node := node.after) for _ in range(3)]
    three_values_after = set([n.value for n in next_three_nodes])
    # find destination
    destination = current_node.lower
    while destination.value in three_values_after:
        destination = destination.lower
    # insert three nodes after destination
    current_node.after = next_three_nodes[-1].after
    next_three_nodes[-1].after = destination.after
    destination.after = next_three_nodes[0]
    # return new current node
    return current_node.after


def get_values_of_linked_list(linked_list):
    return [n.value for n in linked_list_to_list(linked_list)]


if __name__ == "__main__":
    original_cups = read_cups(argv[-1])

    # part 1
    linked_list = initialize_linked_list(original_cups, 9)
    print(get_values_of_linked_list(linked_list))
    for _ in range(100):
        linked_list = evolve_linked_list(linked_list)
        print(get_values_of_linked_list(linked_list))
    # find node number 1 and print from there
    node = linked_list
    while node.value != 1:
        node = node.after
    print("".join(str(n) for n in get_values_of_linked_list(node)[1:]))
