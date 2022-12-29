from __future__ import annotations
from typing import List, Dict

from pprint import pprint
from collections import namedtuple

Point = namedtuple("Point",['x','y'])

WALL = '#'
EMPTY = '.'

WAIT = Point(0,0)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
UP = Point(0, -1)
LEFT = Point(-1, 0)

DEBUG=False


DIRECTION_STRING_MAP = {
    '>': RIGHT,
    '<': LEFT,
    'v': DOWN,
    '^': UP,
}
DIRECTION_POINT_MAP = {
    RIGHT : '>',
    LEFT : '<',
    DOWN : 'v',
    UP : '^',
}

# class Node:
#     def __init__(self, parent: Node, location: Point):
#         self.parent = parent
#         self.location = location

#     def get_path(self):
#         if self.parent is None:
#             return [self]
#         else:
#             p = self.parent.get_path()
#             p.append(self)
#             return p

#     def __str__(self):
#         return f'N({self.location.x},{self.location.y})'
#     def __repr__(self):
#         return self.__str__()

class Grid:
    """Grid has the top-left corner at 0,0 with +x to the right and +y down.
    So the start is at (something, -1) and the end is at (something, height)"""

    def __init__(self, width: int, height: int, start: Point, end:Point, blizzards: Dict[Point, Point]):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        #convert single blizzard map into a map to lists
        self.blizzards: Dict[Point,List[Point]] = { pt: [dir] for pt, dir in blizzards.items()}
        self.initial_blizzards = dict(blizzards)

    def advance_blizzards(self):
        new_blizzards = {}
        for loc, dir_list in self.blizzards.items():
            for dir in dir_list:
                new_pt = Point(
                    (loc.x + dir.x) % self.width,
                    (loc.y + dir.y) % self.height)
                if new_pt not in new_blizzards:
                    new_blizzards[new_pt] = []
                new_blizzards[new_pt].append(dir)
        self.blizzards = new_blizzards

    DIRECTIONS = [DOWN, RIGHT, WAIT, UP, LEFT]
    def get_neighbors(self, pt: Point):
        return [ Point(pt.x + d.x, pt.y + d.y) for d in self.DIRECTIONS ] 

    def is_free(self, loc: Point) -> bool:
        return (((loc not in self.blizzards) 
                and (loc.x >= 0 and loc.x < self.width)
                and (loc.y >= 0 and loc.y < self.height)) 
                or (loc == self.start) or (loc == self.end))

    def find_waypoints(self, waypoints:List[Point]) -> int:
        total_steps = 0
        for start, end in zip(waypoints[:-1], waypoints[1:]):
            print(f"Searching from {start} to {end}")
            steps = self._find_path(start, end)
            print(f"Reached from {start} to {end} in {steps} steps")
            total_steps += steps
        return total_steps

    def _find_path(self, start_loc:Point, end_loc: Point) -> int:
        #build a graph of nodes that are reachable from any particular node

        current_generation_locations = set([start_loc])
        step_count = 0
        while True:
            step_count += 1
            self.advance_blizzards()

            if step_count % 20 == 0:
                print(f"At step {step_count} with {len(current_generation_locations)} possible locations")
            if DEBUG:
                self.draw()

            next_generation_locations = set()
            for cloc in current_generation_locations:     
                for nloc in self.get_neighbors(cloc):
                    if nloc == end_loc:
                        print(f"Found path after {step_count} steps")
                        return step_count
                    if self.is_free(nloc):
                        next_generation_locations.add(nloc)
            if len(next_generation_locations) == 0:
                grid.draw()
                print(f"At location {cloc}, no place to go")
                assert len(next_generation_locations) > 0
            current_generation_locations = next_generation_locations

    def make_border(self, pt: Point) -> str:
        return ''.join([ EMPTY if x == pt.x + 1 else WALL for x in range(self.width + 2)])

    def draw(self):
        print(self.make_border(self.start))
        for y in range(self.height):
            row_str = '#'
            for x in range(self.width):
                try:
                    dir_list = self.blizzards[Point(x,y)]
                    if len(dir_list) == 1:
                        row_str += DIRECTION_POINT_MAP[dir_list[0]]
                    else:
                        row_str += str(len(dir_list))
                except KeyError:
                    row_str += EMPTY
            row_str += "#"
            print(row_str)
        print(self.make_border(self.end))
        print('')
        print('')

def load_input(filename):
    with open(filename) as infile:
        lines = infile.readlines()
    lines = [ l.strip() for l in lines ]
    width = len(lines[0]) - 2
    height = len(lines) - 2

    start = Point(lines[0].index(EMPTY) - 1, -1)
    end = Point(lines[-1].index(EMPTY) - 1, height)

    blizzards = {}
    for y_offset, line in enumerate(lines[1:-1]):
        for x_offset, value in enumerate(line[1:-1]):
            if value == EMPTY:
                continue
            blizzards[Point(x_offset, y_offset)] = DIRECTION_STRING_MAP[value]
    return Grid(width, height, start, end, blizzards)

def part1(grid: Grid):
    step_count = grid.find_waypoints([grid.start, grid.end])

    return step_count

def part2(grid):
    step_count = grid.find_waypoints([grid.start, grid.end, grid.start, grid.end])

    return step_count

if __name__ == '__main__':

    # filename='day24/test.txt'
    filename='day24/input.txt'

    grid = load_input(filename)

    # print('part 1', part1(grid))

    print('part 2', part2(grid))

