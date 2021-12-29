from day23_2 import *
from io import StringIO 


# def to_pos_list(ind_list):
#     return [ INDEX_TO_POSITION[i] for i in ind_list ]

# def to_ind_list(pos_list):
#     return [ pm.position_from_name("p]").indexp in pos_list ]

# def print_path_info(info):
#     info = list(info)
#     info[1] = to_pos_list(info[1])
#     print(tuple(info))


def test_day23_2_test_links():
    pm = PositionMap(2)
    p = pm.position_from_name('A0')
    assert p.get_links() == [Link(1, pm.position_from_name('A1'))]
    p = pm.position_from_name('A1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('A0')),
        Link(2, pm.position_from_name('LU')),
        Link(2, pm.position_from_name('AB')),
    ]

    p = pm.position_from_name('B0')
    assert p.get_links() == [Link(1, pm.position_from_name('B1'))]
    p = pm.position_from_name('B1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('B0')),
        Link(2, pm.position_from_name('AB')),
        Link(2, pm.position_from_name('BC')),
    ]

    p = pm.position_from_name('C0')
    assert p.get_links() == [Link(1, pm.position_from_name('C1'))]
    p = pm.position_from_name('C1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('C0')),
        Link(2, pm.position_from_name('BC')),
        Link(2, pm.position_from_name('CD')),
    ]

    p = pm.position_from_name('D0')
    assert p.get_links() == [Link(1, pm.position_from_name('D1'))]
    p = pm.position_from_name('D1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('D0')),
        Link(2, pm.position_from_name('CD')),
        Link(2, pm.position_from_name('RU')),
    ]

    p = pm.position_from_name('LL')
    assert p.get_links() == [Link(1, pm.position_from_name('LU'))]
    p = pm.position_from_name('LU')
    assert p.get_links() == [
        Link(2, pm.position_from_name('A1')),
        Link(1, pm.position_from_name('LL')),
        Link(2, pm.position_from_name('AB')),
    ]

    p = pm.position_from_name('RL')
    assert p.get_links() == [Link(1, pm.position_from_name('RU'))]
    p = pm.position_from_name('RU')
    assert p.get_links() == [
        Link(2, pm.position_from_name('D1')),
        Link(2, pm.position_from_name('CD')),
        Link(1, pm.position_from_name('RL')),
    ]

    p = pm.position_from_name('AB')
    assert p.get_links() == [
        Link(2, pm.position_from_name('A1')),
        Link(2, pm.position_from_name('B1')),
        Link(2, pm.position_from_name('LU')),
        Link(2, pm.position_from_name('BC')),
    ]

    p = pm.position_from_name('BC')
    assert p.get_links() == [
        Link(2, pm.position_from_name('B1')),
        Link(2, pm.position_from_name('C1')),
        Link(2, pm.position_from_name('AB')),
        Link(2, pm.position_from_name('CD')),
    ]

    p = pm.position_from_name('CD')
    assert p.get_links() == [
        Link(2, pm.position_from_name('C1')),
        Link(2, pm.position_from_name('D1')),
        Link(2, pm.position_from_name('BC')),
        Link(2, pm.position_from_name('RU')),
    ]

def test_day23_2_test_links_4():
    pm = PositionMap(4)
    p = pm.position_from_name('A0')
    assert p.get_links() == [Link(1, pm.position_from_name('A1'))]
    p = pm.position_from_name('A1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('A0')),
        Link(1, pm.position_from_name('A2')),
    ]
    p = pm.position_from_name('A2')
    assert p.get_links() == [
        Link(1, pm.position_from_name('A1')),
        Link(1, pm.position_from_name('A3')),
    ]
    p = pm.position_from_name('A3')
    assert p.get_links() == [
        Link(1, pm.position_from_name('A2')),
        Link(2, pm.position_from_name('LU')),
        Link(2, pm.position_from_name('AB')),
    ]

    p = pm.position_from_name('B0')
    assert p.get_links() == [Link(1, pm.position_from_name('B1'))]
    p = pm.position_from_name('B1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('B0')),
        Link(1, pm.position_from_name('B2')),
    ]
    p = pm.position_from_name('B2')
    assert p.get_links() == [
        Link(1, pm.position_from_name('B1')),
        Link(1, pm.position_from_name('B3')),
    ]
    p = pm.position_from_name('B3')
    assert p.get_links() == [
        Link(1, pm.position_from_name('B2')),
        Link(2, pm.position_from_name('AB')),
        Link(2, pm.position_from_name('BC')),
    ]

    p = pm.position_from_name('C0')
    assert p.get_links() == [Link(1, pm.position_from_name('C1'))]
    p = pm.position_from_name('C1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('C0')),
        Link(1, pm.position_from_name('C2')),
    ]
    p = pm.position_from_name('C2')
    assert p.get_links() == [
        Link(1, pm.position_from_name('C1')),
        Link(1, pm.position_from_name('C3')),
    ]
    p = pm.position_from_name('C3')
    assert p.get_links() == [
        Link(1, pm.position_from_name('C2')),
        Link(2, pm.position_from_name('BC')),
        Link(2, pm.position_from_name('CD')),
    ]

    p = pm.position_from_name('D0')
    assert p.get_links() == [Link(1, pm.position_from_name('D1'))]
    p = pm.position_from_name('D1')
    assert p.get_links() == [
        Link(1, pm.position_from_name('D0')),
        Link(1, pm.position_from_name('D2')),
    ]
    p = pm.position_from_name('D2')
    assert p.get_links() == [
        Link(1, pm.position_from_name('D1')),
        Link(1, pm.position_from_name('D3')),
    ]
    p = pm.position_from_name('D3')
    assert p.get_links() == [
        Link(1, pm.position_from_name('D2')),
        Link(2, pm.position_from_name('CD')),
        Link(2, pm.position_from_name('RU')),
    ]

    p = pm.position_from_name('LL')
    assert p.get_links() == [Link(1, pm.position_from_name('LU'))]
    p = pm.position_from_name('LU')
    assert p.get_links() == [
        Link(2, pm.position_from_name('A3')),
        Link(1, pm.position_from_name('LL')),
        Link(2, pm.position_from_name('AB')),
    ]

    p = pm.position_from_name('RL')
    assert p.get_links() == [Link(1, pm.position_from_name('RU'))]
    p = pm.position_from_name('RU')
    assert p.get_links() == [
        Link(2, pm.position_from_name('D3')),
        Link(2, pm.position_from_name('CD')),
        Link(1, pm.position_from_name('RL')),
    ]

    p = pm.position_from_name('AB')
    assert p.get_links() == [
        Link(2, pm.position_from_name('A3')),
        Link(2, pm.position_from_name('B3')),
        Link(2, pm.position_from_name('LU')),
        Link(2, pm.position_from_name('BC')),
    ]

    p = pm.position_from_name('BC')
    assert p.get_links() == [
        Link(2, pm.position_from_name('B3')),
        Link(2, pm.position_from_name('C3')),
        Link(2, pm.position_from_name('AB')),
        Link(2, pm.position_from_name('CD')),
    ]

    p = pm.position_from_name('CD')
    assert p.get_links() == [
        Link(2, pm.position_from_name('C3')),
        Link(2, pm.position_from_name('D3')),
        Link(2, pm.position_from_name('BC')),
        Link(2, pm.position_from_name('RU')),
    ]

def test_day23_2_get_occupied_positions_4():
    pm = PositionMap(4)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("LU").index] = A_TYPE
    positions[pm.position_from_name("A2").index] = A_TYPE
    positions[pm.position_from_name("A1").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("AB").index] = B_TYPE
    positions[pm.position_from_name("B2").index] = B_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C3").index] = C_TYPE
    positions[pm.position_from_name("C2").index] = D_TYPE
    positions[pm.position_from_name("C1").index] = C_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D3").index] = D_TYPE
    positions[pm.position_from_name("D2").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = D_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    results = list(pm.get_occupied_positions(positions))
    print(results)

    assert len(results) == 6
    assert (pm.position_from_name("LU").index, A_TYPE) in results
    assert (pm.position_from_name("AB").index, B_TYPE) in results
    assert (pm.position_from_name("C3").index, C_TYPE) in results
    assert (pm.position_from_name("C2").index, D_TYPE) in results
    assert (pm.position_from_name("D3").index, D_TYPE) in results
    assert (pm.position_from_name("D2").index, C_TYPE) in results


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


def test_day23_2_get_next_path_indices_4_1():
    pm = PositionMap(4)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("LU").index] = A_TYPE
    positions[pm.position_from_name("A2").index] = A_TYPE
    positions[pm.position_from_name("A1").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = A_TYPE
    positions[pm.position_from_name("CD").index] = B_TYPE
    positions[pm.position_from_name("B2").index] = B_TYPE
    positions[pm.position_from_name("B1").index] = B_TYPE
    positions[pm.position_from_name("B0").index] = B_TYPE
    positions[pm.position_from_name("C3").index] = C_TYPE
    positions[pm.position_from_name("C2").index] = D_TYPE
    positions[pm.position_from_name("C1").index] = C_TYPE
    positions[pm.position_from_name("C0").index] = C_TYPE
    positions[pm.position_from_name("D3").index] = D_TYPE
    positions[pm.position_from_name("D2").index] = C_TYPE
    positions[pm.position_from_name("D1").index] = D_TYPE
    positions[pm.position_from_name("D0").index] = D_TYPE

    path = [pm.position_from_name("LU").index] 

    results = list(pm.get_next_path_indices(path, positions))

    assert len(results) == 3
    assert Link(2, pm.position_from_name("A3")) in results
    assert Link(2, pm.position_from_name("AB")) in results
    assert Link(1, pm.position_from_name("LL")) in results

    path.append(pm.position_from_name("LL").index) 

    results = list(pm.get_next_path_indices(path, positions))

    assert len(results) == 0

    path = [
        pm.position_from_name("LU").index,
        pm.position_from_name("AB").index,
    ] 

    results = list(pm.get_next_path_indices(path, positions))
    print(results)

    assert len(results) == 3
    assert Link(2, pm.position_from_name("A3")) in results
    assert Link(2, pm.position_from_name("B3")) in results
    assert Link(2, pm.position_from_name("BC")) in results



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

    path.append(pm.position_from_name("RL").index)

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
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("RU"), 1) in results

    path.append(pm.position_from_name("RU").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("CD"), 2) in results

    path.append(pm.position_from_name("CD").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("BC"), 2) in results

    path.append(pm.position_from_name("BC").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 1
    assert (pm.position_from_name("AB"), 2) in results

    path.append(pm.position_from_name("AB").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 2
    assert (pm.position_from_name("A1"), 2) in results
    assert (pm.position_from_name("LU"), 2) in results

    path.append(pm.position_from_name("LU").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 2
    assert (pm.position_from_name("A1"), 2) in results
    assert (pm.position_from_name("LL"), 1) in results

    path.append(pm.position_from_name("LL").index)

    results = list(pm.get_next_path_indices(path, positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 0

def path_indices_from_names(pm, names):
    return [ pm.position_from_name(n).index for n in names ]

def test_day23_2_simple_case():
    pm = PositionMap(2)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("A1").index] = A_TYPE
    positions[pm.position_from_name("A0").index] = D_TYPE

    results = list(pm.get_occupied_positions(positions))
    print(results)

    assert len(results) == 2
    assert (pm.position_from_name("A1").index, 'A') in results
    assert (pm.position_from_name("A0").index, 'D') in results

    #A should have multiple positions
    results = list(pm.get_next_path_indices([8], positions))
    # print(results)
    #convert links
    results = [ (l.position, l.distance) for l in results ]

    assert len(results) == 2
    assert (pm.position_from_name("LU"), 2) in results
    assert (pm.position_from_name("AB"), 2) in results

    results = list(pm.get_next_path_indices([7], positions))
    assert len(results) == 0


    state = State(pm, positions, 0, [])
    results = state.get_next_moves()
    #print decoded results
    for r in results:
        print(r[0], [ pm.index_position_map[i] for i in r[1] ])

    assert len(results) == 14
    path_indices_from_names(pm, ['A1', 'LU'])
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'LL'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'AB'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'AB', 'BC'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'AB', 'BC', 'CD'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'AB', 'BC', 'CD', 'RU'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'LU', 'AB', 'BC', 'CD', 'RU', 'RL'])) in results
  
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'LU'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'LU', 'LL'])) in results
    
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'BC'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'BC', 'CD'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'BC', 'CD', 'RU'])) in results
    assert (A_TYPE, path_indices_from_names(pm, ['A1', 'AB', 'BC', 'CD', 'RU', 'RL'])) in results




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


    pm = PositionMap(4)


    #LL
    assert not pm.is_destination(pm.position_from_name('LL').index)
    assert pm.is_not_destination(pm.position_from_name('LL').index)
    #LU
    assert not pm.is_destination(pm.position_from_name('LU').index)
    assert pm.is_not_destination(pm.position_from_name('LU').index)
    #A3
    assert pm.is_destination(pm.position_from_name('A3').index)
    assert not pm.is_not_destination(pm.position_from_name('A3').index)
    #A2
    assert pm.is_destination(pm.position_from_name('A2').index)
    assert not pm.is_not_destination(pm.position_from_name('A2').index)
    #A1
    assert pm.is_destination(pm.position_from_name('A1').index)
    assert not pm.is_not_destination(pm.position_from_name('A1').index)
    #A0
    assert pm.is_destination(pm.position_from_name('A0').index)
    assert not pm.is_not_destination(pm.position_from_name('A0').index)


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

def test_day23_2_can_traverse_4():
    pm = PositionMap(4)

    path = [ pm.position_from_name("LU").index ]

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("LU").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A3").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A2").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A1").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("A0").index, None)
    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("AB").index, None)
    
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B3").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B2").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("B0").index, None)

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("BC").index, None)

    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C3").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C2").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("C0").index, None)

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("CD").index, None)

    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D3").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D2").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D1").index, None)
    assert not pm.can_traverse(path, A_TYPE, pm.position_from_name("D0").index, None)

    #path starting from 0 in another destination

    path = [ pm.position_from_name("B0").index ]

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("B1").index, None)

    path.append(pm.position_from_name("B1").index )

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("B2").index, None)

    path.append(pm.position_from_name("B2").index )

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("B3").index, None)

    #path starting from 1 in another destinagion

    path = [ pm.position_from_name("B1").index ]

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("B2").index, None)

    path.append(pm.position_from_name("B2").index )

    assert pm.can_traverse(path, A_TYPE, pm.position_from_name("B3").index, None)


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


def test_day23_2_can_stop_4():

    pm = PositionMap(4)

    positions = [None]*len(pm.index_position_map)
    positions[pm.position_from_name("D0").index] = A_TYPE

    path = [
        pm.position_from_name("D0").index, 
    ] 

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D1").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D3").index, positions)

    path.append(pm.position_from_name("D1").index)

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D3").index, positions)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("CD").index, positions)

    path.append(pm.position_from_name("D2").index)

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("D3").index, positions)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("CD").index, positions)

    path.append(pm.position_from_name("D3").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("CD").index, positions)

    path.append(pm.position_from_name("CD").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("BC").index, positions)
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("RU").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("B3").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("C3").index, positions)

    path.append(pm.position_from_name("BC").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("AB").index, positions)
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("CD").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("B1").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("C1").index, positions)

    path.append(pm.position_from_name("AB").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("LU").index, positions)

    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A3").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)

    #set the lower to our type
    positions[pm.position_from_name("A0").index] = A_TYPE
    #should be able to stop on the upper now
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A3").index, positions)

    #set the lower to our type
    positions[pm.position_from_name("A1").index] = A_TYPE
    #should be able to stop on the upper now
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A3").index, positions)

    #set the lower to our type
    positions[pm.position_from_name("A2").index] = A_TYPE
    #should be able to stop on the upper now
    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A3").index, positions)

    #set the lower to another type
    positions[pm.position_from_name("A0").index] = D_TYPE
    positions[pm.position_from_name("A1").index] = None
    positions[pm.position_from_name("A2").index] = None
    positions[pm.position_from_name("A3").index] = None
    #should not be aB0e to stop on the upper now
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A1").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A2").index, positions)
    assert not pm.can_stop(path, A_TYPE, pm.position_from_name("A3").index, positions)

    #unset the lower to keep testing
    positions[pm.position_from_name("A0").index] = None

    path.append(pm.position_from_name("A3").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A0").index, positions)

    path.append(pm.position_from_name("A2").index)

    assert pm.can_stop(path, A_TYPE, pm.position_from_name("A0").index, positions)

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


class DebugPrinterForTest:

    def __init__(self):
        self.sbuf = StringIO()

    def __call__(self, *args, depth=0):
        print(*args, file=self.sbuf)        

def test_day23_2_get_initialized_position():

    pm = PositionMap(2)

    data = """#############
#...........#
###A#C#B#D###
  #D#B#C#A#
  #########
"""
    ip = pm.get_initialized_position(data)
    print(ip)
    assert ip[pm.position_from_name('LL').index] == None
    assert ip[pm.position_from_name('LU').index] == None
    assert ip[pm.position_from_name('AB').index] == None
    assert ip[pm.position_from_name('BC').index] == None
    assert ip[pm.position_from_name('CD').index] == None
    assert ip[pm.position_from_name('RU').index] == None
    assert ip[pm.position_from_name('RL').index] == None
    assert ip[pm.position_from_name('A1').index] == A_TYPE
    assert ip[pm.position_from_name('A0').index] == D_TYPE
    assert ip[pm.position_from_name('B1').index] == C_TYPE
    assert ip[pm.position_from_name('B0').index] == B_TYPE
    assert ip[pm.position_from_name('C1').index] == B_TYPE
    assert ip[pm.position_from_name('C0').index] == C_TYPE
    assert ip[pm.position_from_name('D1').index] == D_TYPE
    assert ip[pm.position_from_name('D0').index] == A_TYPE

    state = State(pm, ip, 0, [])
    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    #also test state iteration

    ################################################################################################
    # iteration to LU

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('LU').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == A_TYPE
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#.A.........#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to LU

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('LU').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == A_TYPE
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#A..........#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to AB

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('AB').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == None
    assert iv[pm.position_from_name('AB').index] == A_TYPE
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#...A.......#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to BC

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('AB').index,pm.position_from_name('BC').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == None
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == A_TYPE
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#.....A.....#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to CD

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('AB').index,pm.position_from_name('BC').index,pm.position_from_name('CD').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == None
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == A_TYPE
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#.......A...#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to RU

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('AB').index,
        pm.position_from_name('BC').index,pm.position_from_name('CD').index,
        pm.position_from_name('RU').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == None
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == A_TYPE
    assert iv[pm.position_from_name('RL').index] == None
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#.........A.#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()

    ################################################################################################
    # iteration to RL

    new_path = [pm.position_from_name('A1').index,pm.position_from_name('AB').index,
        pm.position_from_name('BC').index,pm.position_from_name('CD').index,
        pm.position_from_name('RU').index,pm.position_from_name('RL').index]
    new_state = state.apply_path(A_TYPE, new_path)

    iv = new_state.indexed_value_list
    assert iv[pm.position_from_name('LL').index] == None
    assert iv[pm.position_from_name('LU').index] == None
    assert iv[pm.position_from_name('AB').index] == None
    assert iv[pm.position_from_name('BC').index] == None
    assert iv[pm.position_from_name('CD').index] == None
    assert iv[pm.position_from_name('RU').index] == None
    assert iv[pm.position_from_name('RL').index] == A_TYPE
    assert iv[pm.position_from_name('A1').index] == None
    assert iv[pm.position_from_name('A0').index] == D_TYPE
    assert iv[pm.position_from_name('B1').index] == C_TYPE
    assert iv[pm.position_from_name('B0').index] == B_TYPE
    assert iv[pm.position_from_name('C1').index] == B_TYPE
    assert iv[pm.position_from_name('C0').index] == C_TYPE
    assert iv[pm.position_from_name('D1').index] == D_TYPE
    assert iv[pm.position_from_name('D0').index] == A_TYPE

    refdata = """#############
#..........A#
###.#C#B#D###
  #D#B#C#A#
  #########
"""

    td = DebugPrinterForTest()
    state.dump(debug_function=td)
    assert td.sbuf.getvalue().strip() == data.strip()



def test_day23_2_4_troubleshoot():
    pm = PositionMap(4)

    watch_data = """#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########"""
    iv = pm.get_initialized_position(watch_data)
    state = State(pm, iv, 0, [])
    state.dump(debug_function=debug1)
    for type_value, path in state.get_next_moves():
        print(type_value, [ pm.position_from_index(pv) for pv in path ])

    assert False


if __name__ == "__main__":

    test_day23_2_4_troubleshoot()