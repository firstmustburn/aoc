import sys
from collections import namedtuple
import statistics

def compute_fuel_single(position, target):
    # return abs(target-position)

    # 1 2 3 4 5 6 7
    #   X       Y
    #     1 2 3 4
    n = abs(position - target)
    return n*(n + 1) / 2.0


def compute_fuel(positions, target):
    consumption = 0
    for position in positions:
        consumption += compute_fuel_single(position, target)
    return consumption

def find_min_pos(filename):
    with open(filename) as infile:
        lines = infile.readlines()
    assert len(lines) == 1

    positions = [int(p) for p in lines[0].split(',') ]

    print(statistics.mean(positions))
    print(statistics.median(positions))

    min_pos = min(positions)
    max_pos = max(positions)


    min_fuel = compute_fuel(positions, min_pos)
    min_location = min_pos
    for p in range (min_pos, max_pos+1):
        cons = compute_fuel(positions, p)
        if cons < min_fuel:
            min_fuel = cons
            min_location = p       
        print(p, cons)
    
    print(f"Minimum at {min_location}: {min_fuel}")

    



# find_min_pos("day7_test.txt")
find_min_pos("day7.txt")  

#Part 1: Minimum at 346: 359648
#Part 2: Minimum at 497: 100727924.0