import sys
from collections import namedtuple
import re


Point = namedtuple("Point", ["x", "y"])

class PointSet:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def is_vh(self):
        return (self.p1.x == self.p2.x) or (self.p1.y == self.p2.y)

    def __str__(self):
        return f"{self.p1} -> {self.p2}"

    def __repr__(self):
        return self.__str__()


class VentMap:

    IMPORT_REGEX = re.compile("(\d+),(\d+) -> (\d+),(\d+)")

    @classmethod
    def loader(cls, filename):
        with open(filename) as infile:
            lines = infile.readlines()
        pointsets = []
        for line in lines:
            m = cls.IMPORT_REGEX.match(line)
            if m is None:
                print(f"Failed match on '{line}'")
            x1, y1, x2, y2 = [ int(c) for c in m.groups() ]
            pointsets.append(PointSet(Point(x1,y1), Point(x2,y2)))
        return VentMap(pointsets)

    def __init__(self, pointsets):
        self.pointsets = pointsets
        self.build_field()

    def build_field(self):
        xs = [ ps.p1.x for ps in self.pointsets ] + [ ps.p2.x for ps in self.pointsets ]
        ys = [ ps.p1.y for ps in self.pointsets ] + [ ps.p2.y for ps in self.pointsets ]
        self.min = Point(min(xs+[0]), min(ys+[0]))
        self.max = Point(max(xs), max(ys))
        print(self.min, self.max)
        assert self.min.x == 0
        assert self.min.y == 0
        self.field = []
        for x in range(self.max.x - self.min.x + 1):
            self.field.append([0]*(self.max.y - self.min.y + 1))

    def full_range(self, v1, v2):
        if v2 > v1:
            return list(range(v1, v2+1))
        elif v1 > v2:
            return list(range(v1, v2-1, -1))
        else:
            raise RuntimeError("Not supported")        

    def populate_field(self, skip_diag):
        for ps in self.pointsets:
            #note: field coords are [y][x]
            if ps.p1.x == ps.p2.x:
                print("Processed", ps)
                for y in self.full_range(ps.p1.y, ps.p2.y):
                    self.field[y][ps.p1.x] += 1
            elif ps.p1.y == ps.p2.y:
                print("Processed", ps)
                for x in self.full_range(ps.p1.x, ps.p2.x):
                    self.field[ps.p1.y][x] += 1
            else:
                if skip_diag:
                    print("Skipped", ps)
                    continue
                print("Processed", ps)
                xs = self.full_range(ps.p1.x, ps.p2.x)
                ys = self.full_range(ps.p1.y, ps.p2.y)
                for x,y in zip(xs, ys):
                    self.field[y][x] += 1

    def count_intersection_points(self):
        count = 0
        for row in self.field:
            for cell in row:
                if cell >= 2:
                    count += 1
        return count

    def dump(self):
        print("\n".join([str(s) for s in self.pointsets]))
        print("min: ", self.min)
        print("max: ", self.max)
        print("*"*80)
        for row in self.field:
            print(" ".join([ str(i) for i in row]))
        print("*"*80)
            



# # part1 = VentMap.loader("day5_test.txt")
# part1 = VentMap.loader("day5.txt")
# part1.populate_field(True)
# part1.dump()
# print("intersections:", part1.count_intersection_points())
# # intersections: 7318

# part2 = VentMap.loader("day5_test.txt")
part2 = VentMap.loader("day5.txt")
part2.populate_field(False)
part2.dump()
print("intersections:", part2.count_intersection_points())
# intersections: 19939