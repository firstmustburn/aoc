import sys

class InitialConditions:

    def __init__(self, xvel, yvel):
        self.xvel = xvel
        self.yvel = yvel
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"v={self.xvel},{self.yvel}"

    def __repr__(self):
        return self.__str__()



class Target:

    def __init__(self, target_tuple):
        self.xmin = min(target_tuple[0])
        self.xmax = max(target_tuple[0])
        self.ymin = min(target_tuple[1])
        self.ymax = max(target_tuple[1])

    def contains(self, x, y):
        return x >= self.xmin and x <= self.xmax and y >= self.ymin and y <= self.ymax


class Simulation:
    def __init__(self, target, initial_conditions):
        self.target = target
        self.initial_conditions = initial_conditions

        #additional state
        self.step_count = 0
        self.trajectory = []
        self.in_target = False

    def max_height(self):
        return self.y_range[1]

    def simulate(self):
        x = self.initial_conditions.x
        y = self.initial_conditions.y
        xvel = self.initial_conditions.xvel
        yvel = self.initial_conditions.yvel

        self.trajectory.append((x,y))
        while 1:
            self.step_count += 1
            x += xvel
            y += yvel
            if xvel > 0:
                xvel -= 1
            elif xvel < 0:
                xvel += 1
            #else no change, once xvel at 0
            yvel -= 1

            self.trajectory.append((x,y))

            if self.target.contains(x,y):
                max_h = max([ t[1] for t in self.trajectory ])
                # print(f"{self.initial_conditions.xvel},{self.initial_conditions.yvel} hit target at {x},{y} at height of {max_h} with trajectory of len {len(self.trajectory)}")
                self.in_target = True
                break

            #non-target halting condition:
            # we are below the ymin of the target and yvel is negative
            if y < self.target.ymin and yvel < 0:
                # max_h = max([ t[1] for t in self.trajectory ])
                # print(f"{self.initial_conditions.xvel},{self.initial_conditions.yvel} missed target at {x},{y} at height of {max_h} with trajectory of len {len(self.trajectory)}")
                break

        #save the stats
        self.x_range = (min([ t[0] for t in self.trajectory ]), max([ t[0] for t in self.trajectory ]))
        self.y_range = (min([ t[1] for t in self.trajectory ]), max([ t[1] for t in self.trajectory ]))
        # self.trajectory = None

    def dump(self):
        for t in self.trajectory:
            print(t[0], t[1])

    def __str__(self):
        return f"Simulation({self.initial_conditions})->{self.in_target}"

    def __repr__(self):
        return self.__str__()



class Range:
    def __init__(self, start, end):
        assert start != None
        assert end != None
        self.start = start
        self.end = end

    def iterate(self):
        return range(self.start, self.end+1)

    def __str__(self):
        return f"Range[{self.start},{self.end}]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash(self.start, self.end)

class SimulationSet:

    def __init__(self, target):
        self.target = target
        self.sim_data = {}

    def any_in_target(self, xv_range, yv_range):

        for xv in xv_range:
            for yv in yv_range:
                if self.sim_data[xv,yv].in_target == True:
                    return True
        return False

    def check_boundaries(self, xv_range, yv_range):
        """Assume everything in the boundary range has been simulated"""
        
        boundary_grew = False
        new_xmax = None
        new_ymin = None
        new_ymax = None

        #make sure we have at least one in target
        if not self.any_in_target(xv_range.iterate(), yv_range.iterate()):
            #grow all ranges until we hit the target once
            new_xmax = xv_range.end + 1
            new_ymin = yv_range.start - 1
            new_ymax = yv_range.end + 1

        else: 
            #we have hit the target, so check each boundary
            if self.any_in_target([xv_range.end-2, xv_range.end], yv_range.iterate()):
                #expand x range in the max direction
                new_xmax = xv_range.end + 1
            if self.any_in_target(xv_range.iterate(), [yv_range.start+2, yv_range.start]):
                #expand y range in the min direction
                new_ymin = yv_range.start - 1
            if self.any_in_target(xv_range.iterate(), [yv_range.end-2, yv_range.end]):
                #expand y range in the max direction
                new_ymax = yv_range.end + 1

        if new_xmax is not None:
            xv_range.end = new_xmax
            boundary_grew = True
        if new_ymin is not None:
            yv_range.start = new_ymin
            boundary_grew = True
        if new_ymax is not None:
            yv_range.end = new_ymax
            boundary_grew = True

        return boundary_grew

    def simulate_range(self, xv_range, yv_range):

        for xvel_start in xv_range.iterate():
            for yvel_start in yv_range.iterate():
                if (xvel_start, yvel_start) in self.sim_data:
                    #already simulated, so skip it
                    continue
                # print(f"New simulation for initial condition {xvel_start}, {yvel_start}")
                #new simulation
                ic = InitialConditions(xvel_start, yvel_start)
                sim = Simulation(self.target, ic)
                sim.simulate()
                self.sim_data[(xvel_start, yvel_start)] = sim
        
        #done simulating

    def grow_vel_ranges(self):

        #initial ranges
        xmax = max([abs(self.target.xmin), abs(self.target.xmax)])
        xv_range = Range(0,xmax+1)
        ymax = max([abs(self.target.ymin), abs(self.target.ymax)])
        yv_range = Range(-ymax,ymax)

        while 1:
            print("ranges", xv_range, yv_range)
            self.simulate_range(xv_range, yv_range)
            new_boundary = self.check_boundaries(xv_range, yv_range)
            if not new_boundary:
                print(f"Stopping at ranges xv:{xv_range} and yv:{yv_range}")
                break

        # self.xv_range = xv_range
        # self.yv_range = yv_range
        for xv in xv_range.iterate():
            print("XV=",xv)
            for yv in yv_range.iterate():
                target_string = "*" if self.sim_data[(xv,yv)].in_target else " "
                print(f"{yv:3d}{target_string} ", end="")
            print("")

    def get_in_target_results(self):
        return [ sim for sim in self.sim_data.values() if sim.in_target ]



def part1(target_tuple):
    target = Target(target_tuple)
    simset = SimulationSet(target)
    simset.grow_vel_ranges()

    in_target_runs = simset.get_in_target_results()

    in_target_runs = [ (s, s.max_height()) for s in in_target_runs  ] 
    in_target_runs.sort(key=lambda n:n[1])

    print ("shortest", in_target_runs[0])
    print ("tallest", in_target_runs[-1])
    print ("num hits", len(in_target_runs))





if __name__ == "__main__":
    #test
    # target area: x=20..30, y=-10..-5
    # target_area = ((20, 30), (-10,-5))

    #actual
    # "target area: x=169..206, y=-108..-68"
    target_area = ((169, 206), (-108, -68))

    part1(target_area)

    # target = Target(((169, 206), (-108, -68)))
    # ic = InitialConditions(19,107)
    # sim = Simulation(target, ic)
    # sim.simulate()
    # sim.dump()
    # print(sim.in_target)
    # print(sim.max_height())
