
from pprint import pprint
from collections import namedtuple
from math import floor
import re

class Item:

    def __init__(self, level, monkey):
        self._level = level

    def get_level(self):
        return self._level

    def set_level(self, new_level):
        self._level = new_level

    def __str__(self):
        return f"Item({self._level})"
    def __repr__(self):
        return self.__str__()

TIMES_REGEX=re.compile("^old \* (\d+)$")
PLUS_REGEX=re.compile("^old \+ (\d+)$")

def get_operation(opstr):
    #times pattern
    match = TIMES_REGEX.match(opstr)
    if match:
        arg = int(match.group(1))
        def myfun(old):
            return old * arg
        return myfun
    #plus pattern
    match = PLUS_REGEX.match(opstr)
    if match:
        arg = int(match.group(1))
        def myfun(old):
            return old + arg
        return myfun
    # power pattern
    if opstr == "old * old":
        def myfun(old):
            return old * old
        return myfun
    #else failed
    raise RuntimeError(f'No operation for string "{opstr}"')

class Monkey:
    def __init__(
        self, 
        index, 
        item_list, 
        operation_str, 
        test_value, 
        true_monkey_index, 
        false_monkey_index
    ):
        self.index = index 
        self.item_list = item_list
        self.operation_str = operation_str
        self.test_value = test_value
        self.true_monkey_index = true_monkey_index
        self.false_monkey_index = false_monkey_index
        self.monkey_list = None #set later

        self.operation = get_operation(self.operation_str)

        self.inspection_count = 0
        self.do_worry_reduction = True

        self.lcm = None

    def get_lcm(self):
        if self.lcm is None:
            assert len(self.monkey_list) > 0
            self.lcm = 1
            for m in self.monkey_list:
                self.lcm *= m.test_value
        return self.lcm

    def __str__(self):
        return f'Monkey(id={self.index},items={self.item_list},operation="{self.operation_str}",' \
            f'test="divisible by {self.test_value}",if_true={self.true_monkey_index},' \
            f'if_false={self.false_monkey_index})'

    def __repr__(self):
        return self.__str__()

    def add_item(self, new_item):
        self.item_list.append(new_item)

    def do_round(self):
        for item in self.item_list:
            self.inspection_count += 1
            #inspect
            item.set_level(self.operation(item.get_level()))
            if self.do_worry_reduction:
                # devalue
                item.set_level(int(floor(item.get_level() / 3)))
            else:
                item.set_level(item.get_level() % self.get_lcm())
            # test
            test_result = (item.get_level() % self.test_value) == 0
            if test_result:
                self.monkey_list[self.true_monkey_index].add_item(item)
            else:
                self.monkey_list[self.false_monkey_index].add_item(item)


        #clear the item list because we threw them all
        self.item_list = []


def parse_monkey(lines):

    # monkey line
    tokens = lines[0].strip().split()
    assert len(tokens) == 2
    assert tokens[0] == "Monkey"
    index = int(tokens[1].strip(':'))
    # starting items
    tokens = lines[1].strip().split(":")
    assert len(tokens) == 2
    assert tokens[0] == "Starting items"
    items = [ Item(int(i.strip()), index) for i in tokens[1].split(',') ]
    # operation
    tokens = lines[2].strip().split("=")
    assert tokens[0] == 'Operation: new '
    operation_str = tokens[1].strip()
    # test line
    tokens = lines[3].strip().split()
    assert tokens[:-1] == ["Test:","divisible","by"]
    test_value = int(tokens[-1])
    # true line
    tokens = lines[4].strip().split()
    assert tokens[:-1] == ["If","true:","throw","to","monkey"]
    true_value = int(tokens[-1])
    # false line
    tokens = lines[5].strip().split()
    assert tokens[:-1] == ["If","false:","throw","to","monkey"]
    false_value = int(tokens[-1])

    return Monkey(
        index=index,
        item_list = items,
        operation_str = operation_str,
        test_value = test_value,
        true_monkey_index=true_value,
        false_monkey_index=false_value,
    )
    

def load_input(filename):
    monkeys = []
    with open(filename) as infile:
        lines = infile.readlines()
        for i in range(int((len(lines)+1)/7)):
            monkey_lines = lines[i*7:(i*7)+7]
            monkeys.append(parse_monkey(monkey_lines))

    for monkey in monkeys:
        monkey.monkey_list = monkeys

    return monkeys

def monkey_business(monkeys, rounds, rounds_of_interest):
    for round in range(rounds):
        #execute the round
        for monkey in monkeys:
            monkey.do_round()
        #print something
        if round+1 in rounds_of_interest:
            print("===============================")
            print("Round", round+1)
            # for monkey in monkeys:
            #     print(f"Monkey {monkey.index} has items {[ i.get_level() for i in monkey.item_list]}")
            for monkey in monkeys:
                print(f"Monkey {monkey.index} has handled {monkey.inspection_count} items")


    #summarize results
    inspections = sorted([ m.inspection_count for m in monkeys ])
    print(inspections)

    #monkey business is the product of the top 2 monkeys
    return inspections[-1]*inspections[-2]


def part1(monkeys):
    return monkey_business(monkeys, 20, list(range(1,21)))

def part2(monkeys):
    for monkey in monkeys:
        monkey.do_worry_reduction = False
    return monkey_business(monkeys, 10000, [1,20,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])

if __name__ == '__main__':

    filename='day11/test.txt'
    filename='day11/input.txt'

    monkeys = load_input(filename)

    # pprint(monkeys)

    # print('part 1', part1(monkeys))

    print('part 2', part2(monkeys))

