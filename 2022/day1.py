
from util import load_line_sep_groups

def part1(filename):
    elves = load_line_sep_groups(filename, int)
    # print(elves)
    elf_counts = [ sum(e) for e in elves]
    # print(elf_counts)
    return max(elf_counts)
    
def part2(filename):
    elves = load_line_sep_groups(filename, int)
    # print(elves)
    elf_counts = [ sum(e) for e in elves]
    # print(elf_counts)
    elf_counts.sort()
    # print(elf_counts)
    return sum(elf_counts[-3:])
    

if __name__ == '__main__':

    # filename="day1/test.txt"
    filename="day1/input.txt"

    print("part 1", part1(filename))

    print("part 2", part2(filename))

