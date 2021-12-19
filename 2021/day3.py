import sys
from collections import namedtuple

Entry = namedtuple("Entry", ["direction","magnitude"])


with open('day3.txt') as infile:
    lines = infile.readlines()

# lines = """00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010""".split("\n")

# print(lines)

lines = [l.strip() for l in lines ]

def part1(lines):

    gamma = ""
    epsilon = ""
    place_count = len(lines[0])

    for place in range(place_count):
        values = [ l[place] for l in lines]
        ones = len([ i for i in values if i == '1'])
        zeros = len(values)-ones
        if ones > zeros:
            gamma += '1'
            epsilon += '0'
        elif zeros > ones:
            gamma += '0'
            epsilon += '1'
        else:
            raise RuntimeError("tie")
        
        print(values)
        print(ones)
        print(zeros)
    print(gamma)
    print(epsilon)
    gamma = int(gamma,2)
    epsilon = int(epsilon,2)

    print("gamma", gamma)
    print("epsilon", epsilon)
    print("gamma*epsilon", gamma*epsilon)


def filter(values, place, digit):
    if len(values) == 1:
        return values
    return [ v for v in values if v[place] == digit ]


def oxygen_filter(values, place, zeros, ones):
    if ones > zeros:
        print("ones > zeros --> take 1s")
        return filter(values, place, '1')
    elif zeros > ones:
        print("zeros > ones --> take 0s")
        return filter(values, place, '0')
    else:
        print("tie --> take 1s")
        return filter(values, place, '1')


def co2_filter(values, place, zeros, ones):
    if ones > zeros:
        print("ones > zeros --> take 0s")
        return filter(values, place, '0')
    elif zeros > ones:
        print("zeros > ones --> take 1s")
        return filter(values, place, '1')
    else:
        print("tie --> take 0s")
        return filter(values, place, '0')


def part2(lines, filter_fcn):

    place_count = len(lines[0])

    #candidates
    candidates=list(lines)

    print("candidates len", len(candidates))
    print("candidates", candidates)

    for place in range(place_count):
        values = [ l[place] for l in candidates]
        ones = len([ i for i in values if i == '1'])
        zeros = len(values)-ones
        candidates = filter_fcn(candidates, place, zeros, ones)

        print("ones, zeros", ones, zeros)
        print("candidates len", len(candidates))
        print("candidates", candidates)
        
        if len(candidates) == 0:
            break

    assert len(candidates) == 1

    return int(candidates[0],2)





# part1(lines)  #  3374136

#part 2
oxygen = part2(lines, oxygen_filter)  #  
print("---------------------------")
print("---------------------------")
co2 = part2(lines, co2_filter)  #  
print("---------------------------")
print("---------------------------")

print("oxygen", oxygen)
print("co2", co2)
print("oxygen*co2", oxygen*co2)
# 4432698
