
class ALUstate:

    def __init__(self, registers=None):
        if registers is None:
            self.registers = {
                'w':0,
                'x':0,
                'y':0,
                'z':0,            
            }
        else:
            self.registers = registers

    def copy(self):
        return ALUstate(dict(self.registers))

    def reset(self):
        for k in self.registers:
            self.registers[k] = 0

class ALU:

    def __init__(self):
        self.OP_MAP = {
            'inp':self._instruction_inp,
            'add':self._instruction_add,
            'mul':self._instruction_mul,
            'div':self._instruction_div,
            'mod':self._instruction_mod,
            'eql':self._instruction_eql,
        }

    def parse_instructions(self, lines):
        alu_state = ALUstate()
        instructions = []
        for line in lines:
            tokens = line.strip().split()
            # print(tokens)
            assert len(tokens) == 2 or len(tokens) == 3
            op = tokens[0]
            assert op in self.OP_MAP
            args = tokens[1:]
            assert args[0] in alu_state.registers
            if len(args) == 2:
                if args[1] not in alu_state.registers:
                    args[1] = int(args[1])
            instructions.append((op, args))
        return instructions

    def run_instruction_sequence(self, alu_state, instructions, input):
        """Run a list of instruction tuples created by parse_instruction"""
        op,args = instructions[0]
        assert op == 'inp'
        self.OP_MAP[op](*args, alu_state = alu_state, input=input)
        for op, args in instructions[1:]:
            self.OP_MAP[op](*args, alu_state = alu_state)

    def _instruction_inp(self, arg1, alu_state=None, input=None):
        # inp a - Read an input value and write it to variable a.
        assert isinstance(input, int)
        alu_state.registers[arg1] = input
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_add(self, arg1, arg2, alu_state=None):
        # add a b - Add the value of a to the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        alu_state.registers[arg1] = alu_state.registers[arg1] + arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mul(self, arg1, arg2, alu_state=None):
        # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        alu_state.registers[arg1] = alu_state.registers[arg1] * arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_div(self, arg1, arg2, alu_state=None):
        # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        alu_state.registers[arg1] = int(alu_state.registers[arg1] / arg2)
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mod(self, arg1, arg2, alu_state=None):
        # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        alu_state.registers[arg1] = alu_state.registers[arg1] % arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_eql(self, arg1, arg2, alu_state=None):
        # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]

        assert isinstance(arg2, int)
        alu_state.registers[arg1] = 1 if alu_state.registers[arg1] == arg2 else 0

        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

class AluTree:

    def create_instruction_sets(self, lines):
        instructions = self.alu.parse_instructions(lines)
        instruction_sets = []
        current_iset = None

        for inst in instructions:
            if inst[0] == 'inp':
                if current_iset is not None:
                    instruction_sets.append(current_iset)
                current_iset = [inst]
            else:
                current_iset.append(inst)
        if len(current_iset) > 0:
            instruction_sets.append(current_iset)
        assert len(instruction_sets) == 14
        return instruction_sets

    def __init__(self, lines):

        self.alu = ALU()
        self.digits = [9,8,7,6,5,4,3,2,1]
        self.places = 14
        self.all_valid_results = []
        self.number_processed = 0

        self.instruction_sets = self.create_instruction_sets(lines)

    def get_important_inputs_for_instruction_sets(self):
        alu_state = ALUstate()

        def destroys_value(op, args):
            if op == 'inp':
                print(f"input into {args[0]}")
                assert len(args) == 1
                return args[0]
            if op == 'mul' and args[1] == 0:
                print(f"multiple {args[0]} by 0")
                return args[0]
            return None

        for iset_index, iset in enumerate(self.instruction_sets):
            matters = [ r for r in alu_state.registers.keys() ] 
            for op, args in iset:
                destroyed_value = destroys_value(op, args)
                if destroyed_value is not None and destroyed_value in matters:
                    matters.remove(destroyed_value)
            print(f"For iset {iset_index+1}, state that matters is: {matters}")
            assert matters == ['z']
            




    def run(self):
        initial_alu_state = ALUstate()
        self.solutions = self._iterate_place(0, initial_alu_state, "")

    def _iterate_place(self, depth, parent_alu_state, parent_input_string):
        this_instruction_set = self.instruction_sets[depth]
        z_values_seen = set()
        for digit in self.digits:
            #make a copy of the parent ALU state and run the current digit
            current_alu_state = parent_alu_state.copy()
            self.alu.run_instruction_sequence(current_alu_state, this_instruction_set, digit)
            
            #see if we've seen this Z value before:
            z_val = current_alu_state.registers['z']
            if z_val in z_values_seen:
                print(f"Skipping further iteration after {parent_input_string+str(digit)} because we've already seen the Z value {z_val}")
                continue
            else:
                print(f"new zval after {parent_input_string+str(digit)}: {z_val}")
                z_values_seen.add(z_val)

            #recurse for additional digits
            if depth == self.places-1:
                #halting condition, check the Z register
                self.number_processed += 1
                if current_alu_state.registers['z'] == 0:
                    #we found a valid program return
                    final_number = parent_input_string + str(digit)
                    print("VALID RETURN: ", final_number)
                    self.all_valid_results.append(final_number)
                else:
                    if self.number_processed % 100000 == 0:
                        print("Progress:", parent_input_string + str(digit))
            else:
                #recurse for the next place
                self._iterate_place(depth+1, current_alu_state, parent_input_string+str(digit))

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

def part1_bruteforce(lines):

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
        
def part1_tree(lines):
    atree = AluTree(lines)
    atree.get_important_inputs_for_instruction_sets()
    atree.run()
    print(atree.all_valid_results)

if __name__ == "__main__":
    with open('day24.txt') as infile:
        lines = infile.readlines()

    part1_tree(lines)