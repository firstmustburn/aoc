
from pprint import pprint
from collections import namedtuple

Pair = namedtuple('Pair',['start','end'])

def contains(p1, p2):
    return p1.start <= p2.start and p1.end >= p2.end

def overlaps(p1, p2):
    return (p1.start >= p2.start and p1.start <= p2.end) or (p1.end >= p2.start and p1.end <= p2.end)

def parse_assignment(astr):
    left, right = astr.split('-')
    return Pair(int(left), int(right))

def load_input(filename):
    assignment_pairs = []
    with open(filename) as infile:
        for line in infile:
            assignment_pair = tuple([ parse_assignment(a) for a in line.split(',') ])
            assert len(assignment_pair) == 2
            assignment_pairs.append(assignment_pair)
    return assignment_pairs

def part1(apairs):
    contained = []
    for apair in apairs:
        if contains(apair[0], apair[1]) or contains(apair[1], apair[0]):
            print("Contained", apair)
            contained.append(apair)
    return len(contained)

def part2(apairs):
    overlapped = []
    for apair in apairs:
        if overlaps(apair[0], apair[1]) or overlaps(apair[1], apair[0]):
            print("overlapped", apair)
            overlapped.append(apair)
    return len(overlapped)


filename="day4/test.txt"
filename="day4/input.txt"

apairs = load_input(filename)

# pprint(apairs)

# print("part 1", part1(apairs))

print("part 2", part2(apairs))

