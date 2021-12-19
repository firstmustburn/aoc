import sys
from collections import namedtuple

Entry = namedtuple("Entry", ["direction","magnitude"])

UP_DIR = "up"
DOWN_DIR = "down"
FORWARD_DIR = "forward"
directions = [UP_DIR, DOWN_DIR, FORWARD_DIR]


entries = []
with open('day2.txt') as infile:
    lines = infile.readlines()

# lines = """forward 5
# down 5
# forward 8
# up 3
# down 8
# forward 2""".split("\n")

# print(lines)

for line in lines:
    direction, magnitude = line.split(" ")
    magitude = int(magnitude)
    assert direction in directions
    entries.append(Entry(direction, magitude))

# for entry in entries:
#     print(entry)


def simple_dir(entries):
    vpos = 0
    hpos = 0

    for entry in entries:
        if entry.direction == UP_DIR:
            hpos -= entry.magnitude
        elif entry.direction == DOWN_DIR:
            hpos += entry.magnitude
        elif entry.direction == FORWARD_DIR:
            vpos += entry.magnitude
        else:
            raise RuntimeError(f"Unknown direction {entry}")

    print("Result:")
    print("hpos", hpos)
    print("vpos", vpos)
    print("hpos*vpos", hpos*vpos)  #1459206 

def complex_dir(entries):
    vpos = 0
    hpos = 0
    aim = 0

    for entry in entries:
        if entry.direction == UP_DIR:
            aim -= entry.magnitude
        elif entry.direction == DOWN_DIR:
            aim += entry.magnitude
        elif entry.direction == FORWARD_DIR:
            hpos += entry.magnitude
            vpos += entry.magnitude*aim
        else:
            raise RuntimeError(f"Unknown direction {entry}")

    print("Result:")
    print("hpos", hpos)
    print("vpos", vpos)
    print("hpos*vpos", hpos*vpos)  



simple_dir(entries)  #1459206 
complex_dir(entries)  # 1320534480 
