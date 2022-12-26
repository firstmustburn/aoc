from __future__ import annotations
from typing import List, Dict

import sys

from pprint import pprint
from collections import namedtuple

def make_resource_list():
    return [ 0 for i in range(4) ]

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

ROBOTS = [
    GEODE,
    OBSIDIAN, 
    CLAY, 
    ORE, 
]

ROBOT_NAMES = ["ore", "clay", "obsidian", "geode"]

def robot_str(i: int):
    return ROBOT_NAMES[i]

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

        return Blueprint(id, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost)

    def __init__(self, id: int, ore_ore_cost: int, clay_ore_cost: int, obsidian_ore_cost: int, obsidian_clay_cost: int, geode_ore_cost: int, geode_obsidian_cost: int):
        self.id = id

        self.ore_ore_cost = ore_ore_cost
        self.clay_ore_cost = clay_ore_cost
        self.obsidian_ore_cost = obsidian_ore_cost
        self.obsidian_clay_cost = obsidian_clay_cost
        self.geode_ore_cost = geode_ore_cost
        self.geode_obsidian_cost = geode_obsidian_cost

        self.robot_costs = [
            [ore_ore_cost, 0, 0, 0], 
            [clay_ore_cost, 0, 0, 0], 
            [obsidian_ore_cost, obsidian_clay_cost, 0, 0], 
            [geode_ore_cost, 0, geode_obsidian_cost, 0], 
        ]

        self.max_costs = [
            max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost),
            obsidian_clay_cost,
            geode_obsidian_cost,
            1000,
        ]

    def can_build_ore(self, resources: ResourceList):
        return resources[ORE] >= self.ore_ore_cost

    def can_build_clay(self, resources: ResourceList):
        return resources[ORE] >= self.clay_ore_cost

    def can_build_obsidian(self, resources: ResourceList):
        return resources[ORE] >= self.obsidian_ore_cost and resources[CLAY] >= self.obsidian_clay_cost

    def can_build_geode(self, resources: ResourceList):
        return resources[ORE] >= self.geode_ore_cost and resources[OBSIDIAN] >= self.geode_obsidian_cost

    def can_build(self, robot: int, resources: ResourceList):
        if robot == ORE:
            return self.can_build_ore(resources)
        elif robot == CLAY:
            return self.can_build_clay(resources)
        elif robot == OBSIDIAN:
            return self.can_build_obsidian(resources)
        elif robot == GEODE:
            return self.can_build_geode(resources)
        else:
            raise RuntimeError(f"Unhandled robot {robot}")
        pass

    def __str__(self):
        robot_strs = []
        for robot_index, costlist in enumerate(self.robot_costs):
            cost_str = ' + '.join([ f'{c} {robot_str(i)}' for i, c in enumerate(costlist) if c > 0 ])
            robot_strs.append(f'{robot_str(robot_index)}={cost_str}')
        return f'Blueprint(id={self.id}, ' + ', '.join(robot_strs) + ")"

    def __repr__(self):
        return self.__str__()

def load_input(filename):
    with open(filename) as infile:
        blueprints = [ Blueprint.parse(line) for line in infile]
    return blueprints


class RobotSearch:

    def __init__(self, blueprint: Blueprint, search_duration: int):
        self.blueprint = blueprint
        self.search_duration = search_duration
        self.current_max = 0

        self.geodes_possible = [ t*(t-1) // 2 for t in range(search_duration + 1) ]


    def do_search(self):
        for next_robot in ROBOTS:
            self._find_max(self.search_duration, next_robot, [1,0,0,0], [0,0,0,0])
        return self.current_max

    def _find_max(self, time_remaining: int, robot_to_build: int, robots: ResourceList, resources: ResourceList) -> int:
        #reasons to skip:
        # build no geodes if no obsidian robots
        # build no obsidians if no clays or too many obsidian robots already
        # build no clays if too many clay robots already
        # build no ores if too many ore robots already
        # stop if we can't possibly achieve more geodes than we currently have
        if (
            (robot_to_build == GEODE and robots[OBSIDIAN] == 0) or
            (robot_to_build == OBSIDIAN and (robots[CLAY] == 0 or robots[OBSIDIAN] >= self.blueprint.max_costs[OBSIDIAN] )) or
            (robot_to_build == CLAY and robots[CLAY] >= self.blueprint.max_costs[CLAY] ) or
            (robot_to_build == ORE and robots[ORE] >= self.blueprint.max_costs[ORE] ) or
            (resources[GEODE] + robots[GEODE] * time_remaining + self.geodes_possible[time_remaining] < self.current_max)
            ):
            return
        next_resources = list(resources)
        while time_remaining > 0:
            #branch out if we can build another robot
            if self.blueprint.can_build(robot_to_build, next_resources):
                #decrement resources for the robot we built and
                #add the resources from the robots we had
                for i in range(len(next_resources)):
                    next_resources[i] = next_resources[i] \
                        - self.blueprint.robot_costs[robot_to_build][i] \
                        + robots[i]
                #add the robot we built
                next_robots = list(robots)
                next_robots[robot_to_build] = next_robots[robot_to_build] + 1
                for next_robot in ROBOTS:
                    self._find_max(time_remaining-1, next_robot, next_robots, next_resources)
                #stop searching when we built a robot
                return
            #we didn't build a robot, so keep ticking down
            time_remaining = time_remaining - 1
            #add resources every tick
            for i in range(len(next_resources)):
                next_resources[i] = next_resources[i] + robots[i]
        #if we get here, we should check whether this is the max
        if next_resources[GEODE] > self.current_max:
            self.current_max = next_resources[GEODE]
            print("New max value", self.current_max)
        # self.current_max = max(self.current_max, next_resources[GEODE])


def part2(blueprints):
    search_duration = 32

    geode_product = 1
    for blueprint in blueprints[:3]:
        print("Iterating blueprint", blueprint)

        rs = RobotSearch(blueprint, search_duration)
        max_value = rs.do_search()
        geode_product *= max_value

        print("Max value", max_value)
        print("-------------------------------")

    print("Final geode product", geode_product)

if __name__ == '__main__':

    # filename='day19/test.txt'
    filename='day19/input.txt'

    blueprints = load_input(filename)

    # for blueprint in blueprints:
    #     print(blueprint)

    print('part 2', part2(blueprints))

