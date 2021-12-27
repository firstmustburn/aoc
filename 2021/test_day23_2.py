from day23_2 import *


# def to_pos_list(ind_list):
#     return [ INDEX_TO_POSITION[i] for i in ind_list ]

# def to_ind_list(pos_list):
#     return [ pm.position_from_name("p]").indexp in pos_list ]

# def print_path_info(info):
#     info = list(info)
#     info[1] = to_pos_list(info[1])
#     print(tuple(info))

def test_day23_2_get_occupied_positions():
    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("LL").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C1").index] = C_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = D_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    results = list(pm.get_occupied_positions(positions))
    print(results)

    assert len(results) == 1
    assert (pm.position_from_name("LL").index, A_TYPE) in results

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("A1").index] = D_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("B1").index] = C_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C1").index] = B_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = A_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    results = list(pm.get_occupied_positions(positions))
    # print(results)

    assert len(results) == 4
    assert (pm.position_from_name("A1").index, D_TYPE) in results
    assert (pm.position_from_name("B1").index, C_TYPE) in results
    assert (pm.position_from_name("C1").index, B_TYPE) in results
    assert (pm.position_from_name("D1").index, A_TYPE) in results

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("A1").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = B_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = A_TYPE
    positions[pm.position_from_name("C1").index] = D_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = C_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    results = list(pm.get_occupied_positions(positions))
    # print(results)

    assert len(results) == 6
    assert (pm.position_from_name("A1").index, A_TYPE) in results
    assert (pm.position_from_name("A0").index, B_TYPE) in results
    assert (pm.position_from_name("B1").index, B_TYPE) in results
    assert (pm.position_from_name("B0").index, A_TYPE) in results
    assert (pm.position_from_name("C1").index, D_TYPE) in results
    assert (pm.position_from_name("D1").index, C_TYPE) in results

def test_day23_2_get_next_path_indices_1():
    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("LL").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C1").index] = C_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = D_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    path = [pm.position_from_name("LL").index] 

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("LU"), 1) in results

    path.append(pm.position_from_name("LU").index)

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 2
    assert (pm.position_from_name("A1"), 2) in results
    assert (pm.position_from_name("AB"), 2) in results

    path.append(pm.position_from_name("AB").index)

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 2
    assert (pm.position_from_name("A1"), 2) in results
    assert (pm.position_from_name("BC"), 2) in results

    path.append(pm.position_from_name("BC").index)

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("CD"), 2) in results

    path.append(pm.position_from_name("CD").index)

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("RU"), 2) in results

    path.append(pm.position_from_name("RU").index)

    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("RL"), 1) in results

    path.append(pm.position_from_name("RL"))

    todo start here troubleshooting
    results = list(pm.get_next_path_indices(path, positions))
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 0



def test_day23_2_get_next_path_indices_2():
    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("RL").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C1").index] = C_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = D_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    path = [pm.position_from_name("RL").index] 

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (pm.position_from_name("RU").index, 1) in results

    path.append(pm.position_from_name("RU").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (pm.position_from_name("CD").index, 2) in results

    path.append(pm.position_from_name("CD").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (pm.position_from_name("BC").index, 2) in results

    path.append(pm.position_from_name("BC").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (pm.position_from_name("AB").index, 2) in results

    path.append(pm.position_from_name("AB").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (pm.position_from_name("A1").index, 2) in results
    assert (pm.position_from_name("LU").index, 2) in results

    path.append(pm.position_from_name("LU").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (pm.position_from_name("A1").index, 2) in results
    assert (pm.position_from_name("LL").index, 1) in results

    path.append(pm.position_from_name("LL").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 0

def test_day23_2_is_destination():

    pm = PositionMap(2)


    #LL
    assert not pm.is_destination(pm.position_from_name('LL').index)
    assert pm.is_not_destination(pm.position_from_name('LL').index)
    #LU
    assert not pm.is_destination(pm.position_from_name('LU').index)
    assert pm.is_not_destination(pm.position_from_name('LU').index)
    #A1
    assert pm.is_destination(pm.position_from_name('A1').index)
    assert not pm.is_not_destination(pm.position_from_name('A1').index)
    #A0
    assert pm.is_destination(pm.position_from_name('A0').index)
    assert not pm.is_not_destination(pm.position_from_name('A0').index)
    #B1
    assert pm.is_destination(pm.position_from_name('B1').index)
    assert not pm.is_not_destination(pm.position_from_name('B1').index)
    #B0
    assert pm.is_destination(pm.position_from_name('B0').index)
    assert not pm.is_not_destination(pm.position_from_name('B0').index)
    #C1
    assert pm.is_destination(pm.position_from_name('C1').index)
    assert not pm.is_not_destination(pm.position_from_name('C1').index)
    #C0
    assert pm.is_destination(pm.position_from_name('C0').index)
    assert not pm.is_not_destination(pm.position_from_name('C0').index)
    #D1
    assert pm.is_destination(pm.position_from_name('D1').index)
    assert not pm.is_not_destination(pm.position_from_name('D1').index)
    #D0
    assert pm.is_destination(pm.position_from_name('D0').index)
    assert not pm.is_not_destination(pm.position_from_name('D0').index)
    #AB
    assert not pm.is_destination(pm.position_from_name('AB').index)
    assert pm.is_not_destination(pm.position_from_name('AB').index)
    #BC
    assert not pm.is_destination(pm.position_from_name('BC').index)
    assert pm.is_not_destination(pm.position_from_name('BC').index)
    #CD
    assert not pm.is_destination(pm.position_from_name('CD').index)
    assert pm.is_not_destination(pm.position_from_name('CD').index)
    #RU
    assert not pm.is_destination(pm.position_from_name('RU').index)
    assert pm.is_not_destination(pm.position_from_name('RU').index)
    #RL
    assert not pm.is_destination(pm.position_from_name('RL').index)
    assert pm.is_not_destination(pm.position_from_name('RL').index)

def test_day23_2_can_traverse():
    pm = PositionMap(2)

    path = [ pm.position_from_name("LL").index ]

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A1").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A0").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B0").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C0").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D0").index, None)

    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("A1").index, None)
    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("A0").index, None)
    assert pm.can_traverse(path, B_TYPE, pm.position_from_name("B1").index, None)
    assert pm.can_traverse(path, B_TYPE, pm.position_from_name("B0").index, None)
    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("C1").index, None)
    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("C0").index, None)
    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("D1").index, None)
    assert not pm.can_traverse(path, B_TYPE, pm.position_from_name("D0").index, None)

    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("A1").index, None)
    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("A0").index, None)
    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("B1").index, None)
    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("B0").index, None)
    assert pm.can_traverse(path, C_TYPE, pm.position_from_name("C1").index, None)
    assert pm.can_traverse(path, C_TYPE, pm.position_from_name("C0").index, None)
    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("D1").index, None)
    assert not pm.can_traverse(path, C_TYPE, pm.position_from_name("D0").index, None)

    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("A1").index, None)
    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("A0").index, None)
    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("B1").index, None)
    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("B0").index, None)
    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("C1").index, None)
    assert not pm.can_traverse(path, D_TYPE, pm.position_from_name("C0").index, None)
    assert pm.can_traverse(path, D_TYPE, pm.position_from_name("D1").index, None)
    assert pm.can_traverse(path, D_TYPE, pm.position_from_name("D0").index, None)

def test_day23_2_can_stop():

    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("D0").index] = A_TYPE

    path = [
        pm.position_from_name("D0").index, 
    ] 

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D0").index, positions)

    path.append(pm.position_from_name("D1").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("CD").index, positions)

    path.append(pm.position_from_name("CD").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("BC").index, positions)

    path.append(pm.position_from_name("BC").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("AB").index, positions)

    path.append(pm.position_from_name("AB").index)

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)

    #set the lower to our type
    positions[pm.position_from_name("A0").index] = A_TYPE
    #should be aB0e to stop on the upper now
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)

    #set the lower to another type
    positions[pm.position_from_name("A0").index] = D_TYPE
    #should not be aB0e to stop on the upper now
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)

    #unset the lower to keep testing
    positions[pm.position_from_name("A0").index] = None


    path.append(pm.position_from_name("A1").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A0").index, positions)

def test_day23_2_all_lower_destinations_are_final():

    # 2 deep map with blanks

    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)

    assert pm.all_lower_destinations_are_final(pm.position_from_name("A0").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)

    positions[pm.position_from_name("A0").index] = A_TYPE

    assert pm.all_lower_destinations_are_final(pm.position_from_name("A0").index, positions)
    assert pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)

    # 4 deep map with blanks

    pm = PositionMap(4)

    positions = [None]*len(pm.index_position_map)

    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)

    positions[pm.position_from_name("A0").index] = A_TYPE

    assert pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)


    positions[pm.position_from_name("A1").index] = A_TYPE

    assert pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)


    positions[pm.position_from_name("A2").index] = A_TYPE

    assert pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)

    # 4 deep map with other entries

    pm = PositionMap(4)

    positions = [None]*len(pm.index_position_map)

    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)

    positions[pm.position_from_name("A0").index] = B_TYPE

    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)

    positions[pm.position_from_name("A1").index] = A_TYPE

    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)

    positions[pm.position_from_name("A2").index] = A_TYPE

    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A1").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A2").index, positions)
    assert not pm.all_lower_destinations_are_final(pm.position_from_name("A3").index, positions)


# def test_day23_2_state():

#     pm = PositionMap(2)


    # positions = [None]*len(pm.index_position_map)
    # positions[pm.position_from_name("LL").index] = A_TYPE
    # positions[pm.position_from_name("A0").index] = A_TYPE
    # positions[pm.position_from_name("B1").index] = B_TYPE
    # positions[pm.position_from_name("B0").index] = B_TYPE
    # positions[pm.position_from_name("C1").index] = C_TYPE
    # positions[pm.position_from_name("C0").index] = C_TYPE
    # positions[pm.position_from_name("D1").index] = D_TYPE
    # positions[pm.position_from_name("D0").index] = D_TYPE

    # expected = [
    #     (A_TYPE, to_ind_list([LL_POS, LU_POS, A1_POS]), 3, 3),
    #     (A_TYPE, to_ind_list([LL_POS, LU_POS, AB_MID, A1_POS]), 5, 5),
    # ]

    # state = State(positions, 0, [])
    # for path_info in state.iterate_next_moves():
    #     print_path_info(path_info)
    #     assert path_info in expected

    # positions = [None]*len(pm.index_position_map)
    # positions[pm.position_from_name("RL").index] = A_TYPE
    # positions[pm.position_from_name("A0").index] = A_TYPE
    # positions[pm.position_from_name("B1").index] = B_TYPE
    # positions[pm.position_from_name("B0").index] = B_TYPE
    # positions[pm.position_from_name("C1").index] = C_TYPE
    # positions[pm.position_from_name("C0").index] = C_TYPE
    # positions[pm.position_from_name("D1").index] = D_TYPE
    # positions[pm.position_from_name("D0").index] = D_TYPE

    # expected = [
    #     (A_TYPE, to_ind_list([RL_POS, RU_POS, CD_MID, BC_MID, AB_MID, A1_POS]), 9, 9),
    #     (A_TYPE, to_ind_list([RL_POS, RU_POS, CD_MID, BC_MID, AB_MID, LU_POS, A1_POS]), 11, 11),
    # ]

    # state = State(positions, 0, [])
    # for path_info in state.iterate_next_moves():
    #     print_path_info(path_info)
    #     assert path_info in expected

    # positions = [None]*len(pm.index_position_map)
    # positions[pm.position_from_name("A1").index] = D_TYPE
    # positions[pm.position_from_name("A0").index] = A_TYPE
    # positions[pm.position_from_name("B1").index] = B_TYPE
    # positions[pm.position_from_name("B0").index] = B_TYPE
    # positions[pm.position_from_name("C1").index] = C_TYPE
    # positions[pm.position_from_name("C0").index] = C_TYPE
    # positions[pm.position_from_name("D1").index] = A_TYPE
    # positions[pm.position_from_name("D0").index] = D_TYPE

    # expected = [
    #     (A_TYPE, to_ind_list([RL_POS, RU_POS, CD_MID, BC_MID, AB_MID, A1_POS]), 9, 9),
    #     (A_TYPE, to_ind_list([RL_POS, RU_POS, CD_MID, BC_MID, AB_MID, LU_POS, A1_POS]), 11, 11),
    # ]

    # state = State(positions, 0, [])
    # for path_info in state.iterate_next_moves():
    #     print_path_info(path_info)
        # assert path_info in expected

if __name__ == "__main__":

    test_day23_2_can_stop()