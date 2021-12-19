import sys
from collections import namedtuple


class Fish:
    def __init__(self, state=8):
        self.state = state

    def iterate(self):
        self.state -= 1
        if self.state < 0:
            #give birth to a new fish
            self.state = 6
            return Fish()
        else:
            #normal aging
            return None    

class FishSim:

    @classmethod
    def loader(cls, filename):
        with open(filename) as infile:
            lines = infile.readlines()

        assert len(lines) == 1

        fishlist = [ Fish(int(s)) for s in lines[0].split(",") ]

        return FishSim(fishlist)

    def __init__(self, fishlist):
        self.fishlist = fishlist
        self.day = 0

    def simulate(self, days):
        for d in range(days):
            new_fishlist = []
            self.day += 1
            for fish in self.fishlist:
                newfish = fish.iterate()
                if newfish:
                    new_fishlist.append(newfish)
            self.fishlist.extend(new_fishlist)
            print(self.day, len(self.fishlist))
            # self.dump()

    def get_count(self):
        return len(self.fishlist)

    def dump(self):
        statelist = ",".join([ str(f.state) for f in self.fishlist ])
        print(f"On day {self.day:2d}: {statelist}")


class FishSimScalable:

    @classmethod
    def loader(cls, filename):
        with open(filename) as infile:
            lines = infile.readlines()

        assert len(lines) == 1

        fishlist = [ Fish(int(s)) for s in lines[0].split(",") ]

        return FishSimScalable(fishlist)

    MAX_DAYS = 9

    def __init__(self, fishlist):
        self.state_count = []
        # count the fish in each state
        for i in range(self.MAX_DAYS):
            self.state_count.append(len([ f for f in fishlist if f.state == i ]))                        
        self.day = 0

    def simulate(self, days):
        for d in range(days):
            self.day += 1
            # shift the state counts by one, saving the fish that will reproduce
            # (at the 0 count) to wrap around and incremnt the number of new fish
            giving_birth_count = self.state_count[0]
            self.state_count = self.state_count[1:]
            self.state_count[6] += giving_birth_count
            self.state_count.append(giving_birth_count) #these are the new fish at day 8
            assert len(self.state_count) == self.MAX_DAYS
            self.dump()

    def get_count(self):
        return sum(self.state_count)

    def dump(self):
        print(self.state_count)
        statelist = ",".join([ f"{i}:{f}" for i,f in enumerate(self.state_count) ])
        print(f"On day {self.day:2d}: {statelist}")


# # part1 = FishSim.loader("day6_test.txt")
# part1 = FishSim.loader("day6.txt")
# part1.dump()
# part1.simulate(80)
# print(part1.get_count()) # 351188 

# part2 = FishSimScalable.loader("day6_test.txt")
part2 = FishSimScalable.loader("day6.txt")
part2.dump()
part2.simulate(256)
print(part2.get_count()) # 1595779846729 
