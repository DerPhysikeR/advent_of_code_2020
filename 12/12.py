from sys import argv


def read_instructions(filename):
    with open(filename) as stream:
        return [(line[0], int(line[1:])) for line in stream.read().strip().split("\n")]


INSTRUCTION_DICT = {
    "N": "move_north",
    "S": "move_south",
    "E": "move_east",
    "W": "move_west",
    "L": "turn_left",
    "R": "turn_right",
    "F": "move_forward",
}


class Ship:

    DIRECTION_DICT = {0: "north", 90: "east", 180: "south", 270: "west"}

    def __init__(self, longitude=0, lattitude=0):
        self.longitude, self.lattitude = longitude, lattitude
        self.direction = 90

    def run_instruction(self, action, value):
        getattr(self, INSTRUCTION_DICT[action])(value)

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


class ActualShip:
    def __init__(self):
        self.waypoint = Ship(10, 1)
        self.longitude, self.lattitude = 0, 0

    def run_instruction(self, action, value):
        obj = self if action in "LRF" else self.waypoint
        getattr(obj, INSTRUCTION_DICT[action])(value)

    def move_forward(self, value):
        self.longitude += value * self.waypoint.longitude
        self.lattitude += value * self.waypoint.lattitude

    def turn_left(self, value):
        for _ in range(value // 90):
            self.waypoint.longitude, self.waypoint.lattitude = (
                -self.waypoint.lattitude,
                self.waypoint.longitude,
            )

    def turn_right(self, value):
        for _ in range(value // 90):
            self.waypoint.longitude, self.waypoint.lattitude = (
                self.waypoint.lattitude,
                -self.waypoint.longitude,
            )


def manhatten_norm(longitude, lattitude):
    return abs(longitude) + abs(lattitude)


def run(ship, instructions):
    for instruction in instructions:
        ship.run_instruction(*instruction)
    print(f"The new positions of the ship is ({ship.longitude}, {ship.lattitude}).")
    print(
        "The ship covered a Manhatten distance of "
        f"{manhatten_norm(ship.longitude, ship.lattitude)}."
    )


if __name__ == "__main__":
    instructions = read_instructions(argv[-1])
    # part 1
    run(Ship(), instructions)
    # part 2
    run(ActualShip(), instructions)
