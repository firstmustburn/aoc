
from pprint import pprint
from collections import namedtuple

NOOP_OP = 'noop'
ADDX_OP = 'addx'

Instruction = namedtuple('Instruction', ['op', 'arg'])

class CPU:
    def __init__(self):
        self.x = 1
        # the history of the value at the end of the Nth cycle
        # insert a value for the 0th entry so that the list index is the cycle number
        self.history = [1]

    def execute(self, instruction):
        if instruction.op == NOOP_OP:
            #after one cycle the value is the same
            self.history.append(self.x)
        elif instruction.op == ADDX_OP:
            #after one cycle the value is the same
            self.history.append(self.x)
            #after the next cycle, the value changes and the register changes
            self.x += instruction.arg
            self.history.append(self.x)
        else:
            raise RuntimeError(f'Unknown opcode {instruction}')

    def get_signal_strength(self, cycle):
        #look back one in the history because it's the value during the cycle, which is the
        #value at the end of the previous cycle
        return self.history[cycle-1] * cycle

def load_input(filename):
    instructions = []
    with open(filename) as infile:
        for line in infile:
            tokens = line.strip().split()
            if tokens[0] == NOOP_OP:
                assert len(tokens) == 1
                instructions.append(Instruction(NOOP_OP, None))
            elif tokens[0] == ADDX_OP:
                assert len(tokens) == 2
                instructions.append(Instruction(ADDX_OP, int(tokens[1])))
            else:
                raise RuntimeError(f'Unknown opcode {tokens}')
    return instructions

def part1(instructions):
    cpu = CPU()
    for instruction in instructions:
        cpu.execute(instruction)

    for index, value in enumerate(cpu.history):
        print(index,value)

    cycles = [20, 60, 100, 140, 180, 220]
    strengths = [ cpu.get_signal_strength(c) for c in cycles ]
    for c,s in zip(cycles, strengths):
        print('cycle',c,'strength',s)

    return sum(strengths), cpu


def part2(instructions, cpu):
    crt = ""
    for index in range(240):
        crt_offset = index % 40
        if abs(crt_offset - cpu.history[index]) <= 1:
            crt += "#"
        else:
            crt += "."
    # now print the crt
    for row in range(6):
        print(crt[row*40:(row+1)*40])

if __name__ == '__main__':

    # filename='day10/test.txt'
    filename='day10/input.txt'

    instructions = load_input(filename)

    result1, cpu = part1(instructions)
    print('part 1', result1)

    print('part 2', part2(instructions, cpu))

