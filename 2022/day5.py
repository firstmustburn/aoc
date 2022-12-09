
from pprint import pprint
from collections import namedtuple


class Port:

    def __init__(self, columns):
        self.columns = columns

    def dump(self):
        height = max([ len(c) for c in self.columns])
        print_cols = [ (c + [' ']*height)[:len(self.columns)] for c in self.columns ]
        print_rows = []

        print('height', height)

        for h in range(height):
            for c in print_cols:
                print('c',c)
                print('h',h)
                print('c[h]', c[h])
            row = [ c[h] for c in print_cols ]
            print_rows.append(row)

        print_rows.reverse()

        for row in print_rows:
            print(' '.join([ f'[{c}]' if c != ' ' else '   ' for c in row ]))

    def make_move(self, move):
        for i in range(move.amount):
            crate = self.columns[move.from_col].pop()
            self.columns[move.to_col].append(crate)
                
def parse_stack(stack_lines):
    #remove the last stack line, then reverse them
    stack_lines = list(stack_lines)
    column_nums = stack_lines.pop()

    #compute column offsets
    num_columns = len(column_nums.strip().split())
    offsets = []
    for index in range(num_columns):
        offset = column_nums.index(str(index+1))
        offsets.append(offset)

    columns = [ [] for i in range(num_columns) ]

    #process the remaining lines in reverse order
    stack_lines.reverse()
    
    for line in stack_lines:
        for index, offset in enumerate(offsets):
            crate = line[offset]
            if crate != ' ':
                #it's a real crate, so push it on the stack
                columns[index].append(crate)
            # else empty so do nothing
        # done with all offsets
    #done with all lines

    return Port(columns)




Move = namedtuple('Move', ['amount', 'from_col', 'to_col'])

def parse_moves(move_lines):
    moves = []
    for line in move_lines:
        tokens = line.strip().split()
        move = Move(int(tokens[1]), int(tokens[3]), int(tokens[5]))
        moves.append(move)

    return moves


def load_input(filename):
    stack_lines = []
    move_lines = []
    is_stack = True
    with open(filename) as infile:
        for line in infile:
            if is_stack:
                if len(line.strip()) == 0:
                    is_stack = False
                    continue
                #add lines to the stack
                stack_lines.append(line)
            else:
                #add lines to the moves
                move_lines.append(line)
    return parse_stack(stack_lines), parse_moves(move_lines)

def part1(stack, moves):
    stack.dump()
    for move in moves:
        stack.make_move(move)
        stack.dump()

def part2(stack, moves):
    pass

filename="day5/test.txt"
# filename="day5/input.txt"

stack, moves = load_input(filename)

# pprint(stack)
# stack.dump()
# pprint(moves)

print("part 1", part1(stack, moves))

# print("part 2", part2(stack, moves))

