
from pprint import pprint

def load_sacks(filename):
    sacks = []
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            assert len(line) % 2 == 0
            split = int(len(line)/2)
            p1 = line[:split]
            p2 = line[split:]
            sacks.append((p1,p2))
    return sacks
        


def get_priority(v):
    if v.islower():
        return ord(v) - ord('a') + 1
    else:
        return ord(v) - ord('A') + 27

def find_common(sack):
    for item in sack[0]:
        if item in sack[1]:
            return item
    raise RuntimeError(f"Nothing in commin in {sack}")

def has_item(sack, item):
    return item in sack[0] or item in sack[1]

def find_group_common(group):

    sack1 = group[0]
    for item in sack1[0] + sack1[1]:
        if has_item(group[1], item) and has_item(group[2], item):
            return item

    raise RuntimeError("No common item")

def group_sacks(sacks):
    group = []
    for sack in sacks:
        group.append(sack)
        if len(group) == 3:
            yield group
            group = []

def part1(sacks):
    priorities = []
    for sack in sacks:
        common_item = find_common(sack)
        priority = get_priority(common_item)
        # print(sack, common_item, priority)
        priorities.append(priority)
    return sum(priorities)

def part2(sacks):
    priorities = []
    for group in group_sacks(sacks):
        common_item = find_group_common(group)
        priority = get_priority(common_item)
        print(group, common_item, priority)
        priorities.append(priority)
    return sum(priorities)





# filename="day3/test.txt"
filename="day3/input.txt"

sacks = load_sacks(filename)

# print("part 1", part1(sacks))

print("part 2", part2(sacks))

