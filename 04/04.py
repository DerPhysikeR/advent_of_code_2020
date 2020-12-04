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


def match_height(height_string):
    """
    >>> match_height("149")
    False
    >>> match_height("150cm")
    True
    >>> match_height("193cm")
    True
    >>> match_height("194cm")
    False
    >>> match_height("58in")
    False
    >>> match_height("59in")
    True
    >>> match_height("76in")
    True
    >>> match_height("77in")
    False
    """
    value, unit = int(height_string[:-2]), height_string[-2:]
    if unit == "cm":
        return 150 <= value <= 193
    if unit == "in":
        return 59 <= value <= 76
    return False


CHECK_FUNCTIONS = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": match_height,
    "hcl": lambda x: bool(re.match(r"^#[0-9a-f]{6}$", x)),
    "ecl": lambda x: x in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]),
    "pid": lambda x: bool(re.match(r"^\d{9}$", x)),
    "cid": lambda x: True,
}


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


def is_passport_really_valid(passport):
    if not is_passport_valid(passport):
        return False
    for field, entry in passport.items():
        if not CHECK_FUNCTIONS[field](entry):
            return False
    return True


if __name__ == "__main__":
    passports = read_passports(argv[-1])
    num_valid_passports = sum(is_passport_valid(p) for p in passports)
    print(f"Of the given {len(passports)} passports, {num_valid_passports} are valid.")
    num_really_valid_passports = sum(is_passport_really_valid(p) for p in passports)
    print(
        f"Of the given {len(passports)} passports, {num_really_valid_passports} are really valid."
    )
