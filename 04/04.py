import re
from sys import argv

REQUIRED_FIELDS = set(
    [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid",
    ]
)


def convert_passport_string_to_dict(passport_string):
    entries = re.split(" |\n", passport_string)
    return {(content := entry.partition(":"))[0]: content[2] for entry in entries}


def read_passports(filename):
    with open(filename, "r") as stream:
        return [
            convert_passport_string_to_dict(passport)
            for passport in stream.read().strip().split("\n\n")
        ]


def is_passport_valid(passport):
    return len(REQUIRED_FIELDS.difference(passport.keys())) == 0


if __name__ == "__main__":
    passports = read_passports(argv[-1])
    num_valid_passports = sum(is_passport_valid(p) for p in passports)
    print(f"Of the given {len(passports)} passports, {num_valid_passports} are valid.")
