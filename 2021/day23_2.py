from collections import namedtuple
from functools import total_ordering
from frozendict import frozendict as fd
from os import path, pathsep

def debug(*args):
    # pass
    print(*args)

A_TYPE="A"
B_TYPE="B"
C_TYPE="C"
D_TYPE="D"

MOVE_COST = fd({
    A_TYPE:1,
    B_TYPE:10,
    C_TYPE:100,
    D_TYPE:1000,
})


def pairwise(list_val):
    for l1, l2 in zip(list_val[:-1], list_val[1:]):
        yield l1, l2

Link = namedtuple("Link",["distance","position"])

class Position:

    def __init__(self, index, description, destination_for=None):
        self.index = index
        self.description = description
        self.destination_for = destination_for
        self._links = []

    def add_link(self, position, distance):
        self._links.append(Link(distance, position))

    def get_links(self):
        return self._links

    def iterate_links(self, filter=None):
        for p in self._links:
            if filter is None:
                yield p
            else:
                if filter(p):
                    yield p

    def __str__(self):
        return f"{self.description}-{self.index}"

    def __repr__(self):
        return self.__str__()


class PositionMap:

    def __init__(self, dest_count):
        self.dest_count = dest_count

        self.index_counter = 0
        self.destination_map = {}
        self.mid_list = []
        self.destination_list = []
        self._build_map()
        #build an index map
        self.index_position_map = { p.index: p for p in self.mid_list + self.destination_list }
        self.name_to_position_map = { p.description: p for p in self.mid_list + self.destination_list }

    def get_initialized_position(self, data):
        """Return a vector of initial values from the data"""

        def hash_parse(line):
            return [ i for i in line.split("#") if len(i.strip()) > 0 ]

        lines = data.strip().split("\n")
        assert len(lines) == self.dest_count + 3
        values = []
        for i in range(self.dest_count):
            values.append(hash_parse(lines[i+2]))

        index_list = [None]*len(self.index_position_map)
        for type_ind, target_dest in enumerate([A_TYPE, B_TYPE, C_TYPE, D_TYPE]):
            for row_ind in range(self.dest_count):
                dest_index = self.destination_map[target_dest][row_ind].index
                index_list[dest_index] = values[row_ind][type_ind]
        return index_list

    def is_complete(self, indexed_value_list):
        for type_val, positions in self.destination_map.items():
            for position in positions:
                if indexed_value_list[position.index] != type_val:
                    return False
        return True

    def _cross_link(self, p1, p2, dist):
        p1.add_link(p2, dist)
        p2.add_link(p1, dist)

    def _next_index(self):
        ret = self.index_counter
        self.index_counter += 1
        return ret

    def _create_destination(self, typeval):
        positions = []
        for i in range(self.dest_count):
            positions.append(Position(self._next_index(), f"{typeval}{i}", typeval))
        #make links both ways
        for p1, p2 in pairwise(positions):
            self._cross_link(p1,p2,1)
        self.destination_map[typeval] = positions
        self.destination_list.extend(positions)
        return positions

    def _build_map(self):
        #positions
        LL = Position(self._next_index(), "LL")
        LU = Position(self._next_index(), "LU")
        AB = Position(self._next_index(), "AB")
        BC = Position(self._next_index(), "BC")
        CD = Position(self._next_index(), "CD")
        RU = Position(self._next_index(), "RU")
        RL = Position(self._next_index(), "RL")
        self.mid_list = [LL, LU, AB, BC, CD, RU, RL]
        #add destinations for each type and link into the mid list
        a_list = self._create_destination(A_TYPE)
        self._cross_link(a_list[-1],LU,2)
        self._cross_link(a_list[-1],AB,2)
        b_list = self._create_destination(B_TYPE)
        self._cross_link(b_list[-1],AB,2)
        self._cross_link(b_list[-1],BC,2)
        c_list = self._create_destination(C_TYPE)
        self._cross_link(c_list[-1],BC,2)
        self._cross_link(c_list[-1],CD,2)
        d_list = self._create_destination(D_TYPE)
        self._cross_link(c_list[-1],CD,2)
        self._cross_link(c_list[-1],RU,2)
        #cross-link mids last, so their links will be at the ends of the lists
        self._cross_link(LL,LU,1)
        self._cross_link(LU,AB,2)
        self._cross_link(AB,BC,2)
        self._cross_link(BC,CD,2)
        self._cross_link(CD,RU,2)
        self._cross_link(RU,RL,1)

    def position_from_name(self, name_str):
        return self.name_to_position_map[name_str]

    ## Map helpers
    def is_final_destination(self, pos_index, indexed_value_list):
        assert self.is_destination(pos_index)
        pos_obj = self.index_position_map[pos_index]
        pos_obj_type = pos_obj.destination_for
        # make sure this object and all the objects below it are the final type
        pos_index_in_dest = self.get_destination_index(pos_index)
        for i in range(pos_index_in_dest+1):
            if indexed_value_list[self.destination_map[pos_obj_type][i].index] != pos_obj_type:
                return False
        #all of them match
        return True

    def all_lower_destinations_are_final(self, pos_index, indexed_value_list):
        assert self.is_destination(pos_index)
        pos_obj = self.index_position_map[pos_index]
        pos_obj_type = pos_obj.destination_for
        # make all the objects below it are the final type
        pos_index_in_dest = self.get_destination_index(pos_index)
        for i in range(pos_index_in_dest):
            if indexed_value_list[self.destination_map[pos_obj_type][i].index] != pos_obj_type:
                return False
        #all of them match
        return True

    def get_occupied_positions(self, indexed_value_list):
        for pos_index, pos_object in self.index_position_map.items():
            pos_value = indexed_value_list[pos_index]
            #skip empty
            if pos_value is None:
                continue
            #skip positions that are occupied in their final destinations
            if self.is_destination(pos_index) and self.is_final_destination(pos_index, indexed_value_list):
                continue
            #else return
            yield pos_index, pos_value

    def get_next_path_indices(self, path_indices, indexed_value_list):
        path_end = self.index_position_map[path_indices[-1]]
        for link in path_end.get_links():
            #skip occupied spaces
            if indexed_value_list[link.position.index] is not None:
                continue
            #skip if in path
            if link.position.index in path_indices:
                continue
            yield link

    def is_destination(self, position_index):
        return self.index_position_map[position_index].destination_for is not None

    def is_not_destination(self, position_index):
        return not self.is_destination(position_index)

    def get_destination_index(self, position_index):
        assert self.is_destination(position_index)
        pos_obj = self.index_position_map[position_index]
        dest_list = self.destination_map[pos_obj.destination_for]
        return dest_list.index(pos_obj)

    def is_target_destination_traversible(self, path_indices, original_type, target_index, indexed_value_list):
        assert self.is_destination(target_index)
        type_of_destination = self.index_position_map[target_index].destination_for
        #same type is always traversible
        if type_of_destination == original_type:
            return True
        #the rest is for different types
        #the upper is traversible if we started out in the lower
        #too long a path to traverse the upper
        if len(path_indices) > 1: 
            return False
        #check the exceptional condition where the path start is inside the destination of another type 
        path_start_ind = path_indices[0]
        if self.is_destination(path_start_ind):
            path_start_dest_ind = self.get_destination_index(path_start_ind)
            target_dest_ind = self.get_destination_index(target_index)        
            path_start = self.index_position_map[path_start_ind]
            #the path start is in the same destination as the target and the target is above it
            if self.is_destination(path_start_ind) and path_start.destination_for == type_of_destination and target_dest_ind > path_start_dest_ind:
                return True
        #otherwise not traversible
        return False

    def can_traverse(self, path_indices, original_type, target_index, indexed_value_list):
        if self.is_destination(target_index):
            return self.is_target_destination_traversible(path_indices, original_type, target_index, indexed_value_list)
        else:
            #mids are always traversible
            return True

    def can_stop(self, path_indices, original_type, target_index, indexed_value_list):
        #can't stop if on a mid if we started on mid
        if self.is_not_destination(path_indices[0]) and self.is_not_destination(target_index):
            return False
        #can't stop on a destination unless all the lower ones are full of the right kind
        if self.is_destination(target_index) and not self.all_lower_destinations_are_final(target_index, indexed_value_list):
            return False
        #can't stop in any destination that isn't ours
        if self.is_destination(target_index) and \
            self.index_position_map[target_index].destination_for != original_type:
            return False
        #otherwise can stop
        return True

    def dump(self, indexed_value_list, depth=0):
        def to_str(val):
            if val is None:
                return "."
            return val

        mid_state_str = to_str(indexed_value_list[self.mid_list[0].index]) \
            + '.'.join([ to_str(indexed_value_list[p.index]) for p in self.mid_list[1:-1] ]) \
            + to_str(indexed_value_list[self.mid_list[-1].index])
        row_strs=[]
        for row in range(self.dest_count):
            row_str = "#".join([ to_str(indexed_value_list[dest_list[row].index]) for dest_list in self.destination_map.values() ])
            row_strs.append(row_str)

        print(f"""
{" "*depth}#############
{" "*depth}#{mid_state_str}#
{" "*depth}###{row_strs[0]}###""")
        for rs in row_strs[1:]:
            print(f"""{" "*depth}  #{rs}#""")
        print(f"""{" "*depth}  #########""")
        # for t, p in self.paths:
        #     debug("   ",t,[ INDEX_TO_POSITION[i] for i in p ])




class State:

    def __init__(self, position_map, indexed_value_list, cost, paths):
        assert len(indexed_value_list) == len(position_map.index_position_map)
        self.position_map = position_map
        self.cost = cost
        self.indexed_value_list = indexed_value_list
        self.paths = paths

    def apply_path(self, type_value, path, path_cost):
        new_indexed_value_list = list(self.indexed_value_list)
        assert new_indexed_value_list[path[0]] == type_value
        for pind in path[1:]:
            assert new_indexed_value_list[pind] is None
        new_indexed_value_list[path[0]] = None
        new_indexed_value_list[path[-1]] = type_value
        return State(self.position_map, new_indexed_value_list, self.cost + path_cost, self.paths + [(type_value, path)])

    def iterate_next_moves(self):
        count = 0
        for pos_index, pos_value in self.position_map.get_occupied_positions(self.indexed_value_list):
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

    def _recurse_moves(self, original_index, original_value, current_path_indices, current_path_length, depth=0):
        debug(" "*depth,"Recursing moves")
        debug(" "*depth,"original_index", original_index)
        debug(" "*depth,"original_value", original_value)
        debug(" "*depth,"current_path_indices", self.path_to_str(current_path_indices))
        debug(" "*depth,"current_path_length", current_path_length)

        next_moves = []
        #iterate the available moves from the end of the current path
        for next_link in list(self.position_map.get_next_path_indices(current_path_indices, self.indexed_value_list)):
            next_index = next_link.position.index
            next_distance = next_link.distance
            #skip destinations that aren't traversible
            if not self.position_map.can_traverse(current_path_indices, original_value, next_index, self.indexed_value_list):
                continue

            debug(" "*depth, "next:", self.position_map.index_position_map[next_index], next_index, next_distance)

            next_move = current_path_indices + [next_index]
            next_move_length = current_path_length + next_distance
            if self.position_map.can_stop(current_path_indices, original_value, next_index, self.indexed_value_list):
                next_moves.append((next_move, next_move_length))

            # whether or not we save this position, recurse along clear paths
            # recurse to find other destinations we can stop at
            sub_moves = self._recurse_moves(original_index, original_value, list(next_move), next_move_length, depth+1)
            next_moves.extend(sub_moves)

        return next_moves

    def path_to_str(self, index_path):
        return str([ self.position_map.index_position_map[i] for i in index_path ]) + "/" + str(index_path)

    def dump(self, depth=0):
        self.position_map.dump(self.indexed_value_list, depth)



class StateTree:

    def __init__(self, position_map, initial_positions):
        self.position_map = position_map
        self.min_cost = float('inf')
        self.min_cost_state = None
        self.initial_positions = initial_positions
        self.visited_states = dict() #map of the hash of the positions to the state object for visited states
        assert len(self.initial_positions) == len(self.position_map.index_position_map)

        self.initial_state = State(self.position_map, initial_positions, 0, [])
        self.initial_state.dump()

    def iterate_states(self):
        #iterate the tree of states, terminating each branch when no options of lower cost than
        #the current min cost are available
        self.visited_states[hash(tuple(self.initial_state.indexed_value_list))] = self.initial_state
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

            new_state_hash = hash(tuple(new_state.indexed_value_list))
            try:
                already_seen = self.visited_states[new_state_hash]
                if already_seen.cost <= new_state.cost:
                    # print(" "*depth, "Halt at already seen state")
                    continue
            except KeyError:
                pass            
            self.visited_states[new_state_hash] = new_state

            if self.position_map.is_complete(new_state.indexed_value_list):
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




if __name__ == "__main__":
#test input
    data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
#debugging input
    data = """#############
#...........#
###A#B#C#D###
  #D#B#C#A#
  #########
"""

    # #real input
    # with open('day23.txt') as infile:
    #     data = infile.read()

    pm = PositionMap(2)
    initial_positions = pm.get_initialized_position(data)
    state_tree = StateTree(pm, initial_positions)
    state_tree.iterate_states()
    print("Min cost state")
    state_tree.min_cost_state.dump()
    print('state tree min cost:', state_tree.min_cost)

    # Min cost state

    # #############
    # #...........#
    # ###A#B#C#D###
    #   #A#B#C#D#
    #   #########
    # state tree min cost: 15412
