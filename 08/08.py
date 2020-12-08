from sys import argv


class Emulator:
    def __init__(self, instructions):
        self.accumulator = 0
        self.line_number = 0
        self.instructions = instructions

    def __iter__(self):
        return self

    def __next__(self):
        if self.line_number >= len(self.instructions):
            raise StopIteration
        line_number, instruction = self.line_number, self.instructions[self.line_number]
        self._execute(instruction)
        return line_number, instruction

    def _execute(self, instruction):
        opcode, argument = instruction.split(" ")
        getattr(self, f"_{opcode}")(int(argument))

    def _acc(self, argument):
        self.accumulator += argument
        self.line_number += 1

    def _jmp(self, argument):
        self.line_number += argument

    def _nop(self, _):
        self.line_number += 1

    @classmethod
    def from_file(cls, filename):
        with open(filename) as stream:
            instructions = stream.read().strip().split("\n")
            return cls(instructions)


if __name__ == "__main__":
    emulator = Emulator.from_file(argv[-1])
    visited_line_numbers, accumulator = set(), 0
    for line_number, instruction in emulator:
        if line_number in visited_line_numbers:
            break
        visited_line_numbers.add(line_number)
        accumulator = emulator.accumulator
        print(f"{line_number}: {instruction}")
    print(f"The accumulator had the value {accumulator} before the programm repeated.")

