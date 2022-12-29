from __future__ import annotations
from typing import List, Tuple

from pprint import pprint
from collections import namedtuple, defaultdict

ELF = "#"
EMPTY = "."

Point = namedtuple("Point",['x','y'])

DIR_STR = [
    "NORTH",
    "SOUTH",
    "WEST",
    "EAST"
]

class State:
    def __init__(self, elves: List[Elf]):
        self.elves = elves
        for elf in elves:
            elf.state = self
        self._update_occupation()
        self.step_count = 0
        self.last_step_move_count = None

    def _update_occupation(self):
        self.occupied = set([ e.location for e in self.elves ])

    def is_occupied(self, points: List[Point]):
        return [ p in self.occupied for p in points ]

    def step(self):
        self.step1()
        self.step2()
        self.step_count += 1

    def step1(self):
        for elf in self.elves:
            # if elf.id in [1420, 1493, 1535]: 
            # # if elf.location.x == 0 and elf.location.y >= 39 and elf.location.y <= 42:
            #     print("break")
            elf.propose_move()

    def step2(self):
        next_moves = defaultdict(list) #map of next move position to a list of the elves holding it
        for elf in self.elves:
            #skip elves that aren't moving
            if elf.next_move is None:
                continue
            #add this elf to its list
            next_moves[elf.next_move].append(elf)
        
        self.last_step_move_count = 0
        for elf_list in next_moves.values():
            if len(elf_list) == 1:
                elf_list[0].do_move()
                self.last_step_move_count += 1
            # else:                
            #     print(f'Conflicted elves moving into {elf_list[0].next_move} from {", ".join([ str(e.location) for e in elf_list ])}')
        self._update_occupation()

    def get_range(self):
        x_list = [ e.location.x for e in self.elves ]
        y_list = [ e.location.y for e in self.elves ]
        return Point(min(x_list), min(y_list)), Point(max(x_list), max(y_list))

    def draw(self, margin = 1):
        pmin, pmax = self.get_range()
        elf_points = set()
        for elf in self.elves:
            elf_points.add(elf.location)
        for y in range(pmin.y-margin, pmax.y+margin+1):
            row_str = ""
            for x in range(pmin.x-margin, pmax.x+margin+1):
                if Point(x,y) in elf_points:
                    row_str += ELF
                else:
                    row_str += EMPTY
            print(row_str)
        print("="*(pmax.x - pmin.x + 1))
        print('')


class Elf:
    #these indices are base on the order in the _make_test_points method

    TEST_LABELS=['NW','N','NE','E','SE','S','SW','W']

    NORTH_INDICES = [0,1,2]
    EAST_INDICES = [2,3,4]
    SOUTH_INDICES = [4,5,6]
    WEST_INDICES = [6,7,0]
    SEARCH_INDICES = [
        NORTH_INDICES,
        SOUTH_INDICES,
        WEST_INDICES,
        EAST_INDICES,
    ]
    NORTH_MOVE = 1
    SOUTH_MOVE = 5
    EAST_MOVE = 3
    WEST_MOVE = 7
    MOVE_INDICES = [
        NORTH_MOVE,
        SOUTH_MOVE,
        WEST_MOVE,
        EAST_MOVE,
    ]

    next_id = 0

    def __init__(self, location: Point):
        self.id = Elf.next_id
        Elf.next_id += 1
        self.state: State = None
        self.location = location      
        self.search_function_index = 0
        self.next_move = None
    
    def _make_test_points(self):
        p = self.location
        return [
            Point(p.x-1, p.y-1), #NW
            Point(p.x, p.y-1), #N
            Point(p.x+1, p.y-1), #NE
            Point(p.x+1, p.y), #E
            Point(p.x+1, p.y+1), #SE
            Point(p.x, p.y+1), #S
            Point(p.x-1, p.y+1), #SW
            Point(p.x-1, p.y), #W
        ]

    def propose_move(self):
        test_points = self._make_test_points()
        occupied = self.state.is_occupied(test_points)

        # print(f'Elf at {self.location.x},{self.location.y}:')
        # print('    test points:', ', '.join([ f'{p}={"T" if o  else "F"}' for p,o in zip(self.TEST_LABELS, occupied) ]))

        self.next_move = None
        if any(occupied):
            #propose a move
            for i in range(4):
                index = (self.search_function_index+i) % 4
                if not any([ occupied[p] for p in self.SEARCH_INDICES[index] ]):
                    #okay to move in this direction:
                    # print(f'    propose moving {DIR_STR[index]} {[ occupied[p] for p in self.SEARCH_INDICES[index] ]}')
                    self.next_move = test_points[self.MOVE_INDICES[index]]
                    break
                # print(f'    not propose moving {DIR_STR[index]} {[ occupied[p] for p in self.SEARCH_INDICES[index] ]}')
        # else:
            #no move if no neighbors    
            # print(f'    not proposing a move because no neighbors')

        # iterate the search function order
        self.search_function_index = (self.search_function_index+1) % 4
        # print(f'    next search start is {DIR_STR[self.search_function_index]}')

    
    def do_move(self):
        # print(f'Elf at {self.location} moving to {self.next_move}')
        self.location = self.next_move

    def __str__(self):
        if self.next_move is None:
            return f'E( {self.location.x},{self.location.y} -> None )'    
        return f'E( {self.location.x},{self.location.y} -> {self.next_move.x},{self.next_move.y} )'    

    def __repr__(self):
        return self.__str__()


def load_input(filename) -> List[Elf]:
    elves = []
    with open(filename) as infile:
        for y_index, line in enumerate(infile):
            for x_index, pt_val in enumerate(line.strip()):
                if pt_val == ELF:
                    elves.append(Elf(Point(x_index, y_index)))
            pass
    return elves

def empty_count(state: State):

    pmin, pmax = state.get_range()
    area = (pmax.x - pmin.x + 1) * (pmax.y - pmin.y + 1)
    #the empty spaces are all the ones not occupied by elves
    return area - len(state.elves)


def part1(elves: List[Elf]):
    s = State(elves)
    s.draw()
    for _ in range(10):
        s.step()
    
    s.draw()
    return empty_count(s)

def part2(elves: List[Elf]):
    s = State(elves)
    s.draw()
    s.step()
    while s.last_step_move_count > 0:
        s.step()

        # with open(f'outputs/day23_{s.step_count}.out', 'w') as outfile:
        #     sorted_elves = sorted([ (e.location.x, e.location.y) for e in s.elves ])
        #     for elf in sorted_elves:
        #         outfile.write(str(elf) + '\n')

        if s.step_count % 50 == 0:
            print("Completed step:", s.step_count, " with moves", s.last_step_move_count)

    print("Done stepping at", s.step_count)    
    s.draw()
    return s.step_count


def test1():

    for i in range(4):
        print("For", DIR_STR[i],
            "indices:", [ Elf.TEST_LABELS[j] for j in Elf.SEARCH_INDICES[i] ],
            "move:", Elf.TEST_LABELS[Elf.MOVE_INDICES[i]])

    elves = load_input('day23/test_sm.txt')
    s = State(elves)
    s.draw()
    for _ in range(3):
        s.step()
        s.draw()



if __name__ == '__main__':

    # filename='day23/test.txt'
    filename='day23/input.txt'

    # test1()

    elves = load_input(filename)

    # print('part 1', part1(elves))

    print('part 2', part2(elves))

