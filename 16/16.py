from sys import argv
from copy import deepcopy


def parse_ticket(ticket_string):
    return [int(i) for i in ticket_string.split(",")]


def rule_checker_factory(*ranges):
    def rule_checker(number):
        for range_ in ranges:
            if range_[0] <= number <= range_[1]:
                return True
        return False

    return rule_checker


def parse_ticket_rules(rule_description):
    ticket_rules = {}
    for line in rule_description.split("\n"):
        key, _, ranges_string = line.partition(": ")
        ranges = [
            tuple(int(i) for i in string_ranges.split("-"))
            for string_ranges in ranges_string.split(" or ")
        ]
        ticket_rules[key] = rule_checker_factory(*ranges)
    return ticket_rules


def read_ticket_information(filename):
    with open(filename) as stream:
        content = stream.read().strip().split("\n\n")
        ticket_rules = parse_ticket_rules(content[0])
        your_ticket = parse_ticket(content[1].partition("\n")[2])
        nearby_tickets = [parse_ticket(ticket) for ticket in content[2].split("\n")[1:]]
    return ticket_rules, your_ticket, nearby_tickets


def find_valid_tickets_and_scanning_error_rate(tickets_to_check, ticket_rules):
    valid_tickets, error_rate = [], 0
    for ticket in tickets_to_check:
        for number in ticket:
            for rule in ticket_rules.values():
                if rule(number):
                    break
            else:
                error_rate += number
                break
        else:
            valid_tickets.append(ticket)
    return valid_tickets, error_rate


def find_possible_field_names_for_every_field(tickets, ticket_rules):
    possible_field_names_for_every_field = []
    for field_num in range(len(tickets[0])):
        possible_field_names = set()
        for field_name, ticket_rule in ticket_rules.items():
            if all(ticket_rule(ticket[field_num]) for ticket in tickets):
                possible_field_names.add(field_name)
        possible_field_names_for_every_field.append(possible_field_names)
    return possible_field_names_for_every_field


def identify_field_names_uniquely(possible_field_names):
    possible_field_names = deepcopy(possible_field_names)
    previous_num_field_names = sum(len(fn) for fn in possible_field_names) + 1
    while sum(len(fn) for fn in possible_field_names) < previous_num_field_names:
        previous_num_field_names = sum(len(fn) for fn in possible_field_names)
        for i, field_names in enumerate(possible_field_names):
            if len(field_names) == 1:
                for j, _ in enumerate(possible_field_names):
                    if i != j:
                        possible_field_names[j] = possible_field_names[j].difference(
                            field_names
                        )
    if any(len(pfn) != 1 for pfn in possible_field_names):
        raise ValueError("Field names can't be identified uniquely!")
    return [pfn.pop() for pfn in possible_field_names]


if __name__ == "__main__":
    # part 1
    ticket_rules, your_ticket, nearby_tickets = read_ticket_information(argv[-1])
    valid_tickets, scanning_error_rate = find_valid_tickets_and_scanning_error_rate(
        nearby_tickets, ticket_rules
    )
    print(scanning_error_rate)

    # part 2
    possible_field_names_for_every_field = find_possible_field_names_for_every_field(
        valid_tickets, ticket_rules
    )
    # print(possible_field_names_for_every_field)
    unique_field_names = identify_field_names_uniquely(
        possible_field_names_for_every_field
    )
    # print(unique_field_names)
    product = 1
    for ufn, yt in zip(unique_field_names, your_ticket):
        if ufn.startswith("departure"):
            product *= yt
    print(product)
