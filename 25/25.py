from sys import argv


def read_public_keys(filename):
    with open(filename) as stream:
        return [int(key) for key in stream.read().strip().split("\n")]


def generate_transformations(subject_number):
    value = 1
    while True:
        yield (value := (value * subject_number) % 20201227)


def transform_subject_number(subject_number, loop_size):
    value = None
    for _, value in zip(range(loop_size), generate_transformations(subject_number)):
        pass
    return value


def find_loop_size(public_key, subject_number=7):
    count = 0
    for count, value in enumerate(generate_transformations(subject_number), 1):
        if value == public_key:
            break
    return count


if __name__ == "__main__":
    card_key_pub, door_key_pub = read_public_keys(argv[-1])
    card_loop_size = find_loop_size(card_key_pub)
    door_loop_size = find_loop_size(door_key_pub)
    assert (
        key := transform_subject_number(card_key_pub, door_loop_size)
    ) == transform_subject_number(door_key_pub, card_loop_size)
    print(key)
