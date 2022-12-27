from __future__ import annotations
from typing import List, Tuple, Union, Callable, Dict, Any

from pprint import pprint
from collections import namedtuple

OPERATIONS = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: x/y,
    '=': lambda x,y: x == y,
}

HUMAN_ID = 'humn'
LEFT = 0
RIGHT = 1


class OpMonkey:

    def __init__(self, id, operation: str, operands: Tuple[Any, Any]):
        self.id = id
        self.operation_str = operation
        self.operation = OPERATIONS[operation]
        self.operands = operands

    def compute(self):
        m1 = self.operands[0].compute()
        m2 = self.operands[1].compute()
        return self.operation(m1,m2)

    def has_child(self, id: str) -> bool:
        return self.operands[0].has_child(id) or self.operands[1].has_child(id) 

    def __str__(self):
        return f'{self.id}( {self.operands[0].id} {self.operation_str} {self.operands[1].id} )'

    def __repr__(self):
        return self.__str__()

class ValMonkey:

    def __init__(self, id, value: int):
        self.id = id
        self.value = value

    def compute(self):
        return self.value

    def has_child(self, id: str) -> bool:
        return id == self.id

    def __str__(self):
        return f'{self.id}( {self.value} )'

    def __repr__(self):
        return self.__str__()

def parse_monkey(mstr: str) -> Union(OpMonkey, ValMonkey):
    # Example inputs: 
    # root: pppw + sjmn
    # dbpl: 5
    tokens = mstr.strip().split()
    id = tokens[0].strip(':')
    if len(tokens) == 2:
        value = int(tokens[1])
        return ValMonkey(id, value)
    elif len(tokens) == 4:
        operands = (tokens[1], tokens[3])
        operation = tokens[2]
        return OpMonkey(id, operation, operands)
    else:
        raise RuntimeError(f"Unhandled input: {mstr}")


def load_input(filename):
    with open(filename) as infile:
        monkeys = []
        for line in infile:
            monkeys.append(parse_monkey(line))

    monkey_map = { m.id:m for m in monkeys }

    #put the objects in for the operand strings
    for monkey in monkey_map.values():
        if isinstance(monkey, OpMonkey):
            monkey.operands = ( monkey_map[monkey.operands[0]], monkey_map[monkey.operands[1]]  ) 

    return monkey_map

def split_monkey(monkey: OpMonkey):
    """Return the the subtree containing the human element, the index of that operand, and the computation of the other operand"""
    if monkey.operands[0].has_child(HUMAN_ID):
        return monkey.operands[LEFT], LEFT, monkey.operands[RIGHT].compute()
    else:
        return monkey.operands[RIGHT], RIGHT, monkey.operands[LEFT].compute()

def reverse_compute(monkey: OpMonkey, target_value: float):
    # target_value = monkey.op0 monkey.operation monkey.op1
    # op0 and op1 might be an operation containing the human value

    subtree, subside, constval = split_monkey(monkey)

    if monkey.operation_str == '+':
        #reverse targetval = (search) + const --> commutative, so order doesn't matter
        new_target_value = target_value - constval
    elif monkey.operation_str == '*':
        #reverse targetval = (search) * const --> commutative, so order doesn't matter
        new_target_value = target_value / constval
    elif monkey.operation_str == '-':
        if subside == LEFT:                
            #reverse targetval = (search) - const
            new_target_value = target_value + constval
        else:                
            #reverse targetval = const - (search) --> (search) = - (target_val - const)
            new_target_value = -1 * (target_value - constval)
    elif monkey.operation_str == '/':
        if subside == LEFT:                
            #reverse targetval = (search) / const
            new_target_value = target_value * constval
        else:                
            #reverse targetval = const / (search) --> (search) = const / target_val
            new_target_value = constval / target_value
    else:
        raise RuntimeError(f"Unhandled operation {monkey.operation_str}")

    # termination condition
    if subtree.id == HUMAN_ID:
        return new_target_value

    #recurse with the subtree and the new target value
    return reverse_compute(subtree, new_target_value)


def part1(monkey_map):

    return monkey_map['root'].compute()

def part2(monkey_map: Dict[str, Union[OpMonkey, ValMonkey]]):

    human = monkey_map[HUMAN_ID]
    root = monkey_map['root']

    # make modifications
    root.operation = OPERATIONS['=']
    root.operation_str = '='

    search_tree, search_side, target_value = split_monkey(root)
    #compute a value for HUMN so that search_tree evaluates to target_value

    human_value = reverse_compute(search_tree, target_value)

    #double check
    human.value = 3272260914328

    assert root.compute() == True
    
    return human_value
        

if __name__ == '__main__':

    filename='day21/test.txt'
    filename='day21/input.txt'

    monkey_map = load_input(filename)

    # for monkey in monkey_map.values():
    #     print(monkey)

    # print('part 1', part1(monkey_map))

    print('part 2', part2(monkey_map))

