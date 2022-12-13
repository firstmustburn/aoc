
from pprint import pprint
from collections import namedtuple
import functools

Pair = namedtuple('Pair', ['left', 'right'])

IN_ORDER = 1
OUT_OF_ORDER = -1
EQUAL_ORDER = 0


def compare_pairs(left, right):
    if isinstance(left, list) and isinstance(right, list):
        return compare_list_pairs(left, right)
    elif isinstance(left, int) and isinstance(right, int):
        return compare_integer_pairs(left,right)
    elif isinstance(left, int) and isinstance(right, list):
        #wrap int in list
        return compare_list_pairs([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        #wrap int in list
        return compare_list_pairs(left, [right])
    else:
        raise RuntimeError(f'Unhandled case for left={left} and right={right}')

def compare_integer_pairs(left,right):
    if left < right:
        return IN_ORDER
    elif left > right:
        return OUT_OF_ORDER
    else:
        return EQUAL_ORDER

def compare_list_pairs(left,right):
    #compare elements over the common part of the length of the list
    for index in range(min([len(left), len(right)])):
        compval = compare_pairs(left[index], right[index])
        if compval != EQUAL_ORDER:
            return compval
    #if we get here, all common list elements compared equal
    if len(left) < len(right):
        return IN_ORDER
    elif len(left) > len(right):
        return OUT_OF_ORDER
    else:
        return EQUAL_ORDER

def parse_pair(lines):
    left = eval(lines[0])
    right = eval(lines[1])
    if len(lines) > 2:
        assert len(lines[2].strip()) == 0
    return Pair(left,right)

def load_input(filename):
    pairs = []
    with open(filename) as infile:
        lines = infile.readlines()
        for i in range(int((len(lines)+1)/3)):
            pair_lines = lines[i*3:(i*3)+3]
            pairs.append(parse_pair(pair_lines))
    return pairs

def part1(pairs):
    right_order_indices = []
    for index, pair in enumerate(pairs):
        compval = compare_pairs(pair.left, pair.right)
        if compval == IN_ORDER:
            right_order_indices.append(index+1) #because the indices are 1-indexed
    print("Pairs in order: ", right_order_indices)
    return sum(right_order_indices)

def part2(pairs):
    packets = []
    for pair in pairs:
        packets.extend([pair.left, pair.right])
    divider1 = eval('[[2]]')
    packets.append(divider1)
    divider2 = eval('[[6]]')
    packets.append(divider2)
    
    packets = sorted(packets, key=functools.cmp_to_key(compare_pairs), reverse=True)
    
    for packet in packets:
        print(packet)

    decoder_key = (packets.index(divider1) + 1) * (packets.index(divider2) + 1)
    return decoder_key

if __name__ == '__main__':

    # filename='day13/test.txt'
    filename='day13/input.txt'

    pairs = load_input(filename)

    # print('part 1', part1(pairs))

    print('part 2', part2(pairs))

