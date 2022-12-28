from __future__ import annotations
from typing import List, Dict, Union, Tuple

import re

from pprint import pprint
from collections import namedtuple

#  Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

RIGHT_TURN = 'R'
LEFT_TURN = 'L'

WALL='#'
FREE='.'
EMPTY=' '



TURN_TABLE = {
    (RIGHT, RIGHT_TURN): DOWN,
    (RIGHT, LEFT_TURN): UP,
    (LEFT, RIGHT_TURN): UP,
    (LEFT, LEFT_TURN): DOWN,
    (UP, RIGHT_TURN): RIGHT,
    (UP, LEFT_TURN): LEFT,
    (DOWN, RIGHT_TURN): LEFT,
    (DOWN, LEFT_TURN): RIGHT,
}

#opposite values for each index: RIGHT, DOWN, LEFT, UP
OPPOSITE_DIRECTION = [LEFT, UP, RIGHT, DOWN]

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
DIR_CHAR = ['>', 'v', '<', "^"]


Coord = namedtuple("Coord", ['r', 'c'])

Turn = namedtuple("Turn", ['direction'])
Move = namedtuple("Move", ['distance'])

def parse_moves(move_str):
    moves = []
    tokens = re.split(r'([RL])',move_str)
    for token in tokens:
        if token in [RIGHT_TURN, LEFT_TURN]:
            moves.append(Turn(token))
        else:
            moves.append(Move(int(token)))
    return moves

def move(coord: Coord, direction: int, amount: int = 1):
    if direction == RIGHT:
        return Coord(coord.r, coord.c + amount)
    elif direction == LEFT:
        return Coord(coord.r, coord.c - amount)
    elif direction == UP:
        #note that up is minus / smaller rows
        return Coord(coord.r - amount, coord.c)
    elif direction == DOWN:
        return Coord(coord.r + amount, coord.c)
    else:
        raise RuntimeError(f'Unhandled direction {direction}')

class Cell:

    def __init__(self, coord: Coord, value: str):
        self.coord = coord
        self.value = value
        self.neighbors = [ None for _ in range(4) ]
        self.neighbor_directions = [ None for _ in range(4) ]

    def __str__(self):
        return f'{self.coord.r},{self.coord.c}->{self.value}'

    def __repr__(self):
        return self.__str__()

class Part2WrapperA:


    def stitch(self, cl1: List[Coord], cl2: List[Coord], dir1: int, dir2: int):
        for c1, c2 in zip(cl1, cl2):
            # print(f'{c1}, {DIR_CHAR[dir1]} -> {c2}')
            # print(f'{c2}, {DIR_CHAR[dir2]} -> {c1}')
            self.edge_map[(c1, dir1)] = c2, OPPOSITE_DIRECTION[dir2]
            self.edge_map[(c2, dir2)] = c1, OPPOSITE_DIRECTION[dir1]
        # print('---------------------------------------')

    def __init__(self, grid: Grid):
        self.grid = grid
        self.face_size = self.grid.col_count // 4
        assert self.face_size * 3 == self.grid.row_count

        #face boundary numbers
        f0 = 0
        f1 = self.face_size * 1
        f2 = self.face_size * 2
        f3 = self.face_size * 3
        f4 = self.face_size * 4
        
        self.edge_map: Dict[Tuple[Coord, int], Coord] = {} #mapping of a cell and direction to its matching cell

        #map each of the cube edges
        # 1-4, 2-3, 3-4, 4-5, and 5-6 match up on the existing map
        # special handilng for those don't match up on the map
        # 1-3 edge
        top3 = [ Coord(f1,c) for c in range(f1,f2) ]
        left1 =  [ Coord(r,f2) for r in range(f0,f1) ]
        self.stitch(top3, left1, UP, LEFT)        
        # 1-2 edge
        top2 = reversed([ Coord(f1,c) for c in range(f0,f1) ])  
        top1 =  [ Coord(f0,c) for c in range(f2,f3) ]
        self.stitch(top2, top1, UP, UP)        
        # 3-5 edge
        bottom3 = [ Coord(f2-1,c) for c in range(f1,f2) ]
        left5 =  reversed([ Coord(r,f2) for r in range(f2,f3) ])
        self.stitch(bottom3, left5, DOWN, LEFT)
        # 2-5 edge
        bottom2 = reversed([ Coord(f2-1,c) for c in range(f0,f1) ])
        bottom5 =  [ Coord(f3-1,c) for c in range(f2,f3) ]
        self.stitch(bottom2, bottom5, DOWN, DOWN)
        # 4-6 edge
        right4 = [ Coord(r,f3-1) for r in range(f1,f2) ]
        top6 =  reversed([ Coord(f2,c) for c in range(f3,f4) ])
        self.stitch(right4, top6, RIGHT, UP)
        # 1-6 edge
        right6 = [ Coord(r,f4-1) for r in range(f2,f3) ]
        right1 =  reversed([ Coord(r,f3-1) for r in range(f0,f1) ])
        self.stitch(right6, right1, RIGHT, RIGHT)      
        # 2-6 edge
        bottom6 = reversed([ Coord(f3-1,c) for c in range(f3,f4) ])
        left2 =  [ Coord(r,f0) for r in range(f1,f2) ]
        self.stitch(bottom6, left2, DOWN, LEFT)
        #12 edges total

    def wrap(self, cell: Cell, dir: int) -> Tuple(Cell, int):
        next_coord, new_dir = self.edge_map[(cell.coord, dir)]
        return self.grid.cells[next_coord], new_dir    

class Part2WrapperB:

    def stitch(self, cl1: List[Coord], cl2: List[Coord], dir1: int, dir2: int):
        for c1, c2 in zip(cl1, cl2):
            # print(f'{c1}, {DIR_CHAR[dir1]} -> {c2}')
            # print(f'{c2}, {DIR_CHAR[dir2]} -> {c1}')
            self.edge_map[(c1, dir1)] = c2, OPPOSITE_DIRECTION[dir2]
            self.edge_map[(c2, dir2)] = c1, OPPOSITE_DIRECTION[dir1]
        # print('---------------------------------------')

    def __init__(self, grid: Grid):
        self.grid = grid
        self.face_size = self.grid.col_count // 3
        assert self.face_size * 4 == self.grid.row_count

        #face boundary numbers
        f0 = 0
        f1 = self.face_size * 1
        f2 = self.face_size * 2
        f3 = self.face_size * 3
        f4 = self.face_size * 4
        
        self.edge_map: Dict[Tuple[Coord, int], Coord] = {} #mapping of a cell and direction to its matching cell

        #map each of the cube edges
        # 1-2, 2-3, 3-4, 4-5, 5-6 match up on the existing map
        # special handilng for those don't match up on the map
        # 1-3 edge
        right3 = [ Coord(r,f2-1) for r in range(f1,f2) ]
        bottom1 =  [ Coord(f1-1,c) for c in range(f2,f3) ]
        self.stitch(right3, bottom1, RIGHT, DOWN)
        # 4-6 edge
        right6 = [ Coord(r,f1-1) for r in range(f3,f4) ]
        bottom4 =  [ Coord(f3-1,c) for c in range(f1,f2) ]
        self.stitch(right6, bottom4, RIGHT, DOWN)
        # 3-5 edge
        left3 = [ Coord(r,f1) for r in range(f1,f2) ]
        top5 =  [ Coord(f2,c) for c in range(f0,f1) ]
        self.stitch(left3, top5, LEFT, UP)
        # 5-2 edge
        left5 = [ Coord(r,f0) for r in range(f2,f3) ]
        left2 = reversed([ Coord(r,f1) for r in range(f0,f1) ])
        self.stitch(left5, left2, LEFT, LEFT)
        # 1-4 edge
        right1 = [ Coord(r,f3-1) for r in range(f0,f1) ]
        right4 = reversed([ Coord(r,f2-1) for r in range(f2,f3) ])
        self.stitch(right1, right4, RIGHT, RIGHT)
        # 6-2 edge
        left6 = [ Coord(r,f0) for r in range(f3,f4) ]
        top2 =  [ Coord(f0,c) for c in range(f1,f2) ]
        self.stitch(left6, top2, LEFT, UP)
        # 1-6 edge
        top1 =  [ Coord(f0,c) for c in range(f2,f3) ]
        bottom6 =  [ Coord(f4-1,c) for c in range(f0,f1) ]
        self.stitch(top1, bottom6, UP, DOWN)


    def wrap(self, cell: Cell, dir: int) -> Tuple(Cell, int):
        next_coord, new_dir = self.edge_map[(cell.coord, dir)]
        return self.grid.cells[next_coord], new_dir    


class Part1Wrapper:
    def __init__(self, grid):
        self.grid = grid

    def _first_occupied_in_row(self, row):
        for col in range(self.grid.col_count):
            try:
                return self.grid.cells[Coord(row, col)]
            except KeyError:
                pass
        raise RuntimeError("Expected to find an occupied cell")

    def _last_occupied_in_row(self, row):
        for col in range(self.grid.col_count-1, -1, -1):
            try:
                return self.grid.cells[Coord(row, col)]
            except KeyError:
                pass
        raise RuntimeError("Expected to find an occupied cell")

    def _first_occupied_in_col(self, col):
        for row in range(self.grid.row_count):
            try:
                return self.grid.cells[Coord(row, col)]
            except KeyError:
                pass
        raise RuntimeError("Expected to find an occupied cell")

    def _last_occupied_in_col(self, col):
        for row in range(self.grid.row_count-1, -1, -1):
            try:
                return self.grid.cells[Coord(row, col)]
            except KeyError:
                pass
        raise RuntimeError("Expected to find an occupied cell")

    def wrap(self, cell: Cell, dir: int) -> Tuple(Cell, int):
        if dir == RIGHT:
            return self._first_occupied_in_row(cell.coord.r), RIGHT
        elif dir == LEFT:
            return self._last_occupied_in_row(cell.coord.r), LEFT
        elif dir == DOWN:
            return self._first_occupied_in_col(cell.coord.c), DOWN
        elif dir == UP:
            return self._last_occupied_in_col(cell.coord.c), UP
        else:
            raise RuntimeError("unhandled direction")

class Grid:

    def _parse_cells(self):
        self.row_count = 0
        self.col_count = 0
        self.cells: Dict[Coord, Cell] = {} #map of (row, col) -> cell 
        for row_ind, row in enumerate(self.lines):
            for col_ind, value in enumerate(row):
                if value != EMPTY:
                    assert value in [WALL, FREE]
                    coord = Coord(row_ind, col_ind)
                    self.cells[coord] = Cell(coord, value)
                    self.row_count = max(self.row_count, row_ind+1)
                    self.col_count = max(self.col_count, col_ind+1)

    def _wrap_cells(self):
        #now compute neighbors
        for cell in self.cells.values():
            for dir in DIRECTIONS:
                ncell_coord = move(cell.coord, dir)
                if ncell_coord in self.cells:
                    cell.neighbors[dir] = self.cells[ncell_coord]
                    #when the cell already exists, the direction stays the same
                    cell.neighbor_directions[dir] = dir
                else:
                    #no immediate neighbor, so find the wrap neighbor
                    #and the new direction for the neighbor
                    cell.neighbors[dir], cell.neighbor_directions[dir] = self.wrapper.wrap(cell, dir)

        for cell in self.cells.values():
            assert cell.value in [FREE, WALL]
            assert len(cell.neighbors) == len(DIRECTIONS)
            for dir in DIRECTIONS:
                assert isinstance(cell.neighbors[dir], Cell)
                assert isinstance(cell.neighbor_directions[dir], int)
                assert cell.neighbor_directions[dir] >= 0 and cell.neighbor_directions[dir] < 4

    def __init__(self, lines: List[str], wrapper_class):
        self.lines = lines
        self._parse_cells()
        self.wrapper = wrapper_class(self)
        self._wrap_cells()

    def dump(self, move_history = None):
        if move_history is None:
            move_history = {}
        for row in range(self.row_count):
            row_str = ''
            for col in range(self.col_count):
                coord = Coord(row, col)
                if coord in move_history:
                    #draw value from history
                    row_str += move_history[coord]
                else:
                    #draw value from grid
                    try:
                        row_str += self.cells[coord].value
                    except:
                        row_str += EMPTY
            print(row_str)
        print("===================================")

def execute_moves(grid: Grid, start_coord: Coord, start_dir: int, move_list: List[Union[Move, Turn]]) -> Tuple(Coord, int):
    current_location: Cell = grid.cells[start_coord]
    current_direction = start_dir
    history = {start_coord:DIR_CHAR[start_dir]}

    for move in move_list:
        if isinstance(move, Turn):
            #look up the new direction based on our current direction and the move
            current_direction = TURN_TABLE[(current_direction, move.direction)]
            history[current_location.coord] = DIR_CHAR[current_direction]
        elif isinstance(move, Move):
            for _ in range(move.distance):
                next_cell = current_location.neighbors[current_direction]
                next_direction = current_location.neighbor_directions[current_direction]
                if next_cell.value == WALL:
                    break
                current_location = next_cell
                current_direction = next_direction
                history[current_location.coord] = DIR_CHAR[current_direction]
        else:
            raise RuntimeError("Unhandled move type")

        # print("Move:", move)
        # grid.dump(history)
        # print("current Location", current_location.coord, 'Current direction', DIR_CHAR[current_direction])
        # print('')

    grid.dump(history)
    return current_location, current_direction

def find_start_coord(grid):
    for col in range(grid.col_count):
        try:
            coord = Coord(0, col)
            if grid.cells[coord].value == FREE:
                return coord
        except KeyError:
            pass
    raise RuntimeError("Expected to find a free cell")



def load_input(filename, wrapper_class):
    grid_lines = []
    with open(filename) as infile:
        lines = infile.readlines()
        lines = [ l.strip('\n') for l in lines ]
    grid_lines = lines[:-2]
    moves = lines[-1]

    move_list = parse_moves(moves)
    grid = Grid(grid_lines, wrapper_class)

    return move_list, grid

def part1(filename):
    move_list, grid = load_input(filename, Part1Wrapper)

    print(move_list)
    grid.dump()

    start_coord = find_start_coord(grid)
    start_dir = RIGHT

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)
    return (final_cell.coord.r+1)*1000 + (final_cell.coord.c+1) * 4 + final_dir

def part2(filename):
    move_list, grid = load_input(filename, Part2WrapperB)

    print(move_list)
    grid.dump()

    start_coord = find_start_coord(grid)
    start_dir = RIGHT

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)
    return (final_cell.coord.r+1)*1000 + (final_cell.coord.c+1) * 4 + final_dir

def test():
    filename = "day22/test2.txt"
    move_list, grid = load_input(filename, Part2WrapperA)

    print(move_list)
    grid.dump()

    start_coord = Coord(4,0)
    start_dir = RIGHT

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)

    filename = "day22/test2.txt"
    move_list, grid = load_input(filename, Part2WrapperA)

    print(move_list)
    grid.dump()

    start_coord = Coord(0,11)
    start_dir = DOWN

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)


def test2():
    filename = "day22/test3.txt"
    move_list, grid = load_input(filename, Part2WrapperB)

    print(move_list)
    grid.dump()

    start_coord = Coord(50,50)
    start_dir = RIGHT

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)

    filename = "day22/test3.txt"
    move_list, grid = load_input(filename, Part2WrapperB)

    print(move_list)
    grid.dump()

    start_coord = Coord(50,99)
    start_dir = DOWN

    final_cell, final_dir = execute_moves(grid, start_coord, start_dir, move_list)



if __name__ == '__main__':

    filename='day22/test.txt'
    filename='day22/input.txt'

    # test2()

    # print('part 1', part1(filename))

    print('part 2', part2(filename))













#     22221111
#     22221111
#     22221111
#     22221111
#     3333
#     3333
#     3333
#     3333
# 55554444
# 55554444
# 55554444
# 55554444
# 6666
# 6666
# 6666
# 6666






#         1111
#         1111
#         1111
#         1111
#     33332222
#     33332222
#     33332222
#     33332222
#     4444
#     4444
#     4444
#     4444
# 66665555
# 66665555
# 66665555
# 66665555


#         1111
#         1111
#         1111
#         1111
# 222233334444
# 222233334444
# 222233334444
# 222233334444
#         55556666
#         55556666
#         55556666
#         55556666