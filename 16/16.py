from sys import argv


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


def calc_ticket_scanning_error_rate(tickets_to_check, ticket_rules):
    error_rate = 0
    for ticket in tickets_to_check:
        for number in ticket:
            for rule in ticket_rules.values():
                if rule(number):
                    break
            else:
                error_rate += number
    return error_rate


if __name__ == "__main__":
    ticket_rules, your_ticket, nearby_tickets = read_ticket_information(argv[-1])
    print(calc_ticket_scanning_error_rate(nearby_tickets, ticket_rules))
