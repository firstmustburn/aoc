
from typing import NewType, Sequence, Callable

NodeId = NewType('NodeId', str)

def debug(*args):
    pass
    # print(args)

class Node:
    def __init__(self, id: NodeId):
        self.id = id
        self.links = [] #other nodes

    def add_link(self, linked_node: 'Node'):
        assert linked_node not in self.links
        self.links.append(linked_node)

    def is_large(self) -> bool:
        return self.id.isupper()

    def is_small(self) -> bool:
        return not self.is_large()

    def __str__(self) -> str:
        return self.id
        # return "{}({})".format(
        #     self.id,
        #     ",".join([ n.id for n in self.links ])
        # )

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other):
        return self.id.__lt__(other.id)

Path = NewType('Path', Sequence[Node])
class Graph:

    START_NODE = 'start'
    END_NODE = 'end'

    def __init__(self, filename: str, skip_fun: Callable[[Path, 'Node'], bool]):
        self.node_map = {}
        self.skip_fun = skip_fun

        with open(filename) as infile:
            lines = infile.readlines()
        
        for line in lines:
            from_id, to_id = line.strip().split("-")
            from_node = self._add_or_get_node(from_id)
            to_node = self._add_or_get_node(to_id)
            from_node.add_link(to_node)
            to_node.add_link(from_node)
        
        #make sure we got a start and end
        assert self.START_NODE in self.node_map
        assert self.END_NODE in self.node_map

    def _add_or_get_node(self, id: NodeId) -> Node:
        if id not in self.node_map:
            self.node_map[id] = Node(id)

        return self.node_map[id]

    def dump(self):
        for n in self.node_map.values():
            print(n, n.links)

    def _traverse(self, current_path : Path, depth : int = 0) -> Sequence[Path]:
        """Call recursively to traverse the graph.  Each call returns a list of valid paths
        below |currentPath|"""
        #find links that are valid
        current_node = current_path[-1]
        debug("-"*depth,"traversing", current_node, "under", pathstr(current_path))
        valid_paths = []
        debug("-"*depth,"current_node",current_node,"has links",current_node.links)
        for next_node in current_node.links:
            # stop at the end node -- halting condition
            if next_node.id == self.END_NODE:
                debug("-"*depth,"halting at end")
                valid_paths.append([next_node])
                continue
            # skip any small nodes that are already in our path
            if self.skip_fun(current_path, next_node):
                debug("-"*depth,"skipping visited node", next_node)
                continue
            # a valid next link, so traverse it
            debug("-"*depth,"recursing node", next_node)
            sub_paths = self._traverse(current_path + [ next_node ], depth+1)
            for sub_path in sub_paths:
                valid_paths.append([next_node] + sub_path)
        #done, so return valid paths
        debug("-"*depth,len(valid_paths), "paths found:", [ pathstr(p) for p in valid_paths ])
        return valid_paths

    def find_paths(self) -> Sequence[Node]:
        start_path = [self.node_map[self.START_NODE]]
        sub_paths = self._traverse(start_path)

        return [ start_path + p for p in sub_paths ]

def pathstr(p : Path) -> str:
    return str(p)

def part1_skip(current_path, next_node) -> bool:
    return next_node.is_small() and (next_node in current_path)

def has_two_small_nodes(path : Path) -> bool:
    all_nodes = set(path)
    for node in all_nodes:
        if node.is_small():
            count = len([ n for n in path if n.id == node.id ])
            if count > 1:
                return True
    return False

def part2_skip(current_path, next_node) -> bool:
    #always skip start node
    if next_node.id == Graph.START_NODE:
        return True
    #skip a small node if we have already visited it AND we have already visited any small node twice
    if next_node.is_small():
        if has_two_small_nodes(current_path) and next_node in current_path:
            return True
    #otherwise no skip
    return False

def find_all_paths(filename, skip_fun):

    graph = Graph(filename, skip_fun)
    graph.dump()
    print("*"*80)
    paths = graph.find_paths()
    paths.sort()
    for p in paths:
        print(pathstr(p))
    print("*"*80)
    print(f"Found {len(paths)} paths")
    return len(paths)

# assert find_all_paths("day12_test1.txt", part1_skip) == 10
# assert find_all_paths("day12_test2.txt", part1_skip) == 19
# assert find_all_paths("day12_test3.txt", part1_skip) == 226

# find_all_paths("day12.txt", part1_skip) #Found 4792 paths

assert find_all_paths("day12_test1.txt", part2_skip) == 36
assert find_all_paths("day12_test2.txt", part2_skip) == 103
assert find_all_paths("day12_test3.txt", part2_skip) == 3509

find_all_paths("day12.txt", part2_skip) #Found 133360 paths