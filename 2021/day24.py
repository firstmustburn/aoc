
class ALU:

    def __init__(self):
        self.registers = {
            'w':0,
            'x':0,
            'y':0,
            'z':0,            
        }
        self.OP_MAP = {
            'inp':self._instruction_inp,
            'add':self._instruction_add,
            'mul':self._instruction_mul,
            'div':self._instruction_div,
            'mod':self._instruction_mod,
            'eql':self._instruction_eql,
        }
        self.inputs = []

    def parse_instructions(self, lines):
        instructions = []
        for line in lines:
            tokens = line.strip().split()
            # print(tokens)
            assert len(tokens) == 2 or len(tokens) == 3
            op = tokens[0]
            assert op in self.OP_MAP
            args = tokens[1:]
            assert args[0] in self.registers
            if len(args) == 2:
                if args[1] not in self.registers:
                    args[1] = int(args[1])
            instructions.append((op, args))
        return instructions

    def run_instruction_sequence(self, instructions, inputs):
        """Run a list of instruction tuples created by parse_instruction"""
        self.inputs = inputs
        for i in inputs:
            assert isinstance(i, int)

        for k in self.registers:
            self.registers[k] = 0

        for op, args in instructions:
            self.OP_MAP[op](*args)

    def _get_next_input(self):
        retval = self.inputs[0]
        self.inputs = self.inputs[1:]
        return retval

    def _instruction_inp(self, arg1):
        # inp a - Read an input value and write it to variable a.
        self.registers[arg1] = self._get_next_input()
        # for v in self.registers.values():
        #     assert isinstance(v, int)

    def _instruction_add(self, arg1, arg2):
        # add a b - Add the value of a to the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = self.registers[arg2]
        assert isinstance(arg2, int)
        self.registers[arg1] = self.registers[arg1] + arg2
        # for v in self.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mul(self, arg1, arg2):
        # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = self.registers[arg2]
        assert isinstance(arg2, int)
        self.registers[arg1] = self.registers[arg1] * arg2
        # for v in self.registers.values():
        #     assert isinstance(v, int)

    def _instruction_div(self, arg1, arg2):
        # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
        if isinstance(arg2, str):
            arg2 = self.registers[arg2]
        assert isinstance(arg2, int)
        self.registers[arg1] = int(self.registers[arg1] / arg2)
        # for v in self.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mod(self, arg1, arg2):
        # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
        if isinstance(arg2, str):
            arg2 = self.registers[arg2]
        assert isinstance(arg2, int)
        self.registers[arg1] = self.registers[arg1] % arg2
        # for v in self.registers.values():
        #     assert isinstance(v, int)

    def _instruction_eql(self, arg1, arg2):
        # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
        if isinstance(arg2, str):
            arg2 = self.registers[arg2]

        assert isinstance(arg2, int)
        self.registers[arg1] = 1 if self.registers[arg1] == arg2 else 0

        # for v in self.registers.values():
        #     assert isinstance(v, int)

class ModelNumSequence:

    def __init__(self):
        self.digits = [9]*14

    def get_digits(self):
        return list(self.digits)

    def _internal_decrement(self, place):
        self.digits[place] -= 1
        # print("after decrement of", place, ":", self.digits)
        if self.digits[place] == 0:
            self.digits[place] = 9
            if place > 0:
                self._internal_decrement(place-1)
            else:
                raise RuntimeError("Underflow")

    def decrement(self):
        try:
            self._internal_decrement(len(self.digits)-1)
            return True
        except RuntimeError:
            print("Underflow")
            return False

def part1(lines):

    alu = ALU()
    program = alu.parse_instructions(lines)

    digits = ModelNumSequence()
    digit_count = 0
    while 1:
        input_vals = digits.get_digits()
        alu.run_instruction_sequence(program, input_vals)
        if alu.registers['z'] == 0:
            print("MONAD found: ", input_vals)
        digit_count += 1
        if digit_count % 10000 == 0:
            print("Progress:", input_vals)
        if not digits.decrement():
            break
        




if __name__ == "__main__":
    with open('day24.txt') as infile:
        lines = infile.readlines()

    part1(lines)