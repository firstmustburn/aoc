
from __future__ import annotations
from typing import List, Tuple

from pprint import pprint
from collections import namedtuple, Counter, defaultdict
import re


Action = namedtuple('Action',['new_valve','new_location'])

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
        if d < name:
            edges.append((d, name))
        else:
            edges.append((name, d))
    return name, rate, edges

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
        return build_valves(valve_rates, edges)

CLOSED = "closed"
OPEN = "open"

class Valve:
    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.links = []

    def add_link(self, new_link):
        if new_link not in self.links:
            self.links.append(new_link)

    def __str__(self):
        link_str = ','.join([v.name for v in self.links])
        return f'Valve(name={self.name}, flow={self.flow_rate}, links=[{link_str}]' 
    def __repr__(self):
        return self.__str__()

def build_valves(valve_flow, edges):
    valves = {} #map of name to valve object
    for name, flow in valve_flow.items():
        valves[name] = Valve(name, flow)
    #now use edges to add links to valve objects
    for from_valve,to_valve in edges:
        valves[from_valve].add_link(valves[to_valve])
        valves[to_valve].add_link(valves[from_valve])
    return valves

class FlowState:

    def __init__(self, sim: FlowSearch, parent: FlowState, description: str, time: int, locations: List[Valve], open_valves: List[str]):
        self.sim = sim
        self.parent = parent
        self.description = description
        self.time = time
        self.locations = locations
        self.open_valves = open_valves
        self._flow = None
        self._total_flow = None
 
    def __str__(self):
        return f'At {self.get_location_names()}, Time {self.time}, Open: {self.open_valves}, Flow={self.get_flow()}, Total Flow={self.get_total_flow()}'

    def __repr__(self):
        return self.__str__()

    def get_location_names(self) -> List[str]:
        return [ l.name for l in self.locations ]

    def get_path(self) -> List[FlowState]:
        if self.parent is None:
            return [self]
        else:
            return self.parent.get_path() + [self]

    def get_depth(self) -> int:
        if self.parent is None:
            return 0
        else:
            return self.parent.get_depth() + 1

    def _compute_flow(self):
        flow = 0
        for ov in self.open_valves:
            flow += self.sim.valves[ov].flow_rate
        return flow

    def get_flow(self):
        if self._flow is None:
            self._flow = 0
            for ov in self.open_valves:
                self._flow += self.sim.valves[ov].flow_rate
        return self._flow

    def get_total_flow(self):
        if self._total_flow is None:
            if self.parent is not None:
                self._total_flow = self.parent.get_total_flow() + self.get_flow()
            else:
                self._total_flow = self.get_flow()
        return self._total_flow

    def iterate_actionsets(self, actionsets) -> List[Action]:
        if len(actionsets) == 1:
            for a in actionsets[0]:
                yield [a]
        elif len(actionsets) == 2:
            for a1 in actionsets[0]:
                for a2 in actionsets[1]:
                    #skip both turning the same valve
                    if a1.new_valve == a2.new_valve and a1.new_valve is not None: 
                        continue
                    yield [a1,a2]
        else:
            raise RuntimeError("Too many actionsets")


    def iterate_state(self) -> List[FlowState]:
        children = []

        #short circuit because there's no time left in the sim        
        if self.time == self.sim.LAST_TIME:
            return children

        # short circuit if there are no openable valves -- no point in moving anywhere
        # so just return the same state until we count down to 0
        if not self.sim.openable_valves_exist(self.open_valves):
            new_state = FlowState(
                sim=self.sim,
                parent=self,
                description=f'Remain at {self.get_location_names()}',
                time=self.time-1,
                locations = list(self.locations),
                open_valves = list(self.open_valves) )
            children.append(new_state)            
            return children

        #generate new states for opening a valve and moving to other locations
        actionsets: List[List[Action]] = []
        for index, location in enumerate(self.locations):
            actionset = []
            #see if we can open the valve here
            if location.name not in self.open_valves and location.flow_rate > 0:
                #next flow state does not change location, but it does open the valve
                actionset.append(Action(new_valve=location.name, new_location=None))
            #now iterate any links we can follow
            for linked_valve in location.links:
                if self.parent is not None:
                    if self.parent.locations[index] is linked_valve:
                        # print("Skipping backtrack to", linked_valve)
                        continue
                actionset.append(Action(new_valve=None, new_location = linked_valve))
            actionsets.append(actionset)

        #now permute the combinations of the action sets and make new flow states for each
        for actions in self.iterate_actionsets(actionsets):
            new_valves = []
            new_locations = []
            descriptions = []
            for index, action in enumerate(actions):
                if action.new_valve is not None:
                    #turn a valve
                    new_valves.append(action.new_valve)
                    #stay in the same place
                    new_locations.append(self.locations[index])
                    descriptions.append(f"{index} Open {action.new_valve}")
                elif action.new_location is not None:
                    #move to the new location
                    new_locations.append(action.new_location)
                    descriptions.append(f"{index} Move To {action.new_location.name}")
                else:
                    raise RuntimeError(f"Wierd action {action}")
            new_state = FlowState(
                sim=self.sim,
                parent=self,
                description=';'.join(descriptions),
                time=self.time-1,
                locations = new_locations,
                open_valves = self.open_valves + new_valves )
            children.append(new_state)

        #sort the states so states with larger flows are processed first
        children.sort(key=lambda s: s.get_total_flow(), reverse=True)
        
        #done iterating
        return children


class FlowSearch:
    LAST_TIME =1

    def __init__(self, valves: List[Valve], initial_locations: List[str], start_time):
        self.initial_locations = initial_locations
        self.start_time = start_time
        self.valves = valves
        self.openable_valve_names = ( v.name for v in self.valves if v.flow_rate > 0 )
        self.min_time = self.start_time
        self.total_valve_flow = sum([ v.flow_rate for v in self.valves.values() ])

        self.node_count = 0
        self.prune_count = 0
        self.leaf_count = 0
        self.max_state = None
        self.visited_states = {} #map of (locations, open valves) -> the latest time that state was visited

    def visit_and_prune(self, state):
        key = self._state_key(state)
        try:
            current_flow = self.visited_states[key]
            if current_flow >= state.get_total_flow():
                return True #should prune
            else:
                #keep the new value for the flow
                self.visited_states[key] = state.get_total_flow()            
        except KeyError:
            self.visited_states[key] = state.get_total_flow()
        return False #should not prune

    def _state_key(self, state: FlowState):
        return ( tuple([ l.name for l in state.locations ]), tuple(state.open_valves), state.time )

    def openable_valves_exist(self, open_valves):
        if set(open_valves) == self.openable_valve_names:
            return False
        return True

    def find_max_flow_state(self):
        #create the root state
        self.root_flow_state = FlowState(
            sim=self,
            parent=None,
            description=f'Start at {self.initial_locations}',
            time=self.start_time,
            locations = [ self.valves[l] for l in self.initial_locations],
            open_valves = [] )
        self.leaf_count += 1
        self._process_state(self.root_flow_state)


    def _process_state(self, state: FlowState):
        self.node_count += 1
        #track max states
        if state.time == self.LAST_TIME:
            if self.max_state is None:
                self.max_state = state
            else:
                if state.get_total_flow() > self.max_state.get_total_flow():
                    print("New max at", state)
                    self.max_state = state
        #periodically print stats
        if self.node_count % 100000 == 0:
            print("Node count", self.node_count, "prune count", self.prune_count, "leaf count", self.leaf_count, 'Max State', self.max_state)

        should_prune = False
        #prune states that can never reach the current max
        if self.max_state is not None and state.get_total_flow() + state.time * self.total_valve_flow < self.max_state.get_total_flow():
            should_prune = True
        #prune states that we have already visited
        elif self.visit_and_prune(state):
            # print("already visited", state)
            should_prune = True

        if should_prune:
            # print("Pruning state that can never reach the current max", state)
            self.prune_count += 1
            self.leaf_count -= 1
            return

        #iterate children
        children = state.iterate_state()
        self.leaf_count += len(children) - 1 #less one for the node that is no longer a leaf
        for child in children:
            self._process_state(child)


def part1(valves):
    fs  = FlowSearch(valves, ['AA'], 30)
    fs.find_max_flow_state()
    # fs.dump()
    print("final node count", fs.node_count, "final prune count", fs.prune_count)

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

if __name__ == '__main__':

    # filename='day16/test.txt'
    filename='day16/input.txt'

    valves = load_input(filename)

    pprint(valves)

    print('part 1', part1(valves))

    # print('part 2', part2(valves))

