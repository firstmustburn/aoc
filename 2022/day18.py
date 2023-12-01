from __future__ import annotations
from typing import List, Tuple, Set

from pprint import pprint
from collections import namedtuple

# voxel model is that the area in the +x,y,z direction from the point is occupied by the voxel
Voxel = namedtuple('Voxel',['x','y','z'])

def load_input(filename) -> Set[Voxel]:
    voxels = set()
    with open(filename) as infile:
        for line in infile:
            voxels.add(Voxel(*[ int(v) for v in line.strip().split(',')] ))
    return voxels

def get_ranges(voxels: Set[Voxel]) -> Tuple[Voxel, Voxel]:
    x_list = [ v.x for v in voxels ]
    y_list = [ v.y for v in voxels ]
    z_list = [ v.z for v in voxels ]
    xmin = min(x_list)
    xmax = max(x_list)
    ymin = min(y_list)
    ymax = max(y_list)
    zmin = min(z_list)
    zmax = max(z_list)
    return Voxel(xmin, ymin, zmin), Voxel(xmax, ymax, zmax)

def sweep(voxels: Set[Voxel], vmin: Voxel, vmax: Voxel) -> int:
    surface_count = 0
    #sweep an XY plan through zmin/zmax and count the plane boundaries
    for z in range(vmin.z, vmax.z+2): #+2 to check the farthes voxel boundaries
        for x in range(vmin.x, vmax.x+1):
            for y in range(vmin.y, vmax.y+1):
                if  (Voxel(x,y,z) in voxels) != (Voxel(x,y,z-1) in voxels):
                    surface_count += 1
    #sweep a YZ plan through xmin/xmax and count the plane boundaries
    for x in range(vmin.x, vmax.x+2): #+2 to check the farthes voxel boundaries
        for y in range(vmin.y, vmax.y+1):
            for z in range(vmin.z, vmax.z+1):
                if  (Voxel(x,y,z) in voxels) != (Voxel(x-1,y,z) in voxels):
                    surface_count += 1
    #sweep a XZ plan through ymin/ymax and count the plane boundaries
    for y in range(vmin.y, vmax.y+2): #+2 to check the farthes voxel boundaries
        for x in range(vmin.x, vmax.x+1):
            for z in range(vmin.z, vmax.z+1):
                if  (Voxel(x,y,z) in voxels) != (Voxel(x,y-1,z) in voxels):
                    surface_count += 1
    return surface_count

def find_connected_empty_space(occupied_voxel_groups: List[Set[Voxel]], start: Voxel, vmin: Voxel, vmax: Voxel) -> int:

    def is_occupied(v):
        for vg in occupied_voxel_groups:
            if v in vg:
                return True
        return False

    assert not is_occupied(start)

    empty_group:Set[Voxel] = set()
    
    #iterate instead of recurse

    def can_iterate(v):
        if (v.x < vmin.x or v.x > vmax.x) or (v.y < vmin.y or v.y > vmax.y) or (v.z < vmin.z or v.z > vmax.z):
            #stop iterating when we leave the overall volume
            return False
        if is_occupied(v):
            #stop iterating when we hit an occupied voxel
            return False
        if v in empty_group:
            # stop interating when we hit a voxel we are already connected to
            return False
        return True

    def connect_empty_space(v: Voxel, connected: Set[Voxel]) -> Set[Voxel]:
        #not occupied, so add to connected
        connected.add(v)
        # print("Connected",v)
        neighbors_to_check = set()
        for delta in [1,-1]:
            neighbor = Voxel(v.x + delta, v.y, v.z)
            if can_iterate(neighbor):
                neighbors_to_check.add(neighbor)

            neighbor = Voxel(v.x, v.y + delta, v.z)
            if can_iterate(neighbor):
                neighbors_to_check.add(neighbor)

            neighbor = Voxel(v.x, v.y, v.z + delta)
            if can_iterate(neighbor):
                neighbors_to_check.add(neighbor)
        return neighbors_to_check

    assert can_iterate(start)
    current_neighbors = connect_empty_space(start, empty_group)
    while current_neighbors:
        next_neighbors = set()
        for n in current_neighbors:
            immediate_neighbors = connect_empty_space(n, empty_group)
            next_neighbors.update(immediate_neighbors)
        current_neighbors = next_neighbors
    return empty_group

def part1(voxels: Set[Voxel]):
    vmin, vmax = get_ranges(voxels)
    print(vmin, vmax)
    return sweep(voxels, vmin, vmax)

def part2(occupied_voxels: Set[Voxel]):
    vmin, vmax = get_ranges(occupied_voxels)
    print(vmin, vmax)

    bvmin = Voxel(vmin.x-3, vmin.y-3, vmin.z-3)
    bvmax = Voxel(vmax.x+3, vmax.y+3, vmax.z+3)
    outside_group = find_connected_empty_space([occupied_voxels], Voxel(1,1,1), bvmin, bvmax)
    print("outside group len", len(outside_group))


    # find the holes
    inside_groups = []
    inside_total = set()
    fill_count = 0
    for x in range(vmin.x, vmax.x+1):
        for y in range(vmin.y, vmax.y+1):
            for z in range(vmin.z, vmax.z+1):
                test_v = Voxel(x,y,z)
                if test_v in occupied_voxels or test_v in inside_total:
                    continue #skip occupied_voxels
                if test_v not in outside_group:
                    print("Empty interior voxel", test_v)
                    inside_group = find_connected_empty_space([occupied_voxels, inside_total], test_v, vmin, vmax)
                    inside_groups.append(inside_group)
                    inside_total.update(inside_group)

    print("inside total is", len(inside_total))
    print("num groups", len(inside_groups))

    original_area = sweep(occupied_voxels, vmin, vmax)
    original_and_inside = sweep(occupied_voxels.union(inside_total), vmin, vmax)
    original_and_outside = sweep(occupied_voxels.union(outside_group), vmin, vmax)
    outside = sweep(outside_group, vmin, vmax)
    inside = sweep(inside_total, vmin, vmax)

    print("original_area", original_area)
    print("original_and_inside", original_and_inside)
    print("original_and_outside", original_and_outside)
    print("inside", inside)
    print("outside", outside)

    # # fill the holes
    # fill_count = 0
    # for x in range(vmin.x, vmax.x+1):
    #     for y in range(vmin.y, vmax.y+1):
    #         for z in range(vmin.z, vmax.z+1):
    #             test_v = Voxel(x,y,z)
    #             if test_v in occupied_voxels:
    #                 continue #skip occupied_voxels
    #             if test_v not in outside_group:
    #                 print("Empty interior voxel", test_v)
    #                 occupied_voxels.add(test_v)
    #                 fill_count += 1
    # print("Fill count", fill_count)

    # #now do the sweep again
    # return sweep(voxels, vmin, vmax)


if __name__ == '__main__':

    # filename='day18/test.txt'
    filename='day18/input.txt'

    voxels = load_input(filename)

    pprint(voxels)

    print('part 1', part1(voxels))

    print('part 2', part2(voxels))

