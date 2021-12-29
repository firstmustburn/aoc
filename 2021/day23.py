from collections import namedtuple
from functools import total_ordering
from frozendict import frozendict as fd
from os import path, pathsep

def debug(*args):
    pass
    # print(*args)

Link = namedtuple("Link",["distance","position"])

class Position:

    def __init__(self, description, destination_for=None):
        self.description = description
        self.destination_for = destination_for
        self._links = []
        self._contents=None

    def set_contents(self, contents):
        self._contents = contents

    def get_contents(self):
        return self._contents

    def add_link(self, position, distance):
        self._links.append(Link(distance, position))

    def iterate_links(self, filter=None):
        for p in self._links:
            if filter is None:
                yield p
            else:
                if filter(p):
                    yield p

A_TYPE="A"
B_TYPE="B"
C_TYPE="C"
D_TYPE="D"

LL_POS="left left"
LR_POS="left right"
AU_POS="A upper"
AL_POS="A lower"
BU_POS="B upper"
BL_POS="B lower"
CU_POS="C upper"
CL_POS="C lower"
DU_POS="D upper"
DL_POS="D lower"
AB_MID="AB mid"
BC_MID="BC mid"
CD_MID="CD mid"
RL_POS="right left"
RR_POS="right right"

POSITION_TO_INDEX = fd({
    LL_POS:0,
    LR_POS:1,
    AU_POS:2,
    AL_POS:3,
    BU_POS:4,
    BL_POS:5,
    CU_POS:6,
    CL_POS:7,
    DU_POS:8,
    DL_POS:9,
    AB_MID:10,
    BC_MID:11,
    CD_MID:12,
    RL_POS:13,
    RR_POS:14,
})
#reverse the position map
INDEX_TO_POSITION = fd({v:k for k,v in POSITION_TO_INDEX.items()})

#############
#...........#  LL LR . AB . BC . CD . RL RR
###A#B#C#D###        AU   BU   CU   DU
  #A#B#C#D#          AL   BL   CL   DL
  #########

# next positions and distances available to each position:
NEXT_POSITIONS = fd({
    LL_POS: tuple([(LR_POS,1)]),
    LR_POS: tuple([(AU_POS,2),(LL_POS,1),(AB_MID,2)]),
    AU_POS: tuple([(AL_POS,1),(LR_POS,2),(AB_MID,2)]),
    AL_POS: tuple([(AU_POS,1)]),
    BU_POS: tuple([(BL_POS,1),(AB_MID,2),(BC_MID,2)]),
    BL_POS: tuple([(BU_POS,1)]),
    CU_POS: tuple([(CL_POS,1),(BC_MID,2),(CD_MID,2)]),
    CL_POS: tuple([(CU_POS,1)]),
    DU_POS: tuple([(DL_POS,1),(CD_MID,2),(RL_POS,2)]),
    DL_POS: tuple([(DU_POS,1)]),
    AB_MID: tuple([(AU_POS,2),(BU_POS,2),(LR_POS,2),(BC_MID,2)]),
    BC_MID: tuple([(BU_POS,2),(CU_POS,2),(AB_MID,2),(CD_MID,2)]),
    CD_MID: tuple([(CU_POS,2),(DU_POS,2),(BC_MID,2),(RL_POS,2)]),
    RL_POS: tuple([(DU_POS,2),(RR_POS,1),(CD_MID,2)]),
    RR_POS: tuple([(RL_POS,1)]),
})
NEXT_POSITIONS_INDEXED = fd({ 
    POSITION_TO_INDEX[from_pos] : 
    [ (POSITION_TO_INDEX[to_pos], to_len) for to_pos, to_len in to_pos_list ] 
    for from_pos, to_pos_list in NEXT_POSITIONS.items() })

MOVE_COST = fd({
    A_TYPE:1,
    B_TYPE:10,
    C_TYPE:100,
    D_TYPE:1000,
})

DESTINATION_FOR = fd({
    A_TYPE: (AU_POS, AL_POS),
    B_TYPE: (BU_POS, BL_POS),
    C_TYPE: (CU_POS, CL_POS),
    D_TYPE: (DU_POS, DL_POS),
})
DESTINATION_FOR_INDEXED = fd({ k: tuple([ POSITION_TO_INDEX[i] for i in v ]) for k,v in DESTINATION_FOR.items() })

TYPE_OF_DESTINATION = fd({
    AU_POS:A_TYPE,
    AL_POS:A_TYPE,
    BU_POS:B_TYPE,
    BL_POS:B_TYPE,
    CU_POS:C_TYPE,
    CL_POS:C_TYPE,
    DU_POS:D_TYPE,
    DL_POS:D_TYPE,
})
TYPE_OF_DESTINATION_INDEXED = fd({ POSITION_TO_INDEX[k]:v for k,v in TYPE_OF_DESTINATION.items() })


DESTINATION_POSITIONS = (
    AU_POS,
    AL_POS,
    BU_POS,
    BL_POS,
    CU_POS,
    CL_POS,
    DU_POS,
    DL_POS,
)
DESTINATION_POSITIONS_INDEXED = tuple([ POSITION_TO_INDEX[v] for v in DESTINATION_POSITIONS ])

#NOTE: excludes LL and RR
MID_POSITIONS = (
    LR_POS,
    AB_MID,
    BC_MID,
    CD_MID,
    RL_POS,
)
MID_POSITIONS_INDEXED = tuple([ POSITION_TO_INDEX[v] for v in MID_POSITIONS ])


UPPER_LOWER_MAP = fd({
    AU_POS: AL_POS,
    BU_POS: BL_POS,
    CU_POS: CL_POS,
    DU_POS: DL_POS,
})
UPPER_LOWER_MAP_INDEXED = fd({ POSITION_TO_INDEX[k]:POSITION_TO_INDEX[v] for k,v in UPPER_LOWER_MAP.items() })

LOWER_UPPER_MAP = fd({v:k for k,v in UPPER_LOWER_MAP.items() })
LOWER_UPPER_MAP_INDEXED = fd({ POSITION_TO_INDEX[k]:POSITION_TO_INDEX[v] for k,v in LOWER_UPPER_MAP.items() })

OTHER_DESTINATION_MAP = fd({
    AU_POS: AL_POS,
    BU_POS: BL_POS,
    CU_POS: CL_POS,
    DU_POS: DL_POS,
    AL_POS: AU_POS,
    BL_POS: BU_POS,
    CL_POS: CU_POS,
    DL_POS: DU_POS,
})
OTHER_DESTINATION_MAP_INDEXED = fd({ POSITION_TO_INDEX[k]:POSITION_TO_INDEX[v] for k,v in OTHER_DESTINATION_MAP.items() })


class State:

    def __init__(self, positions, cost, paths):
        assert len(positions) == len(POSITION_TO_INDEX)
        self.cost = cost
        self.positions = positions
        self.paths = paths

    def apply_path(self, type_value, path, path_cost):
        new_positions = list(self.positions)
        assert new_positions[path[0]] == type_value
        for pind in path[1:]:
            assert new_positions[pind] is None
        new_positions[path[0]] = None
        new_positions[path[-1]] = type_value
        return State(new_positions, self.cost + path_cost, self.paths + [(type_value, path)])

    def is_complete(self):
        for type_val, indices in DESTINATION_FOR_INDEXED.items():
            for index in indices:
                if self.positions[index] != type_val:
                    return False
        return True

    @classmethod
    def get_occupied_positions(cls, position_list):
        for pos_index, pos_value in enumerate(position_list):
            #empty
            if pos_value is None:
                continue
            #in its destination
            if pos_index in DESTINATION_FOR_INDEXED[pos_value]:
                if cls.is_lower(pos_index):
                    #lower index means it's in its destination no matter what
                    continue
                elif cls.is_upper(pos_index) \
                    and position_list[OTHER_DESTINATION_MAP_INDEXED[pos_index]] == pos_value:
                    #  upper index is in its place if the lower index is
                    continue
            yield pos_index, pos_value

    @classmethod
    def get_next_path_indices(cls, path_indices, position_list):
        for next_pos_index, next_pos_distance in NEXT_POSITIONS_INDEXED[path_indices[-1]]:
            #skip occupied
            if position_list[next_pos_index] is not None:
                continue
            #skip if in path
            if next_pos_index in path_indices:
                continue
            yield next_pos_index, next_pos_distance

    @classmethod
    def is_destination(cls, position_index):
        return position_index in DESTINATION_POSITIONS_INDEXED

    @classmethod
    def is_not_destination(cls, position_index):
        return not cls.is_destination(position_index)

    @classmethod
    def is_lower(cls, position_index):
        return position_index in LOWER_UPPER_MAP_INDEXED

    @classmethod
    def is_upper(cls, position_index):
        return position_index in UPPER_LOWER_MAP_INDEXED

    @classmethod
    def is_target_destination_traversible(cls, path_indices, original_type, target_index, position_list):
        assert cls.is_destination(target_index)
        type_of_destination = TYPE_OF_DESTINATION_INDEXED[target_index]
        #same type is always traversible
        if type_of_destination == original_type:
            return True
        #the rest is for different types
        #the upper is traversible if we started out in the lower
        #too long a path to traverse the upper
        if len(path_indices) > 1: 
            return False
        #check the exceptional condition 
        path_start = path_indices[0]
        if cls.is_destination(path_start) and TYPE_OF_DESTINATION_INDEXED[path_start] == type_of_destination and cls.is_lower(path_start):
            return True
        #otherwise not traversible
        return False

    @classmethod
    def can_traverse(cls, path_indices, original_type, target_index, position_list):
        if cls.is_destination(target_index):
            return cls.is_target_destination_traversible(path_indices, original_type, target_index, position_list)
        else:
            #mids are always traversible
            return True

    @classmethod
    def can_stop(cls, path_indices, original_type, target_index, position_list):
        #can't stop if on a mid if we started on mid
        if cls.is_not_destination(path_indices[0]) and cls.is_not_destination(target_index):
            return False
        #can't stop on an upper if the lower is empty
        if cls.is_upper(target_index) and position_list[OTHER_DESTINATION_MAP_INDEXED[target_index]] == None:
            return False
        #can't stop on an upper destination that is ours if the lower is contains a different type
        if cls.is_upper(target_index) and position_list[OTHER_DESTINATION_MAP_INDEXED[target_index]] != original_type:
            return False
        #can't stop in any destination that isn't ours
        if cls.is_destination(target_index) and \
            TYPE_OF_DESTINATION_INDEXED[target_index] != original_type:
            return False
        #otherwise can stop
        return True
        
    def iterate_next_moves(self):
        count = 0
        for pos_index, pos_value in self.get_occupied_positions(self.positions):
            for next_path, next_distance in self._get_next_moves(pos_index, pos_value):
                #skip paths we have seen before
                if (pos_value, next_path) in self.paths:
                    debug(f"Skip visited path for {(pos_value, next_path)}")
                    continue
                #else yield the path
                cost = next_distance * MOVE_COST[pos_value]
                count += 1
                yield pos_value, next_path, next_distance, cost
        if count == 0:
            debug("No moves in iteration")

    def _get_next_moves(self, position_index, position_value):
        result = self._recurse_moves(position_index, position_value, [position_index], 0)
        return result

    def _get_available_destination(self, type_val):
        """Returns the (end of a) path for the destination of type_val and its length, or None,None
        if no destination is available"""
        upper_index, lower_index = DESTINATION_FOR_INDEXED[type_val]
        if self.positions[upper_index] is not None and self.positions[upper_index] != type_val:
            #a destination is occupied by another type
            return None, None
        if self.positions[lower_index] is not None and self.positions[lower_index] != type_val:
            #a destination is occupied by another type
            return None, None

        #check different combinations of the destinations
        if self.positions[upper_index] == type_val and self.positions[lower_index] == type_val:
            #full
            return None
        elif self.positions[upper_index] is None and self.positions[lower_index] == type_val:
            #upper empty, lower full
            return [upper_index], 0
        elif self.positions[upper_index] is None and self.positions[lower_index] is None:
            #both empty
            return [lower_index, upper_index], 1
        else:
            NotImplemented(f"Unhandled case: upper position {self.positions[upper_index]} and lower position {self.positions[lower_index]} for type {type_val}")

    def _recurse_moves(self, original_index, original_value, current_path_indices, current_path_length, depth=0):
        debug(" "*depth,"Recursing moves")
        debug(" "*depth,"original_index", original_index)
        debug(" "*depth,"original_value", original_value)
        debug(" "*depth,"current_path_indices", self.path_to_str(current_path_indices))
        debug(" "*depth,"current_path_length", current_path_length)

        next_moves = []
        #iterate the available moves from the end of the current path
        for next_index, next_distance in list(self.get_next_path_indices(current_path_indices, self.positions)):
            #skip destinations that aren't traversible
            if not self.can_traverse(current_path_indices, original_value, next_index, self.positions):
                continue

            debug(" "*depth, "next:", INDEX_TO_POSITION[next_index], next_index, next_distance)

            next_move = current_path_indices + [next_index]
            next_move_length = current_path_length + next_distance
            if self.can_stop(current_path_indices, original_value, next_index, self.positions):
                next_moves.append((next_move, next_move_length))

            # whether or not we save this position, recurse along clear paths
            # recurse to find other destinations we can stop at
            sub_moves = self._recurse_moves(original_index, original_value, list(next_move), next_move_length, depth+1)
            next_moves.extend(sub_moves)

        return next_moves

    @staticmethod
    def path_to_str(index_path):
        return str([ INDEX_TO_POSITION[i] for i in index_path ]) + "/" + str(index_path)

    def dump(self, depth=0):
        def to_str(val):
            if val is None:
                return "."
            return val

        mid_state_str = to_str(self.positions[POSITION_TO_INDEX[LL_POS]]) \
            + '.'.join([ to_str(self.positions[i]) for i in MID_POSITIONS_INDEXED ]) \
            + to_str(self.positions[POSITION_TO_INDEX[RR_POS]])
        upper_str = "#".join([ to_str(self.positions[i]) for i in UPPER_LOWER_MAP_INDEXED.keys() ])
        lower_str = "#".join([ to_str(self.positions[i]) for i in UPPER_LOWER_MAP_INDEXED.values() ])
        print(f"""
{" "*depth}#############
{" "*depth}#{mid_state_str}#
{" "*depth}###{upper_str}###
{" "*depth}  #{lower_str}#
{" "*depth}  #########""")
        # for t, p in self.paths:
        #     debug("   ",t,[ INDEX_TO_POSITION[i] for i in p ])

class StateTree:

    def __init__(self, initial_positions):
        self.min_cost = float('inf')
        self.min_cost_state = None
        self.initial_positions = initial_positions
        self.visited_states = dict() #map of the hash of the positions to the state object for visited states
        assert len(self.initial_positions) == len(POSITION_TO_INDEX)

        self.initial_state = State(initial_positions, 0, [])
        self.initial_state.dump()

    def iterate_states(self):
        #iterate the tree of states, terminating each branch when no options of lower cost than
        #the current min cost are available
        self.visited_states[hash(tuple(self.initial_state.positions))] = self.initial_state
        self._recurse_iterate_states(self.initial_state)
        assert self.min_cost_state is not None
        assert self.min_cost is not None

    def _recurse_iterate_states(self, state, depth=0):
        #get a list of single moves for the current state
        for type_value, path, path_distance, path_cost in state.iterate_next_moves():
            if self.min_cost is not None and  state.cost + path_cost > self.min_cost:
                #skip because cost too high
                continue
            new_state = state.apply_path(type_value, path, path_cost)
            # new_state.dump(depth)

            new_state_hash = hash(tuple(new_state.positions))
            try:
                already_seen = self.visited_states[new_state_hash]
                if already_seen.cost <= new_state.cost:
                    # print(" "*depth, "Halt at already seen state")
                    continue
            except KeyError:
                pass            
            self.visited_states[new_state_hash] = new_state

            if new_state.is_complete():
                print(" "*depth, "New state is complete")
                new_state.dump(depth)
                if new_state.cost < self.min_cost:
                    print(" "*depth, "New min state with cost", new_state.cost)
                    self.min_cost = new_state.cost
                    self.min_cost_state = new_state
            else:
                #not complete, so recurse
                self._recurse_iterate_states(new_state, depth+1)
        #done with moves at this level

def load_initial_positions(data):
    """Return a 2x4 position index"""

    def hash_parse(line):
        return [ i for i in line.split("#") if len(i.strip()) > 0 ]

    lines = data.strip().split("\n")
    assert len(lines) == 5
    positions = [
        hash_parse(lines[2]),
        hash_parse(lines[3]),
    ]
    position_map = [
        [AU_POS, BU_POS, CU_POS, DU_POS],
        [AL_POS, BL_POS, CL_POS, DL_POS],
    ]

    final_positions = [None]*len(POSITION_TO_INDEX)
    for row_val, row_map in zip(positions, position_map):
        for val, map_val in zip(row_val, row_map):
            final_positions[POSITION_TO_INDEX[map_val]] = val
    
    return final_positions



if __name__ == "__main__":
#test input
    data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
# debugging input
    data = """#############
#...........#
###A#B#C#D###
  #D#B#C#A#
  #########
"""

    # #real input
    # with open('day23.txt') as infile:
    #     data = infile.read()


    initial_positions = load_initial_positions(data)
    state_tree = StateTree(initial_positions)
    state_tree.iterate_states()
    print("Min cost state")
    state_tree.min_cost_state.dump()
    for p in state_tree.min_cost_state.paths:
        print("  ",p[0], [ INDEX_TO_POSITION[i] for i in p[1]])
    print('state tree min cost:', state_tree.min_cost)

    # Min cost state

    # #############
    # #...........#
    # ###A#B#C#D###
    #   #A#B#C#D#
    #   #########
    # state tree min cost: 15412
