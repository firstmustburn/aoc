import numpy as np
from scipy.spatial.transform import Rotation
import math
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import sys
from typing import Sequence

color_map = matplotlib.colors.get_named_colors_mapping() 



def round3(dist):
    return round(dist*1000)/1000

def pairwise(items):
    for index, item1 in enumerate(items):
        for item2 in items[index+1:]:
            yield item1, item2  

class Scanner:

    def __init__(self, name, points):
        self.name = name
        self.points = points
        self._compute_point_distances()

    def _compute_point_distances(self):
        self.distance_map = defaultdict(list)
        for p, q in pairwise(self.points):
            distance = round3(np.linalg.norm(np.array(p)-np.array(q)))
            self.distance_map[distance].append((p,q))

    def get_distance_segment(self, length):
        dme = self.distance_map[length]
        assert len(dme) == 1
        return dme[0]

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()


class ScannerTransformation:

    def __init__(self, rotation, translation, from_scanner, to_scanner):
        self.rotation = rotation
        self.translation = translation
        self.from_scanner = from_scanner
        self.to_scanner = to_scanner

    def invert(self):
        print("Inverting", self)
        return ScannerTransformation(
            rotation = self.rotation.inv(),
            translation = tuple([ -1*v for v in self.translation ]),
            from_scanner = self.to_scanner,
            to_scanner = self.from_scanner
        )

    def __str__(self):
        return f"stx({self.from_scanner.name}->{self.to_scanner.name})"

    def __repr__(self):
        return self.__str__()

    def transform_points(self, point_list):
        rmat = self.rotation.as_matrix()
        offset_arr = np.array(self.translation)
        new_points=[]
        for point in point_list:
            new_point = np.dot(rmat, np.array(point)) + offset_arr
            new_point = tuple([ int(round(v)) for v in new_point ])
            new_points.append(new_point)
        return new_points

def find_transform_path(s1:Scanner, s2:Scanner, transform_list:Sequence[ScannerTransformation]):

    def recurse_find_path(current_path, intermediate_source, target):
        for tx in transform_list:
            if tx in current_path:
                continue

            if tx.from_scanner is intermediate_source and tx.to_scanner is target:
                return current_path+[tx]
            # if tx.from_scanner is target and tx.to_scanner is intermediate_source:
            #     return current_path+[tx.invert()]

        for tx in transform_list:
            if tx in current_path:
                continue
            if tx.from_scanner is intermediate_source:
                recurse_path = recurse_find_path(current_path+[tx], tx.to_scanner, target)
                if recurse_path is not None:
                    return recurse_path
            # if tx.to_scanner is intermediate_source:
            #     recurse_path = recurse_find_path(current_path+[tx.invert()], tx.from_scanner, target)
            #     if recurse_path is not None:
            #         return recurse_path
        #if we get here, then no path was found on this branch
        return None

    return recurse_find_path([], s1, s2)
    







def load(filename):
    with open(filename) as infile:
        lines = infile.readlines()

    scanners = []

    current_scanner_name = None
    current_points = None
    for line in lines:
        if line.startswith('---'):
            if current_scanner_name is not None:
                scanners.append(Scanner(current_scanner_name, current_points))
            current_scanner_name = line.strip().strip('-').strip()
            current_points = []
            continue
        if len(line.strip()) == 0:
            continue
        #convert the line into a pheaver
        point = [ int(t) for t in line.strip().split(',') ]
        current_points.append(tuple(point))

    #collect the last scanner if there is one
    if current_points is not None and len(current_points) > 0:
        scanners.append(Scanner(current_scanner_name, current_points))

    return scanners












def plot_common_distances(s1, s2, distances):
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, projection='3d')
    colors = ['black','red','sienna','darkorange','gold','lawngreen','darkgreen','turquoise','blue','indigo','magenta','violet']
    # colors = [color_map[c] for c in colors]
    # print(colors)

    def plot_pts(pts, color):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        zs = [p[2] for p in pts]
        ax.plot(xs,ys,zs, color)

    for index, distance in enumerate(distances):
        color = colors[index % len(colors)]
        plot_pts(s1.distance_map[distance][0], color)
        plot_pts(s2.distance_map[distance][0], color)

    plt.show()

def plot_common_points(cp, cp2):
    fig = plt.figure(figsize=(8,8))
    colors = ['black','red','sienna','darkorange','gold','lawngreen','darkgreen','turquoise','blue','indigo','magenta','violet']

    def plot_pts(ax, pts, color):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        zs = [p[2] for p in pts]
        ax.plot(xs,ys,zs, color)

    ax = fig.add_subplot(111, projection='3d')
    index = 0
    color = colors[index % len(colors)]
    index += 1
    for p1, p2 in cp.items():
        plot_pts(ax, [p1,p2],color)

    color = colors[index % len(colors)]
    index += 1
    for p1, p2 in cp.items():
        plot_pts(ax, [p2,cp2[p1]],color)

    plt.show()

def plot_all_common_points(pointsets):
    fig = plt.figure(figsize=(4,4))
    colors = ['black','red','sienna','darkorange','gold','lawngreen','darkgreen','turquoise','blue','indigo','magenta','violet']

    def plot_pts(ax, pts, color):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        zs = [p[2] for p in pts]
        ax.plot(xs,ys,zs, color)

    ax = fig.add_subplot(111, projection='3d')
    index = 0
    for pointset in pointsets:
        color = colors[index % len(colors)]
        index += 1
        for p1, p2 in pointset.items():
            plot_pts(ax, [p1,p2],color)

    plt.show()


def get_all_common_points(scanner1, scanner2, common_distances):
    def find_common_point(s, d1, d2):
        seg1 = s.get_distance_segment(d1)
        seg2 = s.get_distance_segment(d2)
        # print("segment 1:", seg1)
        # print("segment 2:", seg2)
        if seg1[0] in seg2:
            return seg1[0]
        elif seg1[1] in seg2:
            return seg1[1]
        else:
            return None

    common_points = {}
    for d1, d2 in pairwise(common_distances):
        p1 = find_common_point(scanner1, d1, d2)
        if p1 is not None:
            if p1 in common_points:
                continue
            p2 = find_common_point(scanner2, d1, d2)
            if p2 is None:
                print(f"Skipping point because no match found for point p1 {p1} from distances {d1},{d2}")
                continue
            common_points[p1]=p2
    
    return common_points

def centroid(points):
    np = len(points)
    cx = sum([ p[0] for p in points ])/np
    cy = sum([ p[1] for p in points ])/np
    cz = sum([ p[2] for p in points ])/np
    return (cx,cy,cz)

def manhattan_difference(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])+abs(p1[2]-p2[2])

def difference(p1,p2):
    return (p1[0]-p2[0],p1[1]-p2[1],p1[2]-p2[2])

def add_points(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1],p1[2]+p2[2])

def magnitude(p):
    return np.linalg.norm(np.array(p))

def transform(m, p):
    preg = np.array(list(p)+[1])
    tx = np.dot(m, preg.T)
    return tuple(tx.tolist())


def possible_rotations():
    rotations = []
    #+x with four orientations
    rotations.append(Rotation.from_euler('x',0,degrees=True))
    rotations.append(Rotation.from_euler('x',90,degrees=True))
    rotations.append(Rotation.from_euler('x',180,degrees=True))
    rotations.append(Rotation.from_euler('x',270,degrees=True))
    #-x with four orientations
    rotations.append(Rotation.from_euler('zx',[180, 0],degrees=True))
    rotations.append(Rotation.from_euler('zx',[180, 90],degrees=True))
    rotations.append(Rotation.from_euler('zx',[180, 180],degrees=True))
    rotations.append(Rotation.from_euler('zx',[180, 270],degrees=True))
    #+y with four orientations
    rotations.append(Rotation.from_euler('zy',[90, 0],degrees=True))
    rotations.append(Rotation.from_euler('zy',[90, 90],degrees=True))
    rotations.append(Rotation.from_euler('zy',[90, 180],degrees=True))
    rotations.append(Rotation.from_euler('zy',[90, 270],degrees=True))
    #-y with four orientations
    rotations.append(Rotation.from_euler('zy',[270, 0],degrees=True))
    rotations.append(Rotation.from_euler('zy',[270, 90],degrees=True))
    rotations.append(Rotation.from_euler('zy',[270, 180],degrees=True))
    rotations.append(Rotation.from_euler('zy',[270, 270],degrees=True))
    #+z with four orientations
    rotations.append(Rotation.from_euler('yz',[90, 0],degrees=True))
    rotations.append(Rotation.from_euler('yz',[90, 90],degrees=True))
    rotations.append(Rotation.from_euler('yz',[90, 180],degrees=True))
    rotations.append(Rotation.from_euler('yz',[90, 270],degrees=True))
    #-z with four orientations
    rotations.append(Rotation.from_euler('yz',[270, 0],degrees=True))
    rotations.append(Rotation.from_euler('yz',[270, 90],degrees=True))
    rotations.append(Rotation.from_euler('yz',[270, 180],degrees=True))
    rotations.append(Rotation.from_euler('yz',[270, 270],degrees=True))

    return rotations

def rotate_points(rotation, point_map):
    rmat = rotation.as_matrix()
    points_out = {}
    for key, point in point_map.items():
        pout = np.dot(rmat, np.array(point))
        points_out[key] = tuple(pout.tolist())
    return points_out

def compute_total_error(pointmap):
    #distance is sqtr(a**2+b**2+c**2), but we want the square of the error
    def err_fun(p1,p2):
        return math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2)+math.pow(p1[2]-p2[2],2)

    return sum([ err_fun(p1,p2) for p1,p2 in pointmap.items()])

def match_scanners(s1: Scanner, s2: Scanner):
    d1 = set(s1.distance_map.keys())
    d2 = set(s2.distance_map.keys())
    common_distances = d1.intersection(d2)
    for d in list(common_distances):
        if len(s1.distance_map[d]) > 1 or len(s2.distance_map[d]) > 1:
            # print("removing non-unique distance", d)
            common_distances.remove(d)
    common_distances=list(common_distances)

    print("found", len(common_distances), "common distances")
    if len(common_distances) < 12:
        print("No match because not enough common distances")
        #no match possible
        return None

    common_points = get_all_common_points(s1, s2, common_distances)
    print("found",len(common_points), "common points")

    if len(common_points) < 12:
        print("No match because not enough common points")
        #no match possible
        return None

    min_error = float('inf')
    min_rotation = None
    min_offset = None
    min_points = None
    for rotation in possible_rotations():
        transformed_points = rotate_points(rotation, common_points)

        # if "7" in s1.name and "23" in s2.name:
        #     plot_common_points(common_points, transformed_points)

        #transform to align the centroids of the two point sets
        cent1 = centroid(list(transformed_points.keys()))
        cent2 = centroid(list(transformed_points.values()))    
        offset = difference(cent1, cent2)

        for key in transformed_points:
            translated_rpoint = add_points(offset, transformed_points[key])
            transformed_points[key] = translated_rpoint

        total_error = compute_total_error(transformed_points)
        # print("Total error is ", total_error)
        if total_error < min_error:
            min_error = total_error
            min_rotation = rotation
            min_offset = offset
            min_points = transformed_points

    #now we have the rotation and offset between the two scanners
    #gut check
    assert min_points is not None
    if abs(min_error-0) > 1:
        print("  Match failed for all rotations")
        return None

    return ScannerTransformation(min_rotation, min_offset, s1, s2)




def transform_points_with_txlist(pointlist, txlist):
    out_points = pointlist
    for tx in reversed(txlist):
        # print(len(out_points),"points to transform")
        out_points = tx.transform_points(out_points)
    return out_points


if __name__ == "__main__":
    # scanners = load('day19_test.txt')
    scanners = load('day19.txt')

    scanner_transforms = []
    for s1 in scanners:
        for s2 in scanners:
            if s1 is s2:
                continue
            print("*"*80)
            print("Checking", s1.name, "against", s2.name)
            tx_match = match_scanners(s1, s2)
            if tx_match is not None:
                scanner_transforms.append(tx_match)
                print("match FOUND")
            else:
                print("no match")

    print("")
    print("*"*80)
    print("*"*80)
    root_scanner = scanners[0]
    root_scanner.origin = (0,0,0)
    all_points = set(root_scanner.points)
    for scanner in scanners[1:]:
        tx_path = find_transform_path(root_scanner, scanner, scanner_transforms)
        print("Path from", root_scanner, "to", scanner)
        print(tx_path)
        if tx_path is None:
            print("Failed to find a path among these transforms:")
            for stx in scanner_transforms:
                print('   ', stx)
        assert tx_path is not None

        global_points = transform_points_with_txlist(scanner.points, tx_path)
        scanner_origin = transform_points_with_txlist([(0,0,0)], tx_path)
        scanner.origin = scanner_origin[0]
        all_points = all_points.union(global_points)

    print("")
    print("*"*80)
    print("*"*80)
    for p in sorted(all_points):
        print(p)

    print("*"*80)
    for scanner in scanners:
        print(scanner.name, "origin at", scanner.origin)
    
    print("*"*80)
    print("Total number of points:", len(all_points))


    md_list = []
    for s1, s2 in pairwise(scanners):
        md = manhattan_difference(s1.origin, s2.origin)
        print(s1,"to",s2,"manhattan distance is",md)
        md_list.append(md)
    print("Maximum manhattan distance is", max(md_list))



    # part 1
    # ********************************************************************************
    # Total number of points: 398