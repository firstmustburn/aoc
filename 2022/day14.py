
from pprint import pprint
from collections import namedtuple, defaultdict

Point = namedtuple("Point",['x','y'])

def load_input(filename):
    rock_paths = []
    with open(filename) as infile:
        for line in infile:
            rock_path = line.strip().split(' -> ')
            rock_path = [ Point(*[ int(v) for v in p.split(',')]) for p in rock_path ]
            rock_paths.append(rock_path)

    return rock_paths

EMPTY = '.'
SAND = 'o'
ROCK = '#'

class Grid:

    def __init__(self, rock_paths):
        self.grid = {}
        self.rock_paths = rock_paths

        self._fill_paths()
    
    def _fill_paths(self):
        for path in self.rock_paths:
            #take the points in the path pairwise
            for start, end in zip(path[:-1], path[1:]):
                #fill the line from start to end
                if start.x == end.x:
                    ymin = min(start.y, end.y)
                    ymax = max(start.y, end.y)
                    for y in range(ymin, ymax+1):
                        self.set_value(start.x, y, ROCK)
                elif start.y == end.y:
                    xmin = min(start.x, end.x)
                    xmax = max(start.x, end.x)
                    for x in range(xmin, xmax+1):
                        self.set_value(x, start.y, ROCK)
                else:
                    raise RuntimeError(f"Can't path from {start} to {end}")
        self.rock_min, self.rock_max = self.get_range(ROCK)

    def simulate_sand(self, origin):
        # return the point where the sand came to rest, or None if it goes lower than the lowest rock
        sand_point = origin
        while True:
            #check for abyss condition -- if the y is greater than any rock y value, then the sand will fall forever
            if sand_point.y > self.rock_max.y:
                print(f"Sand at {sand_point} will fall forever")
                return None

            down_point = Point(sand_point.x, sand_point.y+1)
            if self.get_valuep(down_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_point
                continue
            down_left_point = Point(sand_point.x-1, sand_point.y+1)
            if self.get_valuep(down_left_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_left_point
                continue
            down_right_point = Point(sand_point.x+1, sand_point.y+1)
            if self.get_valuep(down_right_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_right_point
                continue
            #if we get this far, then all the possible points are full and the sand stops
            self.set_valuep(sand_point, SAND)
            return sand_point
            
    def simulate_sand_2(self, origin):
        # return the point where the sand came to rest, or None if it cannot move from the origin point
        # assume there is an infinite rock layer at y=rock_max.y+2, so any sand that reaches rock_max.y+1 will stop there
        if self.get_valuep(origin) != EMPTY:
            self.dump()
            raise RuntimeError(f"Simulation is full for origin {origin}")

        sand_point = origin
        while True:
            #check for floor condition
            if sand_point.y == self.rock_max.y+1:
                # print(f"Sand at {sand_point} reached the floor")
                self.set_valuep(sand_point, SAND)
                return sand_point

            down_point = Point(sand_point.x, sand_point.y+1)
            if self.get_valuep(down_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_point
                continue
            down_left_point = Point(sand_point.x-1, sand_point.y+1)
            if self.get_valuep(down_left_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_left_point
                continue
            down_right_point = Point(sand_point.x+1, sand_point.y+1)
            if self.get_valuep(down_right_point) == EMPTY:
                #move the sand to empty point
                sand_point = down_right_point
                continue
            #if we get this far, then all the possible points are full and the sand stops
            self.set_valuep(sand_point, SAND)
            return sand_point
            
    def get_range(self, filter_value=None):
        x_list = []
        y_list = []
        for point, value in self.grid.items():
            if filter_value is None or filter_value == value:
                x_list.append(point.x)
                y_list.append(point.y)
        p_min = Point(min(x_list), min(y_list))
        p_max = Point(max(x_list), max(y_list))
        return p_min, p_max

    def dump(self):
        p_min, p_max = self.get_range()
        for y in range(p_min.y, p_max.y+1):
            row = [ self.grid.get(Point(x,y), EMPTY) for x in range(p_min.x, p_max.x + 1) ]
            print(''.join(row))
        print("")

    def set_value(self, x, y, value):
        self.set_valuep(Point(x,y), value)

    def set_valuep(self, point, value):
        self.grid[point] = value

    def get_valuep(self, point):
        try:
            return self.grid[point]
        except KeyError:
            return EMPTY

    def get_value(self, x, y):
        return self.get_valuep(Point(x,y))

def part1(rock_paths):
    g = Grid(rock_paths)
    print(g.get_range())
    g.dump()
    while True:
        settle_point = g.simulate_sand(Point(500,0))
        if settle_point is None:
            break
        print("Sand settled at", settle_point)

    g.dump()
    #count the sand
    return sum([ 1 for v in g.grid.values() if v == SAND ])

def part2(rock_paths):
    g = Grid(rock_paths)
    print(g.get_range())
    g.dump()
    while True:
        origin = Point(500,0)
        settle_point = g.simulate_sand_2(origin)
        if settle_point== origin:
            break
        # print("Sand settled at", settle_point)

    g.dump()
    #count the sand
    return sum([ 1 for v in g.grid.values() if v == SAND ])


if __name__ == '__main__':

    filename='day14/test.txt'
    filename='day14/input.txt'

    rock_paths = load_input(filename)

    # pprint(rock_paths)

    # print('part 1', part1(rock_paths))

    print('part 2', part2(rock_paths))

