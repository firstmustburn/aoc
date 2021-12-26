from day23 import *


def to_pos_list(ind_list):
    return [ INDEX_TO_POSITION[i] for i in ind_list ]

def to_ind_list(pos_list):
    return [ POSITION_TO_INDEX[p] for p in pos_list ]

def print_path_info(info):
    info = list(info)
    info[1] = to_pos_list(info[1])
    print(tuple(info))

def test_day23_get_occupied_positions():
    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[LL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    results = list(State.get_occupied_positions(positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[LL_POS], A_TYPE) in results

    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[AU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    results = list(State.get_occupied_positions(positions))
    # print(results)

    assert len(results) == 4
    assert (POSITION_TO_INDEX[AU_POS], D_TYPE) in results
    assert (POSITION_TO_INDEX[BU_POS], C_TYPE) in results
    assert (POSITION_TO_INDEX[CU_POS], B_TYPE) in results
    assert (POSITION_TO_INDEX[DU_POS], A_TYPE) in results

    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[AU_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    results = list(State.get_occupied_positions(positions))
    # print(results)

    assert len(results) == 6
    assert (POSITION_TO_INDEX[AU_POS], A_TYPE) in results
    assert (POSITION_TO_INDEX[AL_POS], B_TYPE) in results
    assert (POSITION_TO_INDEX[BU_POS], B_TYPE) in results
    assert (POSITION_TO_INDEX[BL_POS], A_TYPE) in results
    assert (POSITION_TO_INDEX[CU_POS], D_TYPE) in results
    assert (POSITION_TO_INDEX[DU_POS], C_TYPE) in results

def test_day23_get_next_path_indices_1():

    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[LL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    path = [POSITION_TO_INDEX[LL_POS]] 

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[LR_POS], 1) in results

    path.append(POSITION_TO_INDEX[LR_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (POSITION_TO_INDEX[AU_POS], 2) in results
    assert (POSITION_TO_INDEX[AB_MID], 2) in results

    path.append(POSITION_TO_INDEX[AB_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (POSITION_TO_INDEX[AU_POS], 2) in results
    assert (POSITION_TO_INDEX[BC_MID], 2) in results

    path.append(POSITION_TO_INDEX[BC_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[CD_MID], 2) in results

    path.append(POSITION_TO_INDEX[CD_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[RL_POS], 2) in results

    path.append(POSITION_TO_INDEX[RL_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[RR_POS], 1) in results

    path.append(POSITION_TO_INDEX[RR_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 0



def test_day23_get_next_path_indices_2():

    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[RR_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    path = [POSITION_TO_INDEX[RR_POS]] 

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[RL_POS], 1) in results

    path.append(POSITION_TO_INDEX[RL_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[CD_MID], 2) in results

    path.append(POSITION_TO_INDEX[CD_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[BC_MID], 2) in results

    path.append(POSITION_TO_INDEX[BC_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 1
    assert (POSITION_TO_INDEX[AB_MID], 2) in results

    path.append(POSITION_TO_INDEX[AB_MID])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (POSITION_TO_INDEX[AU_POS], 2) in results
    assert (POSITION_TO_INDEX[LR_POS], 2) in results

    path.append(POSITION_TO_INDEX[LR_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 2
    assert (POSITION_TO_INDEX[AU_POS], 2) in results
    assert (POSITION_TO_INDEX[LL_POS], 1) in results

    path.append(POSITION_TO_INDEX[LL_POS])

    results = list(State.get_next_path_indices(path, positions))
    # print(results)

    assert len(results) == 0

def test_day23_is_destination():

    #LL
    assert not State.is_destination(0)
    assert State.is_not_destination(0)
    #LR
    assert not State.is_destination(1)
    assert State.is_not_destination(1)
    #AU
    assert State.is_destination(2)
    assert not State.is_not_destination(2)
    #AL
    assert State.is_destination(3)
    assert not State.is_not_destination(3)
    #BU
    assert State.is_destination(4)
    assert not State.is_not_destination(4)
    #BL
    assert State.is_destination(5)
    assert not State.is_not_destination(5)
    #CU
    assert State.is_destination(6)
    assert not State.is_not_destination(6)
    #CL
    assert State.is_destination(7)
    assert not State.is_not_destination(7)
    #DU
    assert State.is_destination(8)
    assert not State.is_not_destination(8)
    #DL
    assert State.is_destination(9)
    assert not State.is_not_destination(9)
    #AB
    assert not State.is_destination(10)
    assert State.is_not_destination(10)
    #BC
    assert not State.is_destination(11)
    assert State.is_not_destination(11)
    #CD
    assert not State.is_destination(12)
    assert State.is_not_destination(12)
    #RL
    assert not State.is_destination(13)
    assert State.is_not_destination(13)
    #RR
    assert not State.is_destination(14)
    assert State.is_not_destination(14)

def test_day23_can_traverse():
    assert State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[AU_POS], None)
    assert State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[AL_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[BU_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[BL_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[CU_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[CL_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[DU_POS], None)
    assert not State.can_traverse(None, A_TYPE, POSITION_TO_INDEX[DL_POS], None)

    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[AU_POS], None)
    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[AL_POS], None)
    assert State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[BU_POS], None)
    assert State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[BL_POS], None)
    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[CU_POS], None)
    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[CL_POS], None)
    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[DU_POS], None)
    assert not State.can_traverse(None, B_TYPE, POSITION_TO_INDEX[DL_POS], None)

    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[AU_POS], None)
    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[AL_POS], None)
    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[BU_POS], None)
    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[BL_POS], None)
    assert State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[CU_POS], None)
    assert State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[CL_POS], None)
    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[DU_POS], None)
    assert not State.can_traverse(None, C_TYPE, POSITION_TO_INDEX[DL_POS], None)

    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[AU_POS], None)
    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[AL_POS], None)
    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[BU_POS], None)
    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[BL_POS], None)
    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[CU_POS], None)
    assert not State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[CL_POS], None)
    assert State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[DU_POS], None)
    assert State.can_traverse(None, D_TYPE, POSITION_TO_INDEX[DL_POS], None)

def test_day23_can_stop():
    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[DL_POS]] = A_TYPE

    path = [
        POSITION_TO_INDEX[DL_POS], 
    ] 

    assert not State.can_stop(path, A_TYPE, POSITION_TO_INDEX[DL_POS], positions)

    path.append(POSITION_TO_INDEX[DU_POS])

    assert State.can_stop(path, A_TYPE, POSITION_TO_INDEX[CD_MID], positions)

    path.append(POSITION_TO_INDEX[CD_MID])

    assert State.can_stop(path, A_TYPE, POSITION_TO_INDEX[BC_MID], positions)

    path.append(POSITION_TO_INDEX[BC_MID])

    assert State.can_stop(path, A_TYPE, POSITION_TO_INDEX[AB_MID], positions)

    path.append(POSITION_TO_INDEX[AB_MID])

    assert not State.can_stop(path, A_TYPE, POSITION_TO_INDEX[AU_POS], positions)

    #set the lower to our type
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    #should be able to stop on the upper now
    assert State.can_stop(path, A_TYPE, POSITION_TO_INDEX[AU_POS], positions)

    #set the lower to another type
    positions[POSITION_TO_INDEX[AL_POS]] = D_TYPE
    #should not be able to stop on the upper now
    assert not State.can_stop(path, A_TYPE, POSITION_TO_INDEX[AU_POS], positions)

    #unset the lower to keep testing
    positions[POSITION_TO_INDEX[AL_POS]] = None


    path.append(POSITION_TO_INDEX[AU_POS])

    assert State.can_stop(path, A_TYPE, POSITION_TO_INDEX[AL_POS], positions)



def test_day23_state():

    # positions = [None]*len(POSITION_TO_INDEX)
    # positions[POSITION_TO_INDEX[LL_POS]] = A_TYPE
    # positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    # positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    # positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    # positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    # positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    # positions[POSITION_TO_INDEX[DU_POS]] = D_TYPE
    # positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    # expected = [
    #     (A_TYPE, to_ind_list([LL_POS, LR_POS, AU_POS]), 3, 3),
    #     (A_TYPE, to_ind_list([LL_POS, LR_POS, AB_MID, AU_POS]), 5, 5),
    # ]

    # state = State(positions, 0, [])
    # for path_info in state.iterate_next_moves():
    #     print_path_info(path_info)
    #     assert path_info in expected

    # positions = [None]*len(POSITION_TO_INDEX)
    # positions[POSITION_TO_INDEX[RR_POS]] = A_TYPE
    # positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    # positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    # positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    # positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    # positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    # positions[POSITION_TO_INDEX[DU_POS]] = D_TYPE
    # positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    # expected = [
    #     (A_TYPE, to_ind_list([RR_POS, RL_POS, CD_MID, BC_MID, AB_MID, AU_POS]), 9, 9),
    #     (A_TYPE, to_ind_list([RR_POS, RL_POS, CD_MID, BC_MID, AB_MID, LR_POS, AU_POS]), 11, 11),
    # ]

    # state = State(positions, 0, [])
    # for path_info in state.iterate_next_moves():
    #     print_path_info(path_info)
    #     assert path_info in expected

    positions = [None]*len(POSITION_TO_INDEX)
    positions[POSITION_TO_INDEX[AU_POS]] = D_TYPE
    positions[POSITION_TO_INDEX[AL_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[BU_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[BL_POS]] = B_TYPE
    positions[POSITION_TO_INDEX[CU_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[CL_POS]] = C_TYPE
    positions[POSITION_TO_INDEX[DU_POS]] = A_TYPE
    positions[POSITION_TO_INDEX[DL_POS]] = D_TYPE

    expected = [
        (A_TYPE, to_ind_list([RR_POS, RL_POS, CD_MID, BC_MID, AB_MID, AU_POS]), 9, 9),
        (A_TYPE, to_ind_list([RR_POS, RL_POS, CD_MID, BC_MID, AB_MID, LR_POS, AU_POS]), 11, 11),
    ]

    state = State(positions, 0, [])
    for path_info in state.iterate_next_moves():
        print_path_info(path_info)
        # assert path_info in expected

if __name__ == "__main__":

    test_day23_can_stop()