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


SearchState = namedtuple('SearchState',['win', 'zin', 'zout'])

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

    def backsolve_2(self, z_limits):

        inputs_by_index = {}
        w_list = [1,2,3,4,5,6,7,8,9]

        iset_index = len(self.instruction_sets)-1
        z_targets = set([0])


        while iset_index >= 0:
            z_limit = z_limits[iset_index]
            new_z_targets = set()
            valid_inputs = set()
            # solution_inputs = [] #list of w,z pairs that give a desired output
            # print(f"in set {iset_index}, looking for inputs that achieve z_targets {z_targets}")

            for zin in range(z_limit+1):
                if zin % 10000 == 0 and zin > 0:
                    print(f"iset_index={iset_index}, zin={zin}")
                for win in w_list:
                    state = ALUstate()
                    state.registers['z'] = zin
                    self.alu.run_instruction_sequence(state, self.instruction_sets[iset_index], win)
                    if state.registers['z'] in z_targets:
                        new_z_targets.add(zin)
                        valid_inputs.add((win, zin))

            #done with this range
            # print(f"in set {iset_index}, found {len(valid_inputs)} solutions to get one of {len(z_targets)} targets")
            inputs_by_index[iset_index] = valid_inputs
            z_targets = new_z_targets
            iset_index -= 1

            if len(new_z_targets) == 0:
                print("Halt because no solution")
                break

        return inputs_by_index

    def search_with_hash_tables(self, z_limit):

        htables = [] #list of hash tables in the same order as the instruction sets
        for iset_index, iset in enumerate(self.instruction_sets):
            print(f"Creating table for iset {iset_index}")
            htable = defaultdict(list) #map of z output to lists of the two inputs that gave rise to it
            success_count = 0
            fail_count = 0
            for win in self.digits:
                for zin in range(0, z_limit+1): #go from 0 because negative z inputs are modded and fail 
                    try:
                        alu_state = ALUstate()
                        alu_state.registers['z'] = zin
                        self.alu.run_instruction_sequence(alu_state, iset, win)
                        htable[alu_state.registers['z']].append((win,zin))
                        success_count += 1
                    except ALUerror as ex:
                        # print(f"Operation failed for zin={zin}, win={win}: {ex}")
                        fail_count += 1
            #done with one table
            htables.append(htable)
            print(f"Finished table {iset_index}: success count={success_count}, fail_count={fail_count}")
        print("non-default-dictionaries")    
        htables = [ dict(ht) for ht in htables ]
        print("Table creation completes")

        # import sys
        # sys.exit(-1)

        global longest_so_far
        longest_so_far = []

        def recurse_htable(z_target, iset_index, inputs_so_far):
            global longest_so_far

            if len(inputs_so_far) > len(longest_so_far):
                longest_so_far = inputs_so_far
                print(f"longest sequence at {iset_index}:  {longest_so_far}")
                print(f"    z_target={z_target}")
                is_longest = True
            else:
                is_longest = False

            try:
                input_list = htables[iset_index][z_target]
            except KeyError:
                if iset_index <= 1 and is_longest:
                    print(" "*(len(self.instruction_sets)-iset_index), f"in {iset_index}: no ztarget for {z_target} in the hash table at {inputs_so_far}")
                return None
            #sort the list so that the largest win comes first -- this ensures the answer will be
            #the largest answer
            input_list.sort(key=lambda n: n[0], reverse=True)
            # print(input_list)
            # print(" "*(len(self.instruction_sets)-iset_index), f"in {iset_index}: target z = {z_target} --> {input_list}")

            if iset_index > 0:
                for win, zin in input_list:
                    if iset_index == 1:
                        print(" "*(len(self.instruction_sets)-iset_index), f"in {iset_index}: trying {win}, {zin}")
                    #recurse
                    result = recurse_htable(zin, iset_index-1, [win]+inputs_so_far)
                    if result is not None:
                        return result
                    # else:
                if iset_index == 1:
                    print(" "*(len(self.instruction_sets)-iset_index), f"in {iset_index}: no result for ztarget {z_target} for {[win]+inputs_so_far}")
                return None
            else:
                #halting condition on first iset:
                # the z input on the first set must be 0
                for win, zin in input_list:
                    if zin == 0:
                        result = [win] + inputs_so_far
                        print("SUCCESS: ", result)
                        return result
                print(" "*(len(self.instruction_sets)-iset_index), f"in {iset_index}: no result with zin==0 z_target {z_target} for {[win]+inputs_so_far}")
                return None

        iset_index = len(self.instruction_sets)-1
        retval = recurse_htable(0, iset_index, [])
        return retval



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
                # print(f"new zval after {parent_input_string+str(digit)}: {z_val}")
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

class BacksolveNode:
    def __init__(self, alu, instruction_sets, instruction_set_index, wlist, z_limit, z_target):
        self.cache = {} #map of win, zin -> zout
        self.alu = alu
        self.instruction_sets = instruction_sets
        self.instruction_set_index = instruction_set_index
        self.wlist = wlist
        self.z_limit = z_limit
        self.z_target = z_target
        self.depth = len(self.instruction_sets)-self.instruction_set_index

        self.child_map = {} #map of children nodes to z inputs
    
    def test_z(self, wval, zval):
        ckey = (wval,zval)
        try:
            return self.cache[ckey]
        except KeyError:
            pass
        alu_state = ALUstate()
        alu_state.registers['z'] = zval
        self.alu.run_instruction_sequence(alu_state, self.instruction_sets[self.instruction_set_index], wval)
        # print(f"in {self.instruction_set_index}, {wval} {zval} -> {alu_state.registers['z']} ")
        self.cache[ckey] = alu_state.registers['z']
        return alu_state.registers['z']

    def _find_inputs_for_z_value(self):
        for wval in self.wlist:
            for current_z in range(0, self.z_limit+1):
                z_out = self.test_z(wval, current_z)
                if z_out == self.z_target:
                    yield wval, -current_z
                if current_z > 0:
                    z_out = self.test_z(wval, -current_z)
                    if z_out == self.z_target:
                        yield wval, -current_z
            # no more

    def _find_inputs_for_final_z_value(self):

        for wval in self.wlist:
            z_out = self.test_z(wval, 0)
            if z_out == self.z_target:
                yield wval, 0
            # no more

    def run(self):
        # print(f"in {self.instruction_set_index}: searching for {self.z_target}")
        if self.instruction_set_index > 0:
            for win, zin in self._find_inputs_for_z_value():
                #skip zinputs we have already searched
                if zin in self.child_map:
                    print(" "*self.depth, f"in {self.instruction_set_index}: skip DUPLICATE ZIN {win},{zin}->{self.z_target}")
                    continue
                print(" "*self.depth, f"in {self.instruction_set_index}: found {win},{zin}->{self.z_target}")
                #new child to iterate
                new_child = BacksolveNode(self.alu, self.instruction_sets, self.instruction_set_index-1, self.wlist, self.z_limit, zin)
                self.child_map[zin] = new_child
                for child_result in new_child.run():
                    yield [SearchState(win, zin, self.z_target)] + child_result
        else:
            #we are in the final instruction set, so do a special search over the wlist with the zin = 0
            for win, zin in self._find_inputs_for_final_z_value():
                yield [SearchState(win, zin, self.z_target)]        
        # print(f"in {self.instruction_set_index}: finished searching for {self.z_target}")


class Backsolver:
    def __init__(self, instruction_sets, zlimit):
        self.alu = ALU()
        self.instruction_sets = instruction_sets
        self.wlist = [9,8,7,6,5,4,3,2,1]
        self.zlimit = zlimit

    def run(self):
        results = []
        root = BacksolveNode(self.alu, self.instruction_sets, len(self.instruction_sets)-1, self.wlist, self.zlimit, 0)
        for result in root.run():
            results.append(result)
            print("RESULT:", result)
        return results



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
        

def part1_tryout(lines):


    atree = AluTree(lines)

    wlist = [1,2,3,4,5,6,7,8,9]

    # zlist = list(range(1001))
    # atree.make_iset_tables(wlist, zlist)

    # try one of the partial inputs
    # wlist = [1,2,3,4,5,6,7,8,9]

    # fixed_inputs = [9, 8, 9, 9, 2, 9, 9, 4, 6, 1, 9, 8]

    # for w0 in wlist:
    #     for w1 in wlist:
    #         sequence = [w0, w1] + fixed_inputs
    #         for index, s_in in enumerate(sequence):
    #             state = ALUstate()
    #             atree.alu.run_instruction_sequence(state, atree.instruction_sets[index], s_in)
    #         if state.registers['z'] == 0:
    #             print("SUCCESS:")
    #         print(f"sequence {sequence} > state {state}")
            


    # z_targets = [0]
    # iset_index = 13
    z_targets = [10,11,12,13,14,15,16,17,18]
    iset_index = 12

    for zin in range(10000000):
        if zin % 100000 == 0:
            print(f"zin={zin}")
        for w in wlist:

            state = ALUstate()
            state.registers['z'] = zin
            atree.alu.run_instruction_sequence(state, atree.instruction_sets[iset_index], w)
            if state.registers['z'] in z_targets:
                print(f"win={w}; zin={zin}; state={state}")

    # # #second set
    # # zin = list(zout)
    # # zout = []
    # # for w in wlist:
    # #     for z in zin:
    # #         # print(f"w={w} for iset 0")
    # #         state = ALUstate()
    # #         state.registers['z'] = z
    # #         atree.alu.run_instruction_sequence(state, atree.instruction_sets[1], w)
    # #         # print(state)
    # #         zout.append(state.registers['z'])
    # #         print(f"w{w}, z{z} -> zout{state.registers['z']}")

def part1_tree(lines):
    atree = AluTree(lines)

    zlimit = 5000
    while 1:
        print("Running with limit", zlimit)
        bs = Backsolver(atree.instruction_sets, zlimit)
        results = bs.run()
        if len(results) > 0:
            break
        zlimit *= 2

    print (results)    

def part1_hash_tables(lines):
    atree = AluTree(lines)

    result = None
    table_size = 10000
    while result is None:
        print("hashing with table size ", table_size)
        result = atree.search_with_hash_tables(table_size)
        table_size *= 2

    print(result)


def part1_backsolve_2(lines):
    atree = AluTree(lines)


    z_limits = {
        13:5000,
        12:5000,
        11:5000,
        10:5000,
        9:5000,
        8:5000,
        7:5000,
        6:5000,
        5:5000,
        4:5000,
        3:5000,
        2:5000,
        1:5000,
        0:5000,
    }

    prev_inputs_by_index = atree.backsolve_2(z_limits)
    z_limits = { k:v*2 for k,v in z_limits.items() }

    converged = False

    while not converged:
        print(f"running z_limits: {z_limits}")

        inputs_by_index = atree.backsolve_2(z_limits)

        #check the results
        converged = True
        for index in z_limits:
            try:
                prev_count = len(prev_inputs_by_index[index])
            except KeyError:
                prev_count = 0
            try:
                current_count = len(inputs_by_index[index])
            except KeyError:
                current_count = 0
            assert current_count >= prev_count

            if current_count == 0:
                z_limits[index] = z_limits[index] * 2
                print(f"Index {index} has {current_count} solutions, so limit increased to {z_limits[index]}")
                converged=False
            elif current_count > prev_count:
                z_limits[index] = z_limits[index] * 2
                print(f"Index {index} has {current_count} solutions increased from {prev_count}, so limit increased to {z_limits[index]}")
                print(list(inputs_by_index[index])[:30])
                converged=False
            else:
                print(f"Index {index} is steady at {current_count} solutions, so limit remains {z_limits[index]}")

        prev_inputs_by_index = inputs_by_index
        time.sleep(5)


if __name__ == "__main__":
    with open('day24.txt') as infile:
        lines = infile.readlines()

    # part1_tree(lines)
    # part1_tryout(lines)
    # part1_hash_tables(lines)
    part1_backsolve_2(lines)