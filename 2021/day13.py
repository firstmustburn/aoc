



class Fold:

    X_DIR='x'
    Y_DIR='y'

    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude
        assert self.direction in [self.X_DIR, self.Y_DIR]


    def _get_point_dir_value(self, point):
        if self.direction == self.X_DIR:
            return point[0]
        elif self.direction == self.Y_DIR:
            return point[1]
        else:
            raise RuntimeError("Should be unnreachable")

    def _set_point_dir_value(self, new_value, point):
        if self.direction == self.X_DIR:
            return (new_value, point[1])
        elif self.direction == self.Y_DIR:
            return (point[0], new_value)
        else:
            raise RuntimeError("Should be unnreachable")

    def _fold(self, point):
        p_val = self._get_point_dir_value(point)
        if p_val < self.magnitude:
            #no fold 
            # print(f"No fold for {point} in {self.direction}={self.magnitude}")
            return point
        elif p_val > self.magnitude:
            #fold
            p_val = self.magnitude + (-1 * (p_val - self.magnitude))
            new_point = self._set_point_dir_value(p_val, point)
            # print(f"Folded {point} --> {new_point} in {self.direction}={self.magnitude}")
            return new_point
        else:
            raise RuntimeError(f"Invalid value {p_val} equal to magnitude {self.magnitude}")

    def fold_points(self, points):
        new_points = []
        for point in points:
            new_point = self._fold(point)
            if new_point not in new_points:
                new_points.append(new_point)
            # else:
            #     print("Skipped new point", new_point)
        return new_points

# class PointSet:

#     def __init__(self, points):
#         self.points = points


def load(filename):
    with open(filename) as infile:
        lines = infile.readlines()

    points = []
    folds = []
    isPoints = True
    for line in lines:
        if isPoints:
            #stop getting points at the blank line
            if line.strip() == "":
                isPoints = False
                continue
            #get a point
            x, y = [ int(s) for s in line.strip().split(',')]
            points.append((x,y))
        else:
            #get a fold
            tokens = line.strip().split(" ")
            assert tokens[0] == "fold"
            assert tokens[1] == "along"
            dir, magnitude = tokens[2].split("=")
            magnitude = int(magnitude)
            folds.append(Fold(dir, magnitude))

    return points, folds

def draw_points(points):
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    print("**************************")
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in points:
                print("#",end="")
            else:
                print(".",end="")
        print("")
    print("**************************")



# points, folds = load("day13_test.txt")
points, folds = load("day13.txt")

folded_points = list(points)
# draw_points(folded_points)
for fold in folds:
    folded_points = fold.fold_points(folded_points)
    # draw_points(folded_points)
    print("Folded point count:", len(folded_points))
    # break

draw_points(folded_points)


# part1: Folded point count: 710

# part2: 
#    ####.###..#.....##..###..#..#.#....###.
#    #....#..#.#....#..#.#..#.#..#.#....#..#
#    ###..#..#.#....#....#..#.#..#.#....#..#
#    #....###..#....#.##.###..#..#.#....###.
#    #....#....#....#..#.#.#..#..#.#....#.#.
#    ####.#....####..###.#..#..##..####.#..#
#
#  EPLGRULR