from collections import namedtuple, defaultdict
from pprint import pprint
import time

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

    def __str__(self):
        return str(self.registers)

    def __repr__(self):
        return self.__str__()

class ALUerror(Exception):
    pass

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
        self.verbose = False

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

    def run_instruction_sequence(self, alu_state, instructions, input, verbose=False):
        """Run a list of instruction tuples created by parse_instruction"""
        old_verbose = self.verbose
        self.verbose = verbose
        op,args = instructions[0]
        assert op == 'inp'
        self.OP_MAP[op](*args, alu_state = alu_state, input=input)
        for op, args in instructions[1:]:
            self.OP_MAP[op](*args, alu_state = alu_state)
        self.verbose = old_verbose

    def _instruction_inp(self, arg1, alu_state=None, input=None):
        # inp a - Read an input value and write it to variable a.
        assert isinstance(input, int)
        if self.verbose:
            print(f"{arg1} <- {input}")
        alu_state.registers[arg1] = input
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_add(self, arg1, arg2, alu_state=None):
        # add a b - Add the value of a to the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        if self.verbose:
            print(f"{arg1} <- {alu_state.registers[arg1]} + {arg2}")

        alu_state.registers[arg1] = alu_state.registers[arg1] + arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mul(self, arg1, arg2, alu_state=None):
        # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        if self.verbose:
            print(f"{arg1} <- {alu_state.registers[arg1]} * {arg2}")

        alu_state.registers[arg1] = alu_state.registers[arg1] * arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_div(self, arg1, arg2, alu_state=None):
        # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        if arg2 == 0:
            raise ALUerror(f"div by 0: arg1 {arg1}->{alu_state.registers[arg1]} arg2 {arg2} with state {alu_state}")

        if self.verbose:
            print(f"{arg1} {int(alu_state.registers[arg1] / arg2)} <- {alu_state.registers[arg1]} / {arg2}")

        alu_state.registers[arg1] = int(alu_state.registers[arg1] / arg2)
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_mod(self, arg1, arg2, alu_state=None):
        # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]
        assert isinstance(arg2, int)
        if alu_state.registers[arg1] < 0:
            raise ALUerror(f"mod negative value arg1: {arg1}->{alu_state.registers[arg1]} arg2 {arg2} with state {alu_state}")
        if arg2 <= 0:
            raise ALUerror(f"mod by 0: arg1 {arg1}->{alu_state.registers[arg1]} arg2 {arg2} with state {alu_state}")

        if self.verbose:
            print(f"{arg1} {alu_state.registers[arg1] % arg2} <- {alu_state.registers[arg1]} mod {arg2}")

        alu_state.registers[arg1] = alu_state.registers[arg1] % arg2
        # for v in alu_state.registers.values():
        #     assert isinstance(v, int)

    def _instruction_eql(self, arg1, arg2, alu_state=None):
        # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
        if isinstance(arg2, str):
            arg2 = alu_state.registers[arg2]

        if self.verbose:
            print(f"{arg1} {1 if alu_state.registers[arg1] == arg2 else 0} <- {alu_state.registers[arg1]} == {arg2}")

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

    def __init__(self, lines, initial_limits):

        self.alu = ALU()
        self.digits = [9,8,7,6,5,4,3,2,1]
        self.places = 14
        self.all_valid_results = []
        self.number_processed = 0

        self.instruction_sets = self.create_instruction_sets(lines)
        self.z_limits = initial_limits
        self.z_limits_expanded = [True]*len(self.instruction_sets)
        self.valid_results_by_iset_index = defaultdict(dict) #map of iset index to map of (win, zin)->zout values seen in testing 


    def backsolve_iteration(self):

        prev_z_target_counts = [0]*len(self.instruction_sets)
        converged = False

        while not converged:

            converged = True #we will unset this in the iteration

            #initialise one iteration of the search
            iset_index = len(self.instruction_sets)-1
            z_targets = set([0])  # initial target is 0 because 0 is the valid output we are seeking from the algorithm

            print(f"Using limits {self.z_limits}")

            while iset_index >= 0:
                new_z_targets = set()

                if iset_index > 0:
                    should_new_search = any([ was_expanded for index, was_expanded in enumerate(self.z_limits_expanded) if index >= iset_index])
                    if should_new_search:
                        print(f"for iset {iset_index}, searching zin range {self.z_limits[iset_index]}")
                        for zin in range(0,self.z_limits[iset_index]+1):
                            #progress indicator
                            if zin % 100000 == 0 and zin > 0:
                                print(f"iset_index={iset_index}, zin={zin}")
                            for win in self.digits:
                                state = ALUstate()
                                state.registers['z'] = zin
                                self.alu.run_instruction_sequence(state, self.instruction_sets[iset_index], win)
                                if state.registers['z'] in z_targets:
                                    new_z_targets.add(zin)
                                    self.valid_results_by_iset_index[iset_index][(win, zin)] = state.registers['z']
                    else:
                        #reuse the existing results
                        for w,z in self.valid_results_by_iset_index[iset_index].keys():
                            new_z_targets.add(z)
                        print(f"for iset {iset_index}, reusing {len(new_z_targets)} results")

                    #check results and limits
                    if len(new_z_targets) == 0:
                        print(f"halt iteration at {iset_index} because no z_targets produced")
                        converged = False
                        self.z_limits[iset_index] = self.z_limits[iset_index] * 2
                        self.z_limits_expanded[iset_index] = True
                        print(f"increasing z_limit for {iset_index} to {self.z_limits[iset_index]}")
                    elif len(new_z_targets) > prev_z_target_counts[iset_index]:
                        #we fount more results, so increase our limit
                        print(f"for {iset_index}, found {len(new_z_targets)}, an increase from {prev_z_target_counts[iset_index]} the previous round")
                        converged = False
                        self.z_limits[iset_index] = self.z_limits[iset_index] * 2
                        self.z_limits_expanded[iset_index] = True
                        print(f"increasing z_limit for {iset_index} to {self.z_limits[iset_index]}")
                    else:
                        print(f"for {iset_index}, found {len(new_z_targets)}, no increase from {prev_z_target_counts[iset_index]} the previous round")
                        print(f"Maintaining z_limit for {iset_index} at {self.z_limits[iset_index]}")
                        self.z_limits_expanded[iset_index] = False
                else:
                    print(f"for iset {iset_index}, use zin=0")
                    zin = 0
                    for win in self.digits:
                        state = ALUstate()
                        state.registers['z'] = zin
                        self.alu.run_instruction_sequence(state, self.instruction_sets[iset_index], win)
                        if state.registers['z'] in z_targets:
                            new_z_targets.add(zin)
                            self.valid_results_by_iset_index[iset_index][(win, zin)] = state.registers['z']
                    
                    if converged and len(new_z_targets) == 0:
                        #double all limits
                        print(f"for {iset_index}, found no results, so increasing all z limits")
                        self.z_limits = { k: v*2 for k,v in self.z_limits.items() }
                        self.z_limits_expanded = [ True for v in self.z_limits_expanded ]
                        converged = False

                #remeber how many results we saw            
                prev_z_target_counts[iset_index] = len(new_z_targets)

                #iterate the loop state
                z_targets = new_z_targets
                iset_index -= 1




                if len(new_z_targets) == 0:
                    break #break the inner loop to start a new convergence iteration

            #done with this iteration
            print("Saving intermediate results to day24_backtrace_results_temp.txt")
            with open('day24_backtrace_results_temp.txt', 'w') as outfile:
                outfile.write(str(dict(self.valid_results_by_iset_index)))
 
        #the values have converged

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
            

    def _print_result_table(self, wlist, zlist, results):
            def print_row(row):
                print(','.join([str(r) for r in row]))

            #header
            print_row([""]+wlist)
            for z in zlist:
                row = [z]
                row.extend( results[(w,z)] for w in wlist )
                print_row(row)

    def make_iset_tables(self, wlist, zlist):
        for iset_index, iset in enumerate(self.instruction_sets):
            results = {}
            for z in zlist:
                for w in wlist:
                    alu_state = ALUstate()
                    alu_state.registers['z'] = z
                    self.alu.run_instruction_sequence(alu_state, iset, w)
                    results[(w,z)] = alu_state.registers['z']
            #print the table for each set
            print("*"*80)
            print(f"Iset {iset_index}")
            self._print_result_table(wlist, zlist, results)
            print("*"*80)


def pairwise(list_val):
    for l1, l2 in zip(list_val[:-1], list_val[1:]):
        yield l1, l2


def load_data(lines):
    z_limits = {
        13: 10000, 
        12: 10000, 
        11: 40000, 
        10: 40000, 
        9: 1024000, 
        8: 1024000, 
        7: 1024000, 
        6: 1024000, 
        5: 1024000, 
        4: 1024000, 
        3: 1024000, 
        2: 1024000, 
        1: 512000, 
        0: 32000
    }
    z_limits = { k:int(v/2) for k,v in z_limits.items() }

    atree = AluTree(lines, z_limits)
    assert len(atree.instruction_sets) == 14

    return atree

def part1_backsolve(atree):

    try:
        atree.backsolve_iteration()
    except Exception as ex:
        print(f"Caught exception: {ex}")

    with open('day24_backtrace_results_final.txt', 'w') as outfile:
        outfile.write(str(dict(atree.valid_results_by_iset_index)))

def part1_find_soln(data, atree, largest=True):

    # global max_word_seen

    def recurse_data(iset_index, z_match_value, number_values, z_list):
        #just get the results that match the z value we are looking for
        iset_inputs = [ isi for isi in data[iset_index].keys() if isi[1] == z_match_value]
        # print(f"iset_inputs for {iset_index}: {iset_inputs}")
        #sort by largest w first    
        iset_inputs = sorted(iset_inputs, key=lambda i: i[0], reverse=largest)
        # print(f"Keys for {iset_index}: {iset_inputs}") 
        for iset_input in iset_inputs:
            win, zin = iset_input
            print(f"at {iset_index}, ({win}, {zin}) -> {z_match_value}; running number={number_values}")
            assert zin == z_match_value
            iset_zout = data[iset_index][iset_input]
            #recurse until we get to the end
            if iset_index < len(atree.instruction_sets)-1:
                retval = recurse_data(iset_index+1, iset_zout, number_values+str(win), z_list + [zin])
                if retval is not None:
                    return retval
            else:
                # we are at the end
                final_result = number_values+str(win)
                print(f"at {iset_index}, number_value:", final_result)
                return final_result, z_list + [zin, iset_zout]

        # global max_word_seen


    # print(data.keys())
    result = recurse_data(0, 0, "", [])
    print(result)


if __name__ == "__main__":
    with open('day24.txt') as infile:
        lines = infile.readlines()

    atree = load_data(lines)

    # part1_backsolve(atree)

    with open('day24_backtrace_results_final.txt') as infile:
        data = eval(infile.read())

    print("Largest val")
    part1_find_soln(data, atree, True)
    print("Smallest val")
    part1_find_soln(data, atree, False)


# Largest val
# at 0, (4, 0) -> 0; running number=
# at 1, (5, 18) -> 18; running number=4
# at 2, (9, 479) -> 479; running number=45
# at 3, (8, 12469) -> 12469; running number=459
# at 4, (9, 324215) -> 324215; running number=4598
# at 5, (9, 12469) -> 12469; running number=45989
# at 6, (2, 324211) -> 324211; running number=459899
# at 7, (9, 12469) -> 12469; running number=4598992
# at 8, (9, 324213) -> 324213; running number=45989929
# at 9, (4, 8429555) -> 8429555; running number=459899299
# at 10, (6, 324213) -> 324213; running number=4598992994
# at 11, (1, 12469) -> 12469; running number=45989929946
# at 12, (9, 479) -> 479; running number=459899299461
# at 13, (9, 18) -> 18; running number=4598992994619
# at 13, number_value: 45989929946199
# ('45989929946199', [0, 18, 479, 12469, 324215, 12469, 324211, 12469, 324213, 8429555, 324213, 12469, 479, 18, 0])
# Smallest val
# at 0, (1, 0) -> 0; running number=
# at 1, (1, 15) -> 15; running number=1
# at 2, (9, 397) -> 397; running number=11
# at 3, (1, 10337) -> 10337; running number=119
# at 4, (2, 268776) -> 268776; running number=1191
# at 5, (8, 10337) -> 10337; running number=11912
# at 6, (1, 268778) -> 268778; running number=119128
# at 7, (4, 10337) -> 10337; running number=1191281
# at 8, (6, 268776) -> 268776; running number=11912814
# at 9, (1, 6988190) -> 6988190; running number=119128146
# at 10, (1, 268776) -> 268776; running number=1191281461
# at 11, (1, 10337) -> 10337; running number=11912814611
# at 12, (5, 397) -> 397; running number=119128146111
# at 13, (6, 15) -> 15; running number=1191281461115
# at 13, number_value: 11912814611156
# ('11912814611156', [0, 15, 397, 10337, 268776, 10337, 268778, 10337, 268776, 6988190, 268776, 10337, 397, 15, 0])
