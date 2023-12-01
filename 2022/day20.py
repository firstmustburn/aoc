from __future__ import annotations
from typing import List, Tuple

from pprint import pprint
from collections import namedtuple

def dprint(*args, **kwargs):
    print(*args, **kwargs)

def load_input(filename):
    with open(filename) as infile:
        return [ int(line.strip()) for line in infile]

class Item:
    def __init__(self, original_postion: int, move_amount: int, list_size: int):
        self.original_position = original_postion
        self.move_amount= move_amount
        self.next: Item = None
        self.prev: Item = None
        self.list_size: int = list_size

    def insert_after(self, new_item: Item):
        assert new_item.next is None
        assert new_item.prev is None

        next_item = self.next

        # dprint(f'Insert after puts {new_item} between {self} and {next_item}')

        self.next = new_item
        next_item.prev = new_item

        new_item.next = next_item
        new_item.prev = self
        
    def insert_before(self, new_item: Item):
        assert new_item.next is None
        assert new_item.prev is None

        prev_item = self.prev

        # dprint(f'Insert before puts {new_item} between {prev_item} and {self}')

        self.prev = new_item
        prev_item.next = new_item

        new_item.next = self
        new_item.prev = prev_item

    def remove(self):
        prev_item = self.prev
        next_item = self.next
        # dprint(f'Removing {self} between {prev_item} and {next_item}')
        prev_item.next = next_item
        next_item.prev = prev_item
        self.prev = None
        self.next = None

    def advance(self, amount, fullmod=False):
        #return the amount-th item from this item
        if fullmod:
            actual_move_amount = abs(amount) % (self.list_size)
        else:
            actual_move_amount = abs(amount) % (self.list_size-1)
        if actual_move_amount == 0:
            return self
        if amount > 0:
            temp = self
            for i in range(actual_move_amount):
                temp = temp.next
            return temp
        elif amount < 0:
            temp = self
            for i in range(abs(actual_move_amount)):
                temp = temp.prev
            return temp
        else:
            return self
        
    def __str__(self):
        return f'{self.original_position}/{self.move_amount}'
    
    def __repr__(self):
        return self.__str__()


def build_linked_list(num_list: List[int]) -> Tuple(List[Item], Item) :
    item_list = []
    item_count = len(num_list)
    zero_item = None
    for index, num_val in enumerate(num_list):
        item = Item(index, num_val, item_count)
        item_list.append(item)
        if num_val == 0:
            assert zero_item is None
            zero_item = item
    #link up the first and last items
    for i1, i2 in zip(item_list[:-1], item_list[1:]):
        i1.next = i2
        i2.prev = i1
    #do the wraparound links
    item_list[-1].next = item_list[0]
    item_list[0].prev = item_list[-1]
    return item_list, zero_item

def print_list(head: Item):
    print(head, end =" ")
    next_item = head.next
    while next_item is not head:
        print(next_item, end =" ")
        next_item = next_item.next
    print('')
    print('------------------------------------')

def deep_print_list(head: Item):
    print(head.prev, '=>', head, '=>', head.next)
    next_item = head.next
    while next_item is not head:
        print(next_item.prev, '=>', next_item, '=>', next_item.next)
        next_item = next_item.next
    print('------------------------------------')


def mix_list(item_list: List[Item]):
    for item in item_list:
        #move the item according to its move_amount
        if item.move_amount > 0:
            temp = item.advance(item.move_amount)
            if temp is item:
                continue
            item.remove()
            temp.insert_after(item)
        elif item.move_amount < 0:
            temp = item.advance(item.move_amount)
            if temp is item:
                continue
            item.remove()
            temp.insert_before(item)
        else:
            #no move needed
            pass


def part1(num_list: List[int]):

    item_list, zero_item = build_linked_list(num_list)
    print_list(zero_item)

    mix_list(item_list)

    print_list(zero_item)
    i1 = zero_item.advance(1000, fullmod=True)
    i2 = zero_item.advance(2000, fullmod=True)
    i3 = zero_item.advance(3000, fullmod=True)
    print("coordinate is", i1.move_amount, i2.move_amount, i3.move_amount)
    return sum([i1.move_amount, i2.move_amount, i3.move_amount])

    
def part2(num_list: List[int]):
    dkey = 811589153

    num_list = [ n*dkey for n in num_list ]

    item_list, zero_item = build_linked_list(num_list)
    print_list(zero_item)

    for _ in range(10):
        mix_list(item_list)

    print_list(zero_item)
    i1 = zero_item.advance(1000, fullmod=True)
    i2 = zero_item.advance(2000, fullmod=True)
    i3 = zero_item.advance(3000, fullmod=True)
    print("coordinate is", i1.move_amount, i2.move_amount, i3.move_amount)
    return sum([i1.move_amount, i2.move_amount, i3.move_amount])

if __name__ == '__main__':

    # filename='day20/test.txt'
    filename='day20/input.txt'

    num_list = load_input(filename)

    # print('part 1', part1(num_list))

    print('part 2', part2(num_list))

