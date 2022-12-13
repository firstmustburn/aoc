
from __future__ import annotations

from typing import Dict, List, Union, Tuple

from pprint import pprint
from collections import namedtuple


Point = namedtuple("Point",['x','y'])

class HeightMap:  
    def __init__(self, start: Point, end:Point, map_data: List[List[int]]):
        self.start = start
        self.end = end
        self.data = map_data #each item is a list that represents a row

        self.x_max = len(self.data[0])
        self.y_max = len(self.data)

    def get(self, x: int, y: int):
        return self.data[y][x]
    
    def getp(self, p: Point):
        return self.get(p.x, p.y)

    def contains(self, x, y):
        return x >= 0 and x < self.x_max and y >= 0 and y < self.y_max

    def containsp(self, p: Point):
        return self.contains(p.x, p.y)

    def iterate(self) -> Tuple[Point, int]:
        for x in range(self.x_max):
            for y in range(self.y_max):
                yield Point(x,y), self.get(x,y)

    def dump(self):
        print("start", self.start)
        print("end", self.end)
        for row in self.data:
            print(' '.join([ f'{c: <2}' for c in row]))
        print("-----------------------------------")


def load_input(filename):
    map_data = [] #list of lists for map rows
    with open(filename) as infile:
        start = None
        end = None
        for y_index, line in enumerate(infile):
            if 'S' in line:
                x_index = line.index('S')
                line = line.replace('S','a')
                start = Point(x_index, y_index)
            if 'E' in line:
                x_index = line.index('E')
                line = line.replace('E','z')
                end = Point(x_index, y_index)
            row = [ ord(c) - ord('a') for c in line.strip() ]
            map_data.append(row)
    assert start is not None
    assert end is not None
    return HeightMap(start, end, map_data)

class Node:
    def __init__(self, parent: Union[Node,None], point: Point, elevation: int):
        self.parent = parent
        self.point = point
        self.elevation = elevation
        self.children = []

    def add_child(self, child: Node):
        self.children.append(child)

    def get_depth(self):
        if self.parent is not None:
            return self.parent.get_depth() + 1
        else:
            return 0

    def __str__(self):
        return f'N(x={self.point.x}, y={self.point.y}, e={self.elevation})'

class PathGraph:
    
    def __init__(self, hmap: HeightMap, initial_shortest_path_depth=None):
        self.hmap = hmap
        
        self.nodes_by_point: Dict[Point, Node] = {}
        self.shortest_path = None
        self.shortest_path_depth = initial_shortest_path_depth

        self.root = Node(None, hmap.start, hmap.getp(hmap.start))
        paths_to_generate = [[self.root]]
        while paths_to_generate:
            # generate all the paths in paths_to_generate
            # collecting the resulting new paths in additonal_paths
            additional_paths = []
            for path in paths_to_generate:
                additional_paths.extend(self._generate_graph(path))
            #on the next loop, iterate the additional paths
            paths_to_generate = additional_paths
            

    def _get_adjacent_points(self, point: Point):
        adjacent: List[Point] = []
        for delta in [1,-1]:
            #x adjacent
            adj_point = Point(point.x + delta, point.y)
            #make sure the point is in range
            if self.hmap.containsp(adj_point):
                adjacent.append(adj_point)
            #y adjacent
            adj_point = Point(point.x, point.y+delta)
            #make sure the point is in range
            if self.hmap.containsp(adj_point):
                adjacent.append(adj_point)
        return adjacent

    def _generate_graph(self, path: List[Node]):
        current_node = path[-1]
        # print(" "*len(path), "Generating for", current_node)

        # See if the path is longer than the shortest path to the solution -- stop if so
        if self.shortest_path_depth is not None and current_node.get_depth() >= self.shortest_path_depth:
            #short circuit because any path from here would be longer than the existing solution
            return []

        # See if we are the end current_node
        if current_node.point == self.hmap.end:
            #we've reached the end!
            self.shortest_path = path
            self.shortest_path_depth = current_node.get_depth()
            print("Found path to solution of length", self.shortest_path_depth)
            print('->'.join([ f'{n.point.x},{n.point.y}' for n in path ]))
            return []

        #else continue the path search
        # Make the child nodes for this current_node
        adjacent_points = self._get_adjacent_points(current_node.point)
        child_nodes = []
        for child_point in adjacent_points:
            if child_point in self.nodes_by_point:
                #skip this for now because if we've already visited that current_node, the path to it should be the same length or shorter.
                continue
            #make a current_node for the point
            adj_elev = self.hmap.getp(child_point)
            if adj_elev > current_node.elevation + 1:
                continue
            #else can move to it
            child_node = Node(current_node, child_point, adj_elev)
            current_node.add_child(child_node)
            self.nodes_by_point[child_point] = child_node
            child_nodes.append(child_node)

        child_nodes.sort(key= lambda n: n.elevation) #iterate higher child nodes first
        #return a path for each child node
        return [ path + [cn] for cn in child_nodes ]


def part1(hmap):
    pg = PathGraph(hmap)
    return pg.shortest_path_depth

def part2(hmap):
    possible_starts = [ p for p,e in hmap.iterate() if e == 0 ]
    pprint(possible_starts)

    shortest_path = None
    shortest_path_depth = None

    for possible_start in possible_starts:
        print("Mapping start at", possible_start)
        hmap.start = possible_start
        pg = PathGraph(hmap, shortest_path_depth)

        if pg.shortest_path is not None:
            print("New shortest path of length", pg.shortest_path_depth, "from start", possible_start)
            assert shortest_path_depth is None or pg.shortest_path_depth < shortest_path_depth
            shortest_path = pg.shortest_path
            shortest_path_depth = pg.shortest_path_depth

    return shortest_path_depth

if __name__ == '__main__':

    # filename='day12/test.txt'
    filename='day12/input.txt'

    hmap = load_input(filename)

    hmap.dump()

    # print('part 1', part1(hmap))

    print('part 2', part2(hmap))

