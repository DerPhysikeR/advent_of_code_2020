from sys import argv


def read_program(filename):
    with open(filename) as stream:
        return stream.read().strip().split("\n")


class PortComputer:

    MAX_VALUE_36bit = 68719476735

    def __init__(self):
        self.memory = {}
        self.force_on_mask = 0
        self.force_off_mask = self.MAX_VALUE_36bit

    def run_line(self, line):
        if line.startswith("mask"):
            self._update_mask(line.partition(" = ")[2])
        elif line.startswith("mem"):
            address, _, value = line.partition("] = ")
            self._write_to_memory(int(address[4:]), int(value))
        else:
            raise ValueError("Invalid command `{line}`.")

    def _update_mask(self, string_mask):
        self.force_on_mask = int(string_mask.replace("X", "0"), 2)
        self.force_off_mask = int(string_mask.replace("X", "1"), 2)

    def _write_to_memory(self, address, value):
        self.memory[address] = (value | self.force_on_mask) & self.force_off_mask

    def sum_values(self):
        return sum(value for value in self.memory.values())


if __name__ == "__main__":
    program = read_program(argv[-1])
    port_computer = PortComputer()
    for line in program:
        port_computer.run_line(line)
    print(f"The sum of all non-zero values in memory is {port_computer.sum_values()}.")
