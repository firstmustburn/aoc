from __future__ import annotations
from typing import List, Dict

import sys

from pprint import pprint
from collections import namedtuple

def make_resource_list():
    return [ 0 for i in range(5) ]

def resource_list_str(listval):
    return '[ ' + ', '.join( f'{robot_str(i)}={v}' for i,v in enumerate(listval)) + ' ]'

def dprint(*args, **kwargs):
    pass

# dprint = print

# def dprint(*args, **kwargs):
#     print(*args, **kwargs)

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
NO_ROBOT = 4

ROBOT_NAMES = ["ore", "clay", "obsidian", "geode", "no_robot"]

def robot_str(i: int):
    return ROBOT_NAMES[i]

Cost = namedtuple('Cost', ['amount','unit'])
ResourceList = List[int]

class Blueprint:
    @classmethod
    def parse(cls, line):
        tokens = line.strip().split()
        id = int(tokens[1].strip(':'))
        ore_ore_cost = int(tokens[6])
        clay_ore_cost = int(tokens[12])
        obsidian_ore_cost = int(tokens[18])
        obsidian_clay_cost = int(tokens[21])
        geode_ore_cost = int(tokens[27])
        geode_obsidian_cost = int(tokens[30])

        robot_costs = [
            [Cost(ore_ore_cost, ORE)],
            [Cost(clay_ore_cost, ORE)],
            [Cost(obsidian_ore_cost, ORE),Cost(obsidian_clay_cost, CLAY)],
            [Cost(geode_ore_cost, ORE),Cost(geode_obsidian_cost, OBSIDIAN)],
            []
        ]

        max_resource_costs = [
            max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost),
            obsidian_clay_cost,
            geode_obsidian_cost,
            1000,
            1000,
        ]
        return Blueprint(id, robot_costs, max_resource_costs)

    def __init__(self, id: int, robot_costs: Dict[str,List[Cost]], max_resource_costs: ResourceList):
        self.id = id
        self.robot_costs = robot_costs
        self.max_resource_costs = max_resource_costs
        self.__strval = None

    def max_cost(self, resource_type: int) -> int:
        return self.max_resource_costs[resource_type]

    def __str__(self):
        if self.__strval is None:
            robot_strs = []
            for robot_index, costlist in enumerate(self.robot_costs):
                cost_str = ' + '.join([ f'{c.amount} {robot_str(c.unit)}' for c in costlist ])
                robot_strs.append(f'{robot_str(robot_index)}={cost_str}')
            self.__strval = f'Blueprint(id={self.id}, ' + ', '.join(robot_strs) + ")"
        return self.__strval

    def __repr__(self):
        return self.__str__()

def load_input(filename):
    with open(filename) as infile:
        blueprints = [ Blueprint.parse(line) for line in infile]
    return blueprints

class ResultFoundException(Exception):
    pass



class Graph:
    geode_spec_values = [ None for i in range(40)]

    def __init__(self, blueprint: Blueprint, last_time: int):
        self.blueprint = blueprint
        self.last_time = last_time
        self.state_count = 0
        self.prune_count = 0
        self.search_result = None
        self._search_graph()

    def _search_graph(self):

        #start with one one ore robot and no resources
        resources = make_resource_list()
        robots = make_resource_list()
        robots[ORE] += 1
        self.root  = RobotState(None, 0, ORE, robots, resources)
        self._iterate_state(self.root, '')

        assert self.search_result is not None

    def _can_build(self, resources: ResourceList, robot_type: int):
        for cost in self.blueprint.robot_costs[robot_type]:
            if resources[cost.unit] < cost.amount:
                # print("can_build FALSE", resources, robot_type)
                return False
        # print("can_build TRUE", resources, robot_type)
        return True

    def _increment_resources(self, resources: ResourceList, robots: ResourceList):
        for robot_type, robot_count in enumerate(robots):
            resources[robot_type] += robot_count
        return resources

    def _process_final_state(self, state: RobotState):
        if self.search_result is None or state.resources_available[GEODE] > self.search_result.resources_available[GEODE]:
            print(f"Found new solution with {state.resources_available[GEODE]} geodes")
            self.search_result = state
            RobotState.dump_sequence(state)
            state.dump()
            print("---------------------------------------------------------------------------")
        # else:
        #     print(f"Not improved solution with {state.resources_available[GEODE]} geodes")
        #     self.search_result = state
        #     RobotState.dump_sequence(state)
        #     state.dump()
        #     print("---------------------------------------------------------------------------")


    def _geode_spec_count(self, time_remaining):
        retval = self.geode_spec_values[time_remaining]
        if retval is None:
            if time_remaining <= 1:
                self.geode_spec_values[time_remaining] = 0
                retval = 0
            else:
                gsc = self._geode_spec_count(time_remaining-1) + time_remaining-1
                self.geode_spec_values[time_remaining] = gsc
                retval = gsc
        return retval

    def _iterate_state(self, state: RobotState, depth_str = '.'):
        self.state_count += 1
        if self.state_count % 1000000 == 0:
            print("State count", self.state_count, "Prune count", self.prune_count)
            RobotState.dump_sequence(state)

        #termination condition
        if state.time == self.last_time:
            self._process_final_state(state)
            return

        # prune when we can't score better than the current best score:
        if self.search_result is not None:
            #compute the maximum possible number of geodes, assuming all the remaining builds could be geodes
            time_remaining = self.last_time - state.time
            max_geodes = state.resources_available[GEODE] + time_remaining * state.robots[GEODE] + time_remaining * self._geode_spec_count(time_remaining)
            if max_geodes < self.search_result.resources_available[GEODE]:
                # print(f"Pruning state that can only produce {max_geodes} which is less than {self.search_result.resources_available[GEODE]}")
                self.prune_count += 1
                return


        state_has_child = False

        #decide which robot to build next
        if state.time == self.last_time-1:
            next_robot_sequence = []
        elif state.time == self.last_time-2:
            next_robot_sequence = [GEODE]
        elif state.time == self.last_time-3:
            next_robot_sequence = [GEODE, OBSIDIAN, ORE]
        else:
            next_robot_sequence = [GEODE, OBSIDIAN, CLAY, ORE, NO_ROBOT]
        dprint(depth_str, "next robot sequence", next_robot_sequence, "at time", state.time)
        
        for next_robot in next_robot_sequence:
        # for next_robot in [ORE, CLAY, OBSIDIAN, GEODE]:
            dprint(depth_str, "Trying to build a", robot_str(next_robot))
            #skip robots that we have too many of all ready
            if state.robots[next_robot] >= self.blueprint.max_cost(next_robot)+1:
                dprint(depth_str, f"Stop building {robot_str(next_robot)} after {state.robots[next_robot]} aere")
                continue

            #skip builds if we don't have the robots to produce resources
            if next_robot == OBSIDIAN and state.robots[CLAY] == 0:
                dprint(depth_str, "Skip obsidian if no clay")
                continue

            #skip builds if we don't have the robots to produce resources
            if next_robot == GEODE and state.robots[OBSIDIAN] == 0:
                dprint(depth_str, "Skip geode if no obsidian")
                continue

            #copy and augment the current state resources
            resources = list(state.resources_available)
            next_time = state.time
            while not self._can_build(resources, next_robot):
                next_time += 1
                if next_time > self.last_time:
                    break
                self._increment_resources(resources, state.robots)
                dprint(depth_str, "increment resources to", resource_list_str(resources), 'at time', next_time)
            
            #add one more time step because the build happens in the next step
            next_time += 1
            self._increment_resources(resources, state.robots)

            if next_time > self.last_time:
                #can't build this resource in time
                dprint(depth_str, f"Can't build a {robot_str(next_robot)} robot in time")
                continue

            #now we can build the robot we want to build
            dprint(depth_str, f"Build a {robot_str(next_robot)} at {next_time}")
            state_has_child = True
            #decrement for robot resources
            for cost in self.blueprint.robot_costs[next_robot]:
                resources[cost.unit] -= cost.amount
            dprint(depth_str, f"decrement costs for {robot_str(next_robot)} to {resources}")

            #copy the robots list and add the new robot
            robots = list(state.robots)
            robots[next_robot] += 1

            next_state = RobotState(state, next_time, next_robot, robots, resources)
            dprint(depth_str, "next_state:", next_state)
            self._iterate_state(next_state, depth_str + '.')

        # if we were not able to build any child nodes, then run the current set of robots through
        # the last time and process it as a final state
        if not state_has_child:
            resources = list(state.resources_available)
            robots = list(state.robots)
            next_time = state.time
            while next_time < self.last_time:
                next_time += 1
                self._increment_resources(resources, state.robots)
                dprint(depth_str, "increment resources to", resource_list_str(resources), 'at time', next_time)
            
            next_state = RobotState(state, next_time, NO_ROBOT, robots, resources)
            dprint(depth_str, "final_state:", next_state)
            self._process_final_state(next_state)

class RobotState:

    @staticmethod
    def dump_sequence(state: RobotState, prefix: str='', extended: bool = False):
        seq = state.get_sequence()
        # seq.reverse()
        print(prefix, ', '.join([ f'{robot_str(r)} @ {t}' for t,r in seq ]))
        if extended:
            states = state.get_state_sequence()
            for index, s in enumerate(states):
                print('.'*index, s)

    def __init__(self, parent_state: RobotState, time: int, new_robot: str, robots: ResourceList, resources_available: ResourceList):
        self.parent_state = parent_state
        self.time = time
        self.new_robot = new_robot
        self.robots = robots
        self.resources_available = resources_available
        self._depth = None

    def __str__(self):
        return f'S(time={self.time}, new_robot={robot_str(self.new_robot)}, robots={resource_list_str(self.robots)}, resources={resource_list_str(self.resources_available)})'
    
    def __repr__(self):
        return self.__str__()

    def get_depth(self):
        if self._depth is None:
            if self.parent_state is None:
                self._depth = 0
            else:
                self._depth = self.parent_state.get_depth() + 1
        return self._depth
        

    def get_state_sequence(self):
        if self.parent_state is None:
            return [self]
        else:
            s = self.parent_state.get_state_sequence()
            s.append(self)
            return s

    def get_sequence(self):
        if self.parent_state is None:
            return [(self.time, self.new_robot)]
        else:
            s = self.parent_state.get_sequence()
            s.append((self.time, self.new_robot))
            return s

    def dump(self):
        print("Robots", resource_list_str(self.robots))
        print("Resources", resource_list_str(self.resources_available))

def part1(blueprints: List[Blueprint]):
    last_time = 24

    quality_level = 0

    for blueprint in blueprints:
        # if blueprint.id != 2:
        #     continue
        print("Iterating blueprint", blueprint)
        print("---------------------------------------------------------------------------")
        g = Graph(blueprint, last_time)
        # assert g.search_result.resources_available[GEODE] > 0
        quality_level += blueprint.id * g.search_result.resources_available[GEODE]
        g.search_result.dump()
        RobotState.dump_sequence(g.search_result, extended=True)
        print("============================================================================")
        print('')

    return quality_level
    
    

def part2(blueprints):
    last_time = 32

    geode_product = 1
    for blueprint in blueprints[:3]:
        print("Iterating blueprint", blueprint)
        print("---------------------------------------------------------------------------")
        g = Graph(blueprint, last_time)
        # assert g.search_result.resources_available[GEODE] > 0
        print("Geode count", g.search_result.resources_available[GEODE])
        geode_product *= g.search_result.resources_available[GEODE]
        g.search_result.dump()
        RobotState.dump_sequence(g.search_result, extended=True)
        print("============================================================================")
        print('')

    return geode_product

if __name__ == '__main__':

    # filename='day19/test.txt'
    filename='day19/input.txt'

    blueprints = load_input(filename)

    # for blueprint in blueprints:
    #     print(blueprint)

    # print('part 1', part1(blueprints))

    print('part 2', part2(blueprints))

