from __future__ import annotations
from typing import List, Tuple

import math

from pprint import pprint
from collections import namedtuple

DIGIT_MAP = {
    '2':2,
    '1':1,
    '0':0,
    '-':-1,
    '=':-2,
}

SDIGIT_MAP = {
    2:'2',
    1:'1',
    0:'0',
    -1:'-',
    -2:'=',
}


def dec_to_snafu(dval: int):
    assert dval >= 0
    places_needed = 0
    total_represented = 2
    while total_represented < dval:
        places_needed += 1
        total_represented += 2*pow(5,places_needed)
        # print("total_represented is", total_represented, "for places", places_needed)

    sval = ''
    for place in range(places_needed, -1, -1):
        place_range = (int(pow(5,place)) - 1) // 2
        place_value = int(pow(5,place))
        # print("try place", place, "with range", place_range)
        for ddigit in [-2,-1,0,1,2]:
            if dval >= (ddigit * place_value) - place_range and dval <= (ddigit * place_value) + place_range:
                sdigit = SDIGIT_MAP[ddigit]
                # print(f"sdigit for place {place} is {sdigit}")
                sval += sdigit
                dval = dval - (ddigit * place_value)
                break
    assert dval == 0
    # print("Final sval is", sval)
    return sval    




def snafu_to_dec(numstr: str):
    dval = 0
    for place, sdigit in enumerate(reversed(numstr)):
        ddigit = DIGIT_MAP[sdigit]
        dval += math.pow(5,place)*ddigit
    return dval

def test():
    test_str = """        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0"""
    for tval in test_str.split('\n'):
        dval, sval = [ t.strip() for t in tval.split()]
        dval = int(dval)
        svald = snafu_to_dec(sval)
        assert dval == svald
        print(f"dval {dval} equals sval {sval}")

        new_sval = dec_to_snafu(dval)
        assert new_sval == sval


def load_input(filename) -> List[str]:
    with open(filename) as infile:
        lines = infile.readlines()
        lines = [ l.strip() for l in lines ]
    return lines

def part1(sval_list):
    dsum = 0
    for sval in sval_list:
        dval = snafu_to_dec(sval)
        print(f"sval {sval} is decimal {dval}")
        dsum += dval
    print("decimal sum is", dsum)

    ssum = dec_to_snafu(dsum)
    return ssum


def part2(sval_list):
    pass

if __name__ == '__main__':

    filename='day25/test.txt'
    filename='day25/input.txt'

    test()

    sval_list = load_input(filename)

    print('part 1', part1(sval_list))

    # print('part 2', part2(sval_list))

