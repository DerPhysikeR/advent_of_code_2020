from sys import argv


def read_instructions(filename):
    with open(filename) as stream:
        instructions = stream.read().strip().split("\n")
        return instructions


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
        return cls(read_instructions(filename))


def does_program_terminate(emulator):
    visited_line_numbers = set()
    for line_number, instruction in emulator:
        if line_number in visited_line_numbers:
            break
        visited_line_numbers.add(line_number)
    else:
        return True
    return False


def instruction_replacer(instructions, to_replace, replacement):
    for i, instruction in enumerate(instructions):
        if to_replace in instruction:
            new_instructions = instructions[:]
            new_instructions[i] = new_instructions[i].replace(to_replace, replacement)
            yield new_instructions


if __name__ == "__main__":
    # part 1
    emulator = Emulator.from_file(argv[-1])
    visited_line_numbers, accumulator = set(), 0
    for line_number, instruction in emulator:
        if line_number in visited_line_numbers:
            break
        visited_line_numbers.add(line_number)
        accumulator = emulator.accumulator
        print(f"{line_number}: {instruction}")
    print(f"The accumulator had the value {accumulator} before the programm repeated.")

    # part 2
    original_instructions = read_instructions(argv[-1])
    for instructions in instruction_replacer(original_instructions, "jmp", "nop"):
        emulator = Emulator(instructions)
        if does_program_terminate(emulator):
            print(emulator.accumulator)
    for instructions in instruction_replacer(original_instructions, "nop", "jmp"):
        emulator = Emulator(instructions)
        if does_program_terminate(emulator):
            print(emulator.accumulator)
