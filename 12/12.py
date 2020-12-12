from sys import argv


def read_instructions(filename):
    with open(filename) as stream:
        return [(line[0], int(line[1:])) for line in stream.read().strip().split("\n")]


class Ship:

    INSTRUCTION_DICT = {
        "N": "move_north",
        "S": "move_south",
        "E": "move_east",
        "W": "move_west",
        "L": "turn_left",
        "R": "turn_right",
        "F": "move_forward",
    }

    DIRECTION_DICT = {0: "north", 90: "east", 180: "south", 270: "west"}

    def __init__(self):
        self.lattitude, self.longitude = 0, 0
        self.direction = 90

    def run_instruction(self, action, value):
        getattr(self, self.INSTRUCTION_DICT[action])(value)

    def move_north(self, value):
        self.lattitude += value

    def move_south(self, value):
        self.lattitude -= value

    def move_east(self, value):
        self.longitude += value

    def move_west(self, value):
        self.longitude -= value

    def turn_left(self, value):
        self.direction -= value

    def turn_right(self, value):
        self.direction += value

    def move_forward(self, value):
        getattr(self, f"move_{self.DIRECTION_DICT[self.direction % 360]}")(value)


def manhatten_norm(longitude, lattitude):
    return abs(longitude) + abs(lattitude)


if __name__ == "__main__":
    instructions = read_instructions(argv[-1])
    ship = Ship()
    for instruction in instructions:
        ship.run_instruction(*instruction)
    print(f"The new positions of the ship is ({ship.longitude}, {ship.lattitude}).")
    print(
        "The ship covered a Manhatten distance of "
        f"{manhatten_norm(ship.longitude, ship.lattitude)}."
    )
