
from __future__ import annotations
from typing import List, Tuple

from pprint import pprint
from collections import namedtuple

def load_input(filename) -> GasSequence:
    with open(filename) as infile:
        sequence = infile.read().strip()
    return GasSequence(sequence)

Point = namedtuple('Point',['x','y'])

class GasSequence:

    def __init__(self, sequence: str):
        self.sequence = sequence
        self.reset()

    def reset(self):
        self.index = 0
    
        self.index = 0

    def next(self) -> str:
        ret = self.sequence[self.index]
        self.index = (self.index + 1) % len(self.sequence)
        return ret

class ShapeSequence:
    grid_sequence=[
        ['@@@@'],
        ['.@.',
            '@@@',
            '.@.'],
        ['..@',
            '..@',
            '@@@'],
        ['@',
            '@',
            '@',
            '@'],
        ['@@',
            '@@'],
    ]
    def __init__(self):
        self.reset()

    def reset(self):
        self.index = 0
    
    def next(self) -> Shape:
        ret = Shape(self.grid_sequence[self.index])
        self.index = (self.index + 1) % len(self.grid_sequence)
        return ret

class Shape:
    EMPTY="."
    WALL="#"
    SHAPE_FILL="@"

    RIGHT = ">"
    LEFT = "<"
    DOWN = "v"

    def __init__(self, grid):
        self.grid = grid
        self._points = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[len(self.grid)-1-y][x] == self.SHAPE_FILL:
                    self._points.add(Point(x,y))
        self.location = None
        self.grid = None

    def place(self, location: Point, grid: Chimney):
        self.location = location
        self.grid = grid
        assert self._test_empty_location(0,0)

    def move(self, direction: str) -> bool:
        if direction == self.DOWN:
            x_offset = 0
            y_offset = -1
        elif direction == self.LEFT:
            x_offset = -1
            y_offset = 0
        elif direction == self.RIGHT:
            x_offset = 1
            y_offset = 0
        else:
            raise RuntimeError(f"Unhandled direction {direction}")

        is_empty = self._test_empty_location(x_offset,y_offset)
        if is_empty:
            self.location = Point(self.location.x + x_offset, self.location.y + y_offset)
        return is_empty

    def get_points(self, x_offset = 0, y_offset = 0):
        for point in self._points:
            yield Point(self.location.x + point.x + x_offset,
                        self.location.y + point.y + y_offset)

    def _test_empty_location(self, x_offset, y_offset):
        for point in self.get_points(x_offset, y_offset):
            if self.grid.get_valuep(point) != Shape.EMPTY:
                return False
        return True

class Chimney:
    def __init__(self, width):
        self.width = width
        self.grid = {} #map of points -> fill value
        self.y_max = -1
        self.y_min = -1

    def get_value(self, x, y):
        return self.get_valuep(Point(x,y))

    def get_valuep(self, p):
        if p.x < 0:
            return Shape.WALL
        if p.x >= self.width:
            return Shape.WALL
        if p.y < 0:
            return Shape.WALL
        try:
            return self.grid[p]
        except KeyError:
            return Shape.EMPTY

    def set_shape(self, shape: Shape, fill=Shape.SHAPE_FILL):
        for p in shape.get_points():
            self.set_valuep(p, fill)

    def set_valuep(self, p, value):
        assert p.x >= 0 and p.x < self.width
        self.grid[p] = value
        self.y_max = max(self.y_max, p.y)

    def set_value(self, x, y, value):
        self.set_valuep(Point(x,y), value)

    def get_ymax(self):
        return self.y_max

    def get_row_value(self, y):
        value = 0
        for x in range(self.width):
            if self.get_value(x,y) != Shape.EMPTY:
                value += 1 << x
        return value

    def dump(self, shapes=None, y_range=None):
        if shapes is not None:
            saved_grid = self.grid
            saved_ymax = self.y_max
            saved_ymin = self.y_min
            self.grid = dict(saved_grid)

            for shape in shapes:
                self.set_shape(shape)

        if y_range is None:
            y_range = (self.y_max, self.y_min)
        assert y_range[0] >= y_range[1]

        for y in range(y_range[0], y_range[1]-1, -1):
            print(''.join([ self.get_value(x,y) for x in range(-1, self.width+1) ]), y, self.get_row_value(y))
        print('')

        if shapes is not None:
            self.grid = saved_grid
            self.y_max = saved_ymax
            self.y_min = saved_ymin

    def forget(self):
        x_found = [ False for f in range(self.width) ]
        for y in range(self.y_max, self.y_min-1,-1):
            for x in range(self.width):
                if Point(x,y) in self.grid:
                    x_found[x] = True
            if all(x_found):
                self.y_min = y
                break
        if all(x_found):
            to_forget = [ p for p in self.grid.keys() if p.y < self.y_min ]
            for point in to_forget:
                del self.grid[point]
            # print(f"forgot {len(to_forget)} points")

class Simulation:

    def __init__(self, gas_sequence:GasSequence, chimney_width: int):
        self.gas_sequence = gas_sequence
        self.total_part_count = 0

        self.shapes = ShapeSequence()
        self.chimney = Chimney(chimney_width)

    def simulate(self, part_count):
        self.total_part_count += part_count
        # print(f"Dropping {part_count} shapes")

        for shape_index in range(part_count):
            shape = self.shapes.next()
            shape_seq_index = self.shapes.index
            shape.place(Point(2, self.chimney.get_ymax()+4), self.chimney)
            # self.chimney.dump([shape])

            gas_indices = []
            while 1:
                #gas drift
                direction = self.gas_sequence.next()
                gas_indices.append(self.gas_sequence.index)
                shape.move(direction)
                # self.chimney.dump([shape])
                #fall down
                did_fall = shape.move(Shape.DOWN)
                # self.chimney.dump([shape])
                if not did_fall:
                    self.chimney.set_shape(shape, Shape.WALL)
                    # self.chimney.dump()
                    break

            # if shape_seq_index== 1:
            #     print("shape index", shape_seq_index, "gas indices", gas_indices)

            # print(f'y_max after shape {self.total_part_count} is {self.chimney.y_max}')





class PatternSearch:
    """Don't re-use this with sequences from a different chimney"""
    def __init__(self, chimney: Chimney, num_matches:int = 3):
        self.chimney = chimney
        self.min_pattern_length = 2
        self.num_matches = num_matches
        self.pattern = None
        self.prefix = None

    def _make_seq(self):
        number_seq = []
        for y in range(self.chimney.y_min+1, self.chimney.y_max+1):
            number_seq.append(self.chimney.get_row_value(y))
        return number_seq

    def _try_pattern(self, number_seq, prefix_len, pattern_len):
        try:
            for offset_value in range(pattern_len):
                pattern_offset = prefix_len + offset_value
                ref_value = number_seq[pattern_offset]
                for i in (1,self.num_matches+1):
                    print(ref_value, number_seq[pattern_offset + i * pattern_len])
                    TODO START HERE, DEBUG WHY 3 16s match
                    if ref_value != number_seq[pattern_offset + i * pattern_len]:
                        return False
            return True
        except IndexError:
            return False

    def count_patterns(self):
        assert self.pattern is not None
        assert self.prefix is not None
        number_seq = self._make_seq()
        prefix_len = len(self.prefix)
        pattern_len = len(self.pattern)
        assert number_seq[:prefix_len] == self.prefix
        offset = prefix_len
        pattern_count = 0
        while offset + pattern_len < len(number_seq):
            if number_seq[offset:offset+pattern_len] == self.pattern:
                pattern_count += 1
                offset += pattern_len
            else:
                #no point in counting once the pattern is broken
                break
        # print(f"suffix after {pattern_count} patterns is {number_seq[offset:]}")
        return pattern_count

        # pattern_count = int((len(number_seq) - prefix_len)/pattern_len)
        # for i in range(pattern_count):
        #     print(number_seq[prefix_len+i*pattern_len : prefix_len+(i+1)*pattern_len])
        #     print(self.pattern)
        #     assert number_seq[prefix_len+i*pattern_len : prefix_len+(i+1)*pattern_len  ] == self.pattern
        # return pattern_count

    def ends_in_pattern(self):
        assert self.pattern is not None
        assert self.prefix is not None
        number_seq = self._make_seq()
        return number_seq[-len(self.pattern)] == self.pattern

    def find_pattern(self):
        assert self.pattern is None
        assert self.prefix is None
        number_seq = self._make_seq()
        for prefix_len in range(len(number_seq)):
            max_pattern_length = int((len(number_seq)-prefix_len)/self.num_matches)+1
            for pattern_len in range(self.min_pattern_length, max_pattern_length):
                if self._try_pattern(number_seq, prefix_len, pattern_len):
                    self.prefix = number_seq[:prefix_len]
                    self.pattern = number_seq[prefix_len:pattern_len+prefix_len]
                    return True
        return False

def part1(gas_sequence: GasSequence):
    part_count = 2022
    chimney_width = 7

    sim = Simulation(gas_sequence, chimney_width)
    sim.simulate(part_count)
    sim.chimney.dump()

    return sim.chimney.y_max+1 # (because of 0 indexing)

def part2(gas_sequence: GasSequence):

    target_part_count = 1000000000000
    chimney_width = 7

    sim = Simulation(gas_sequence, chimney_width)
    pattern_search = PatternSearch(sim.chimney)
    found_pattern = False

    sim.simulate(5)
    while not found_pattern:
        sim.simulate(1)
        found_pattern = pattern_search.find_pattern()
    
    #found pattern
    pattern_count = pattern_search.count_patterns()
    print("prefix len=", len(pattern_search.prefix), "value=", pattern_search.prefix)
    print("pattern len=", len(pattern_search.pattern), "value=", pattern_search.pattern)
    print("pattern_count", pattern_count)
    print("part count", sim.total_part_count)

    #run sim until we get another pattern completed
    while pattern_count == pattern_search.count_patterns():
        sim.simulate(1)

    pattern_count = pattern_search.count_patterns()
    pattern_part_len = 0
    while pattern_count == pattern_search.count_patterns():
        sim.simulate(1)
        pattern_part_len += 1

    print("Number of parts in pattern are: ", pattern_part_len)

    # sim.simulate(pattern_part_len)

    print(f'after another {pattern_part_len}, num patterns is {pattern_search.count_patterns()}')

    num_repeats = int((target_part_count - sim.total_part_count) / pattern_part_len)
    repeated_part_count = num_repeats * pattern_part_len
    repeated_lines = num_repeats * len(pattern_search.pattern)
    print("num_repeats",num_repeats)
    print("repeated_part_count",repeated_part_count)
    print("repeated_lines",repeated_lines)

    remaining_part_count = target_part_count - sim.total_part_count - repeated_part_count
    print("remaining_part_count",remaining_part_count)

    #simulate the remaining parts
    sim.simulate(remaining_part_count)

    #final line count
    final_line_count = sim.chimney.y_max + repeated_lines
    print("final sequence", pattern_search._make_seq())
    print("final_line_count", final_line_count)


    return final_line_count + 1 # +1 for line offset

if __name__ == '__main__':

    # filename='day17/test.txt'
    filename='day17/input.txt'

    gas_sequence = load_input(filename)

    # print('part 1', part1(gas_sequence))

    print('part 2', part2(gas_sequence))

