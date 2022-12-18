
from __future__ import annotations
from typing import List, Tuple, Union, Dict, Optional

from pprint import pprint
from collections import namedtuple, Counter, defaultdict
import re







line_regex = re.compile('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels* leads* to valves* ([A-Z, ]+)')
def parse_line(line):
    # # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    # tokens = line.strip().split()
    # name = tokens[1]
    # rate = int(tokens[4].strip(';').split('=')[1])
    # list_start = tokens.index('valves')
    match = line_regex.match(line)
    if match is None:
        print(line)
    name = match.group(1)
    rate = int(match.group(2))
    destinations = [ i for i in match.group(3).split(', ') ]
    edges = []
    for d in destinations:
        edges.append((name, d))
    return name, rate, edges

Link = namedtuple('Link', ['other_valve', 'duration'])

class Valve:
    def __init__(self, name, flow_rate:int):
        self.name = name
        self.flow_rate = flow_rate
        self.links: List[Link] = []

    def add_link(self, new_link:Link):
        if new_link not in self.links:
            self.links.append(new_link)

    def __str__(self):
        link_str = ','.join([ f'{l.other_valve.name}/{l.duration}' for l in self.links])
        return f'Valve(name={self.name}, flow={self.flow_rate}, links=[{link_str}]' 
    def __repr__(self):
        return self.__str__()

def build_valve_graph(valve_flow, edges) -> Dict[Valve]:

    graph_dist = FloydWarshall(list(valve_flow.keys()), edges)

    #create valve objects only for valves with non-zero flow
    valves: Dict[Valve] = {} #map of name to valve object
    for name, flow in valve_flow.items():
        if flow == 0 and name != 'AA':
            continue
        valves[name] = Valve(name, flow)
    #now make links for the shortest paths between the non-zero valves
    # we use the FloydWarshall results, not the original edge list
    for v1 in valves.values():
        for v2 in valves.values():
            #don't make self links
            if v1 is v2:
                continue
            duration = graph_dist.get_path_length(v1.name, v2.name)
            if duration is not None:
                v1.add_link(Link(v2, duration))
                v2.add_link(Link(v1, duration))
    return valves

def load_input(filename):
    valves= []
    links = set() # to-from pairs in alphabetical order

    with open(filename) as infile:
        valve_rates = {}
        edges = set()
        for line in infile:
            name, rate, line_edges = parse_line(line)
            valve_rates[name] = rate
            for le in line_edges:
                edges.add(le)
        return build_valve_graph(valve_rates, edges)

# Use the Floyd-Warshall algorithm to simplify the graph
# Find all the shortest node paths, then make a new graph where the edge weights are the distance
# between the valves with non-zero flow rates 

class FloydWarshall:

    # from wikipedia
    # procedure FloydWarshallWithPathReconstruction() is
    #     for each edge (u, v) do
    #         dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
    #         next[u][v] ← v
    #     for each vertex v do
    #         dist[v][v] ← 0
    #         next[v][v] ← v
    #     for k from 1 to |V| do // standard Floyd-Warshall implementation
    #         for i from 1 to |V|
    #             for j from 1 to |V|
    #                 if dist[i][j] > dist[i][k] + dist[k][j] then
    #                     dist[i][j] ← dist[i][k] + dist[k][j]
    #                     next[i][j] ← next[i][k]
    # procedure Path(u, v)
    #     if next[u][v] = null then
    #         return []
    #     path ← [u]
    #     while u ≠ v
    #         u ← next[u][v]
    #         path.append(u)
    #     return path


    def __init__(self, vertices: List[str], edges: List()):
        self.vertices = vertices
        self.edges = edges
        self.num_vertices = len(vertices)
        self.__initialize__()
        self.__run__()

    def _index_to_vertex(self, *args) -> Union[List[str],str]:
        # return the indices for any number of names passed as args
        if len(args) == 1:
            return self.vertices[args[0]]
        return [ self.vertices[arg] for arg in args ]

    def _vertex_to_index(self, *args) -> Union[List[int],int]:
        # return the indices for any number of names passed as args
        if len(args) == 1:
            return self.vertices.index(args[0])
        return [ self.vertices.index(arg) for arg in args ]

    def __initialize__(self):
        self.dist = [ [ float('inf') for i in range(self.num_vertices) ] for j in range(self.num_vertices) ]
        self.next = [ [ None for i in range(self.num_vertices) ] for j in range(self.num_vertices) ]
        for edge in self.edges:
            u, v = self._vertex_to_index(*edge)
            self.dist[u][v] = 1 #all edge weights are 1
            self.next[u][v] = v #initialize the path matrix
        for vertex in self.vertices:
            v = self._vertex_to_index(vertex)
            self.dist[v][v] = 0
            self.next[v][v] = v

    def __run__(self):
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.next[i][j] = self.next[i][k]

    def get_path_length(self, vertex1:str, vertex2:str) -> int:
        u, v = self._vertex_to_index(vertex1, vertex2)
        return self.dist[u][v]

    def get_path(self, vertex1:str, vertex2:str) -> Union[List[str],None]:
        u, v = self._vertex_to_index(vertex1, vertex2)
        if self.next[u][v] is None:
            return None
        path = [u]
        while u != v:
            u = next[u][v]
            path.append(u)
        path = self._index_to_vertex(*path)
        return path

def compute_next_actors(current_state: State, current_location: Valve, current_time: int) -> List[Action]:
        next_actors = []

        if current_location.name not in current_state.open_valves:
            #action to open the valve
            #next actor is at the same location
            next_actors.append(Actor(current_location, current_time + 1, valve_to_open=current_location))
        for link in current_location.links:
            #actions to move
            next_actors.append(Actor(link.other_valve, current_time + link.duration, location_to_reach = link.other_valve))
        return next_actors

TODO THINK THROUGH THE STATE ITERATION MORE CLEARLY

class Actor:
    ACTION_OPENING="opening"
    ACTION_MOVING="moving"

    def __init__(self, location: Valve, completion_time: int, valve_to_open: Optional(Valve)=None, location_to_reach=None):
        self.location = location
        assert valve_to_open is not None or location_to_reach is not None
        self.action_type = self.ACTION_OPENING if valve_to_open is not None else self.ACTION_MOVING
        self.completion_time = completion_time
        self.valve_to_open = valve_to_open
        self.location_to_reach = location_to_reach

    def is_done(self, current_time:int):
        return current_time <= self.completion_time

class State:
    def __init__(self, location: Valve, time:int, open_valves: List[str], actors: List[Actor]):
        self.time = time
        self.open_valves = open_valves
        self.actors = actors

    def next_states(self) -> List[State]:
        #tick the time forward
        next_time = self.time + 1
        next_actors = [None for a in range(len(self.actors))]
        for actor_index, actor in enumerate(self.actors):
            if 

        if any([ a.is_done() for a in self.actors ]):





def max_flow(valves: Dict[Valve], start_name: str, start_time: int):
    
    def find_max(state: State, history: List[State]):
        pass



    initial_state = State(
        location=valves[start_name],
        time = start_time,
        open_valves = []
    )
    find_max 








def part1(valves):
    fs  = FlowSearch(valves, ['AA'], 30)
    fs.find_max_flow_state()
    # fs.dump()

    max_state = fs.max_state
    path = max_state.get_path()
    for s in path:
        print(s)
    return max_state.get_total_flow()

def part2(valves):
    fs  = FlowSearch(valves, ['AA','AA'], 26)
    fs.find_max_flow_state()
    # fs.dump()

    max_state = fs.max_state
    path = max_state.get_path()
    for s in path:
        print(s)
    return max_state.get_total_flow()


    pass

if __name__ == '__main__':

    # filename='day16/test.txt'
    filename='day16/input.txt'

    valves = load_input(filename)

    pprint(valves)

    # print('part 1', part1(valves))

    print('part 2', part2(valves))

