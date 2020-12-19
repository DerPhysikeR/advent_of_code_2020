from itertools import product
from sys import argv


def read_rules_and_messages(filename):
    with open(filename) as stream:
        rules_string, messages_string = stream.read().strip().split("\n\n")
        return rules_string.split("\n"), messages_string.split("\n")


class RuleChecker:
    def __init__(self, rule_strings):
        self.rule_dict = {
            int((r := rs.partition(": "))[0]): self.rule_checker_factory(r[2])
            for rs in rule_strings
        }

    def rule_checker_factory(self, rule_string):
        if '"' in rule_string:

            def rule_checker(message, idx):
                if idx >= len(message):
                    return False, idx
                if message[idx] == rule_string[1]:
                    return True, idx + 1
                return False, idx

            return rule_checker
        if "|" in rule_string:
            checkers = [
                self._check_multiple_rules(rp) for rp in rule_string.split(" | ")
            ]

            def rule_checker(message, original_idx):
                for checker in checkers:
                    result, idx = checker(message, original_idx)
                    if result:
                        return True, idx
                return False, original_idx

            return rule_checker
        return self._check_multiple_rules(rule_string)

    def _check_multiple_rules(self, rule_string):
        rule_idxs = [int(r) for r in rule_string.split(" ")]

        def rule_checker(message, idx):
            for rule_idx in rule_idxs:
                result, idx = self.rule_dict[rule_idx](message, idx)
                if not result:
                    return False, idx
            return True, idx

        return rule_checker

    def check_message_with_rule_0(self, message):
        result, idx = self.rule_dict[0](message, 0)
        if idx < len(message):
            return False
        return result


class LoopyRuleChecker(RuleChecker):
    def _update_rule(self, num, rule_string):
        self.rule_dict[num] = self.rule_checker_factory(rule_string)

    def check_message_with_rule_0(self, message):
        for eight, eleven in rule_generator(10):
            self._update_rule(8, eight)
            self._update_rule(11, eleven)
            if super().check_message_with_rule_0(message):
                return True
        return False


def rule_generator(num):
    eight_rule = [" ".join(["42"] * i) for i in range(1, num + 1)]
    eleventh_rule = [" ".join(["42"] * i + ["31"] * i) for i in range(1, num + 1)]
    yield from product(eight_rule, eleventh_rule)


def run(rule_checker, messages):
    num_matching_messages = 0
    for message in messages:
        if rule_checker.check_message_with_rule_0(message):
            print(f"✓ {message}")
            num_matching_messages += 1
        else:
            print(f"x {message}")
    print(num_matching_messages)


if __name__ == "__main__":
    rules, messages = read_rules_and_messages(argv[-1])
    print("Part 1:")
    run(RuleChecker(rules), messages)
    print()
    print("Part 2:")
    run(LoopyRuleChecker(rules), messages)

    # 4 1 5
    # "a" (2 3 | 3 2) "b"
    # "a" (("a" "a" | "b" "b") ("a" "b" | "b" "a") | ("a" "b" | "b" "a") ("a" "a" | "b" "b")) "b"
    # "a" (("aa" | "bb") ("ab" | "ba") | ("ab" | "ba") ("aa" | "bb")) "b"
    # a aa ab b b
