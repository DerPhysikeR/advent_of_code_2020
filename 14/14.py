from sys import argv


def read_program(filename):
    with open(filename) as stream:
        return stream.read().strip().split("\n")


class PortComputer:
    def __init__(self):
        self.memory = {}
        self.mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    def run_line(self, line):
        if line.startswith("mask"):
            self.mask = line.partition(" = ")[2]
        elif line.startswith("mem"):
            address, _, value = line.partition("] = ")
            self._write_to_memory(int(address[4:]), int(value))
        else:
            raise ValueError("Invalid command `{line}`.")

    def _write_to_memory(self, address, value):
        force_on_mask = int(self.mask.replace("X", "0"), 2)
        force_off_mask = int(self.mask.replace("X", "1"), 2)
        self.memory[address] = (value | force_on_mask) & force_off_mask

    def sum_values(self):
        return sum(value for value in self.memory.values())


def to_binary_string(number, length):
    return bin(number)[2:].zfill(length)


def address_generator(address, mask):
    """
    >>> list(address_generator(4, "000"))
    [4]
    >>> list(address_generator(4, "010"))
    [6]
    >>> list(address_generator(4, "01X"))
    [6, 7]
    >>> list(address_generator(4, "X01X"))
    [6, 14, 7, 15]
    """
    address_string = to_binary_string(
        address | int(mask.replace("X", "0"), 2), len(mask)
    )
    address_string = "".join(m if m == "X" else a for a, m in zip(address_string, mask))
    num_floating_bits = address_string.count("X")
    for i in range(2 ** num_floating_bits):
        fill_values = list(to_binary_string(i, num_floating_bits))
        new_address_string = "".join(
            a if a != "X" else fill_values.pop() for a in address_string
        )
        yield int(new_address_string, 2)


class ActualPortComputer(PortComputer):
    def _write_to_memory(self, address, value):
        for addr in address_generator(address, self.mask):
            self.memory[addr] = value


if __name__ == "__main__":
    program = read_program(argv[-1])

    # part 1
    port_computer = PortComputer()
    for line in program:
        port_computer.run_line(line)
    print(f"The sum of all non-zero values in memory is {port_computer.sum_values()}.")

    # part 2
    port_computer = ActualPortComputer()
    for line in program:
        port_computer.run_line(line)
    print(f"The sum of all non-zero values in memory is {port_computer.sum_values()}.")
