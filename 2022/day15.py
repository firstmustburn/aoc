
from pprint import pprint
from collections import namedtuple

Point = namedtuple('Point',['x','y'])

Range = namedtuple('Range',['start','end'])

def mdist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) 

class Sensor:

    def __init__(self, sensor_point, beacon_point):
        self.sensor_point = sensor_point
        self.beacon_point = beacon_point

    def get_mdist(self):
        return mdist(self.sensor_point, self.beacon_point)

    def intersect_row(self, y):
        # returns the x start-end range where the row y intersects the exclusion range
        md = self.get_mdist()
        y_dist = abs(y-self.sensor_point.y)
        if y_dist > md:
            return None
        x_dist = md - y_dist
        return Range(self.sensor_point.x - x_dist, self.sensor_point.x + x_dist)


def parse_line(line):
    #Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    print(line)
    tokens = line.strip().split()
    assert tokens[0] == 'Sensor'
    assert tokens[1] == 'at'
    assert tokens[4] == 'closest'
    assert tokens[5] == 'beacon'
    assert tokens[6] == 'is'
    assert tokens[7] == 'at'
    sensor_x = int(tokens[2].strip(',').split('=')[1])
    sensor_y = int(tokens[3].strip(':').split('=')[1])

    beacon_x = int(tokens[8].strip(',').split('=')[1])
    beacon_y = int(tokens[9].split('=')[1])
    return Sensor(Point(sensor_x, sensor_y), Point(beacon_x, beacon_y))

def load_input(filename):
    sensors = []
    with open(filename) as infile:
        for line in infile:
            sensors.append(parse_line(line))
    return sensors

class MergedRanges:
    def __init__(self, target_row, sensors):
        self.target_row = target_row
        self.ranges = []
        self.sensors = sensors

        for sensor in self.sensors:
            self._add_sensor(sensor)

    @staticmethod
    def _intersect(r1, r2):
        if (r1.start >= r2.start and r1.start <= r2.end) or \
            (r1.end >= r2.start and r1.end <= r2.end) or \
            (r2.start >= r1.start and r2.start <= r1.end) or \
            (r2.end >= r1.start and r2.end <= r1.end):
            return Range(min(r1.start, r1.end, r2.start, r2.end), max(r1.start, r1.end, r2.start, r2.end))
        return None

    def _contains(self, point):
        if point.y != self.target_row:
            return False
        for range in self.ranges:
            if point.x >= range.start and point.x <= range.end:
                return True
            return False

    def _add_sensor(self, sensor):
        sensor_range = sensor.intersect_row(self.target_row)
        if sensor_range is None:
            return False
        self._add_range(sensor_range)

    @staticmethod
    def _join_range(r1, r2):
        if r1.end + 1 == r2.start:
            return Range(r1.start, r2.end)
        if r2.end + 1 == r1.start:
            return Range(r2.start, r1.end)

    def _join_ranges(self):
        while True:
            for i1, r1 in enumerate(self.ranges):
                for r2 in self.ranges[i1+1:]:
                    joined_range = self._join_range(r1,r2)
                    if joined_range:
                        self.ranges.remove(r1)
                        self.ranges.remove(r2)
                        self.ranges.append(joined_range)
                        continue
            #no joins, so done
            break

    def _add_range(self, new_range):        
        new_ranges = []
        for range in self.ranges:
            intersected = self._intersect(range, new_range)
            if intersected is None:
                #keep the old range
                new_ranges.append(range)
            else:
                # keep the merged range as the new range and keep trying to merge it with other ranges
                new_range = intersected
        #at the end, add our new_range
        new_ranges.append(new_range)
        self.ranges = new_ranges
        self._join_ranges()

    def get_coverage(self):
        count = 0
        for range in self.ranges:
            count += (range.end - range.start) + 1
        #decrement counts for any sensor or beacon in any of the ranges
        removed_points = set()

        for sensor in self.sensors:
            if sensor.sensor_point not in removed_points and self._contains(sensor.sensor_point):
                count = count - 1
                removed_points.add(sensor.sensor_point)
            if sensor.beacon_point not in removed_points and self._contains(sensor.beacon_point):
                count = count - 1
                removed_points.add(sensor.beacon_point)
        return count

def part1(sensors, target_y):
    mr = MergedRanges(target_y, sensors)

    print(mr.ranges)

    return mr.get_coverage()

def part2(sensors, bound):

    for y in range(bound+1):
        if y % 10000 == 0:
            print("y=",y)
        mr = MergedRanges(y, sensors)
        if len(mr.ranges) > 1:
            print(y, mr.ranges)
            break

    return None

if __name__ == '__main__':

    # filename='day15/test.txt'
    # target_y = 10
    # bound = 20
    filename='day15/input.txt'
    target_y = 2000000
    bound = 4000000

    sensors = load_input(filename)

    pprint(sensors)

    # print('part 1', part1(sensors, target_y))

    print('part 2', part2(sensors, bound))
    # 3186981 [Range(start=3334480, end=4182002), Range(start=-467701, end=3334478)]

    # 4000000 * 3334479 + 3186981
