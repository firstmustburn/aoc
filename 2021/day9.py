import sys


BASIN_LIMIT = 9

class Basin:

    def __init__(self, hmap, initial_r, initial_c):
        self.hmap = hmap
        self.initial_r = initial_r
        self.initial_c = initial_c
        #
        self.bmap = [ [0]*self.hmap.col_count for r in range(self.hmap.row_count)]
        self.grow(initial_r, initial_c)

        self.size = sum([ sum(row) for row in self.bmap ])

    def grow(self, r, c):
        #add the cell to the basin
        assert self.hmap.get_point(r,c) != BASIN_LIMIT
        #see if we've already added the cell to the basin
        if self.bmap[r][c] == 0:
            self.bmap[r][c] = 1
            #try to add the cell's neighbors
            for nr, nc in self.hmap.neighbor_coords(r,c):
                if self.hmap.get_point(nr, nc) < BASIN_LIMIT:
                    self.grow(nr,nc)
        # else already added, so skip adding and children

    def dump(self):
        output = "********************\n"
        output += f"Size: {self.size}\n"
        for r in range(self.hmap.row_count):
            for c in range(self.hmap.col_count):
                output += str(self.bmap[r][c])
                if self.initial_r == r and self.initial_c == c:
                    output += "*"
                else:
                    output += " "
            output += "\n"
        output += "********************"
        print(output)

class Hmap:

    @classmethod
    def load(cls, filename):

        with open(filename) as infile:
            lines = infile.readlines()

        hmap = []
        for line in lines:
            hmap.append([ int(c) for c in line.strip() ])

        row_len = len(hmap[0])

        return Hmap(hmap)




    def __init__(self, points):
        self.points = points
        self.row_count = len(self.points)
        self.col_count = len(self.points[0])

        for row in self.points:
            assert len(row) == self.col_count

    def neighbor_coords(self, r,c):
        nlist = []
        if r > 0:
            nlist.append((r-1,c))
        if r < self.row_count-1:
            nlist.append((r+1,c))
        if c > 0:
            nlist.append((r, c-1))
        if c < self.col_count-1:
            nlist.append((r, c+1))
        return nlist
    
    def neighbors(self, r,c):
        return [self.points[rn][cn] for rn,cn in self.neighbor_coords(r,c)]

    def is_low_point(self, r, c):
        point = self.points[r][c]
        nlist = self.neighbors(r, c)
        return all([ point < nval for nval in nlist ])

    def get_low_point_coords(self):
        low_points = []
        for row in range(self.row_count):
            for col in range(self.col_count):
                if self.is_low_point(row, col):
                    low_points.append((row, col))
        return low_points

    def get_basins(self):
        basins = []
        for r,c in self.get_low_point_coords():
            basins.append(Basin(self, r, c))
        return basins
            
    def get_point_tuple(self, rc):
        return self.points[rc[0]][rc[1]]

    def get_point(self, r, c):
        return self.points[r][c]

    def get_low_points_risk(self):
        total_risk = 0
        for row, col in self.get_low_point_coords():
            total_risk += self.points[row][col] + 1
            print(f"low point at {row}, {col}: {self.points[row][col]}")
        print(f"total_risk = {total_risk}")

    def dump(self):
        output = "********************\n"
        for r in range(self.row_count):
            for c in range(self.col_count):
                output += str(self.points[r][c])
                if self.is_low_point(r,c):
                    output += "*"
                else:
                    output += " "
            output += "\n"
        output += "********************"
        print(output)


        
# hmap = Hmap.load("day9_test.txt")
hmap = Hmap.load("day9.txt")
hmap.dump()
hmap.get_low_points_risk()
# total_risk = 514

basins = hmap.get_basins()
basins.sort(key=lambda b: b.size)

for b in basins:
    b.dump()

basin_product = 1
print(basins[-3:])
for tb in basins[-3:]:
    print("top basin:", tb.size)
    basin_product *= tb.size
print("Top three basin product:", basin_product)

# top basin: 102
# top basin: 103
# top basin: 105
# Top three basin product: 1103130