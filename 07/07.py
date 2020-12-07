from sys import argv


def read_bag_rules(filename):
    with open(filename) as stream:
        return {
            (p := parse_rule_line(line))[0]: p[1]
            for line in stream.read().strip().split("\n")
        }


def parse_rule_line(rule_string):
    """
    >>> parse_rule_line("light red bags contain 1 bright white bag, 2 muted yellow bags.")
    ('light red', {'bright white': 1, 'muted yellow': 2})
    >>> parse_rule_line("dark orange bags contain 3 bright white bags, 4 muted yellow bags.")
    ('dark orange', {'bright white': 3, 'muted yellow': 4})
    >>> parse_rule_line("faded blue bags contain no other bags.")
    ('faded blue', {})
    """
    outer_bag_color, _, inner_bag_rules = rule_string[:-1].partition(" bags contain ")
    if inner_bag_rules == "no other bags":
        return outer_bag_color, {}
    return outer_bag_color, {
        (p := parse_rule(rule))[0]: p[1] for rule in inner_bag_rules.split(", ")
    }


def parse_rule(rule_string):
    """
    >>> parse_rule('1 bright white bag')
    ('bright white', 1)
    >>> parse_rule('3 bright white bags')
    ('bright white', 3)
    """
    count, _, color_bags = rule_string.partition(" ")
    return color_bags.rpartition(" bag")[0], int(count)


def check_colors_containing_color(bag_rules, color):
    num_colors_before, colors = -1, set()
    while num_colors_before < len(colors):
        num_colors_before = len(colors)
        for bag_color, contained_colors in bag_rules.items():
            if (
                color in contained_colors
                or len(colors.intersection(contained_colors)) > 0
            ):
                colors.add(bag_color)
    return colors


def count_number_of_bags_in_outer_bag(bag_rules, outer_bag_color):
    return sum(
        count + count * count_number_of_bags_in_outer_bag(bag_rules, inner_bag_color)
        for inner_bag_color, count in bag_rules[outer_bag_color].items()
    )


if __name__ == "__main__":
    rules = read_bag_rules(argv[-1])

    # part 1
    colors = check_colors_containing_color(rules, "shiny gold")
    print(
        f"The number of bag colors which can contain at least one shiny gold bag are {len(colors)}."
    )

    # part 2
    bag_count = count_number_of_bags_in_outer_bag(rules, "shiny gold")
    print(f"The number of bags necessary inside a shiny gold bag are {bag_count}.")
