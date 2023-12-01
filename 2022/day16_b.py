
from __future__ import annotations
from typing import List, Tuple, Union, Dict, Optional

from pprint import pprint
from collections import namedtuple, Counter, defaultdict
import re
import itertools

# this doesn't work -- it should have the truncation of states when all the valves are finally open
# and then it might work


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
            self.links.sort(key=lambda l: l.duration*l.other_valve.flow_rate, reverse=True)

    def __str__(self):
        link_str = ','.join([ f'{l.other_valve.name}/{l.other_valve.flow_rate}/{l.duration}' for l in self.links])
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

class Actor:
    ACTION_OPENING="opening"
    ACTION_MOVING="moving"
    LAST_TIME=1

    def __init__(self, location: Valve, last_location: Valve, completion_time: int, valve_to_open: Optional(Valve)=None, location_to_reach: Optional[Valve]=None):
        self.location = location
        self.last_location = last_location
        assert valve_to_open is not None or location_to_reach is not None
        self.action_type = self.ACTION_OPENING if valve_to_open is not None else self.ACTION_MOVING
        self.completion_time = completion_time
        self.valve_to_open = valve_to_open
        self.location_to_reach = location_to_reach

    def is_done(self, time:int):
        return time <= self.completion_time

    def get_next_actors(self, valves: Dict[str, Valve], open_valves: List[str], next_time: int) -> List[Actor]:
        next_actors = []

        if not self.is_done(next_time):
            #not done so make a copy of the same actor
            next_actors.append(Actor(
                location=self.location,
                last_location=self.last_location,
                completion_time = self.completion_time,
                valve_to_open=self.valve_to_open,
                location_to_reach=self.location_to_reach
            ))
        else:
            #done so make actors for everything we could do next
            if self.location.name not in open_valves and valves[self.location.name].flow_rate > 0:
                #action to open the valve
                #next actor is at the same location
                next_actors.append(Actor(self.location, self.last_location, next_time, valve_to_open=self.location))
            for link in self.location.links:
                #don't move back to where we just were
                if link.other_valve is self.last_location:
                    continue
                #actions to move -- the next actor will be at a new location after the link duration
                link_completion_time = next_time - link.duration + 1
                if link_completion_time >= self.LAST_TIME:
                    next_actors.append(Actor(link.other_valve, self.location, link_completion_time, location_to_reach = link.other_valve))
        
        return next_actors

    def __str__(self):
        if self.action_type == self.ACTION_OPENING:
            action_str = f"Opening {self.valve_to_open.name}"
        elif self.action_type == self.ACTION_MOVING:
            action_str = f'Moving to {self.location_to_reach.name}'
        return f'Actor(loc={self.location.name}, last_loc={self.last_location.name}, completion={self.completion_time}, action={action_str})'
    
    def __repr__(self):
        return self.__str__()


class State:
    def __init__(self, time:int, open_valves: List[str], actors: List[Actor]):
        self.time = time
        self.open_valves = open_valves
        self.actors = actors
        self.state_flow = None
        self.cumulative_flow = None

    def _iterate_actor_groups(self, groups: List[List[Actor]]):
        actor_sets: List[Tuple[Actor]] = itertools.product(*groups)
        final_actor_sets = []

        for actor_set in actor_sets:
            targeted_valves = set()
            skip_set = False
            for actor in actor_set:
                if actor.action_type == actor.ACTION_OPENING:
                    if actor.valve_to_open in targeted_valves:
                        #skip becaue both actors targeting the same valve
                        # print("Skip two actors opening the same valve", actor_set)
                        skip_set = True
                        break
                    else:
                        targeted_valves.add(actor.valve_to_open)
            if skip_set:
                continue                    
            final_actor_sets.append(list(actor_set))
        # #now sort the final sets
        # def sort_key(actor_set: List[Actor]):
        #     score = 0
        #     for actor in actor_set:
        #         if actor.action_type == actor.ACTION_MOVING:
        #             score += actor.location_to_reach.flow_rate
        #         elif actor.action_type == actor.ACTION_OPENING:
        #             score += actor.valve_to_open.flow_rate * 2
        #     return score
        # final_actor_sets.sort(key=lambda s: sort_key(s), reverse=True)
        return final_actor_sets


    def get_next_states(self, valves: Dict[str, Valve]) -> List[State]:
        next_time = self.time-1
        next_open_valves = list(self.open_valves)
        #update the valves if any were opened
        for actor in self.actors:
            if actor.is_done(next_time) and actor.action_type == actor.ACTION_OPENING:
                if actor.valve_to_open.name not in next_open_valves:
                    next_open_valves.append(actor.valve_to_open.name)

        #get actors for the next tick
        next_actor_groups = [ a.get_next_actors(valves, next_open_valves, next_time) for a in self.actors ]
        #permute the next actors combinations into states
        next_states = []
        for next_actors in self._iterate_actor_groups(next_actor_groups):
            next_states.append(State(next_time, next_open_valves, next_actors))
        return next_states

    def __str__(self):
        return f'State(time={self.time}, open_valves={[self.open_valves]}, actors={self.actors})'

    def __repr__(self):
        return self.__str__()


class FlowMax:
    LAST_TIME=1

    def __init__(self, valves: Dict[str,Valve], start_location: str, actor_count: int, start_time: int):

        self.valves = valves
        self.total_valve_flow = sum([ v.flow_rate for v in self.valves.values() ])
        
        self.max_flow_level = 0
        self.max_flow_path = None
        self.prune_count = 0
        self.state_count = 0
        self.visited_states = {} #map of (locations, open valves) -> the latest time that state was visited

        initial_actors = [  
            Actor(valves[start_location], valves[start_location], start_time, location_to_reach=valves[start_location])
            for i in range(actor_count)
        ]
        initial_state = State(
            time = start_time,
            open_valves = [],
            actors = initial_actors,
        )
        self._iter_max([initial_state])

    def compute_state_flow(self, state: State):
        if state.state_flow is None:
            state.state_flow = sum( [ self.valves[vname].flow_rate for vname in state.open_valves ] )
        return state.state_flow

    def compute_path_flow(self, path):
        if path[-1].cumulative_flow is None:
            if len(path) > 1:
                path[-1].cumulative_flow = path[-2].cumulative_flow + self.compute_state_flow(path[-1])
            else:
                path[-1].cumulative_flow = self.compute_state_flow(path[-1])
        return path[-1].cumulative_flow

    def visit_and_prune(self, state, state_cumulative_flow):
        key = self._state_key(state)
        try:
            saved_flow = self.visited_states[key]
            if saved_flow >= state_cumulative_flow and saved_flow > 0:
                # print(f'Prune state {key} with existing flow {saved_flow} and new flow {state_cumulative_flow}')
                return True #should prune
            else:
                #keep the new value for the flow
                self.visited_states[key] = state_cumulative_flow            
        except KeyError:
            self.visited_states[key] = state_cumulative_flow
        return False #should not prune

    def _state_key(self, state: State):
        return tuple([frozenset([ a.location.name for a in state.actors ]), frozenset(state.open_valves)])

    def _iter_max(self, current_path: List[State]):
        self.state_count += 1
        final_state = current_path[-1]
        current_flow_level = self.compute_path_flow(current_path)
        # print(" "*len(current_path), final_state)
        
        #see if we're at the end
        if final_state.time == self.LAST_TIME:
            if current_flow_level > self.max_flow_level:
                self.max_flow_level = current_flow_level
                self.max_flow_path = current_path
                print("New max found:", self.max_flow_level)
                # self.print_path(self.max_flow_path)
            # terminate
            return
        
        # see if we should prune this path based on the total flow possible in the remaining time
        if current_flow_level + final_state.time * self.total_valve_flow < self.max_flow_level:
            #prune this branch
            # print(f'Prune branch that cannot exceed current max ({self.max_flow_level}: {current_flow_level} so far and {final_state.time} time remaining')
            self.prune_count += 1
            return
        # prune states that we have visited already if our cumulative flow is less than the last time
        if self.visit_and_prune(final_state, current_flow_level):
            self.prune_count +=1
            return

        if self.state_count % 100000 == 0:
            print("State count", self.state_count, "prune count", self.prune_count, 'Max flow', self.max_flow_level)

        #not at the end, so iterate the state:
        next_states = final_state.get_next_states(valves)
        for next_state in next_states:
            self._iter_max(current_path + [next_state])

    def print_path(self, path):
        for p in path:
            print(p)

def part1(valves):
    fm = FlowMax(valves, 'AA', 1, 30)
    print("Final path")
    fm.print_path(fm.max_flow_path)
    return fm.max_flow_level

def part2(valves):
    fm = FlowMax(valves, 'AA', 2, 26)
    print("Final path")
    fm.print_path(fm.max_flow_path)
    return fm.max_flow_level

if __name__ == '__main__':

    # filename='day16/test.txt'
    filename='day16/input.txt'

    valves = load_input(filename)

    pprint(valves)

    print('part 1', part1(valves))

    # print('part 2', part2(valves))

