
from pprint import pprint
from collections import namedtuple

def load_input(filename):
    with open(filename) as infile:
        return infile.read()


def check_sequence(seq):
    #all chars unique if the length of a set is the same as the length 
    return len(set(seq)) == len(seq)

def search_stream(stream, history_len):
    history = []
    for index, c in enumerate(stream):
        history.append(c)
        if len(history) > history_len:
            history.pop(0)
            assert len(history) == history_len
            if check_sequence(history):
                return index+1
    raise RuntimeError("No start sequence")

def part1(stream):
    return search_stream(stream,4)

def part2(stream):
    return search_stream(stream,14)

if __name__ == '__main__':

    tests = [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb',7),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz',5),
        ('nppdvjthqldpwncqszvftbrmjlhg',6),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',10),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',11),
    ]

    for test in tests:
        assert part1(test[0]) == test[1]

    filename="day6/input.txt"

    seq = load_input(filename)
    
    print("part 1", part1(seq))

    tests = [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
        ('nppdvjthqldpwncqszvftbrmjlhg', 23),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26),
    ]
    for test in tests:
        assert part2(test[0]) == test[1]

    print("part 2", part2(seq))

