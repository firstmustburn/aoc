
# Strategy
# make a grid that is broken down by the x, y, and z boundaries for all the regions in the instruction set
# do on and off on that grid

def debug(*args):
    # pass
    print(*args)

def pair_range(pair):
    return range(pair[0], pair[1]+1)

def pairwise(values):
    return zip(values[:-1],values[1:])

X_INDEX=0
Y_INDEX=1
Z_INDEX=2
ON_STR='on'
OFF_STR='off'
ORIENTATION_STR = {
    X_INDEX:"x",
    Y_INDEX:"y",
    Z_INDEX:"z",
}

class FlexGrid:
    def __init__(self, x_boundaries, y_boundaries, z_boundaries):
        self._x_boundaries = self._parse_boundary_list(x_boundaries)
        self._y_boundaries = self._parse_boundary_list(y_boundaries)
        self._z_boundaries = self._parse_boundary_list(z_boundaries)
        self._construct_grid()

    @classmethod
    def _parse_boundary_list(cls, blist):
        #unique and sort the boundaries
        blist = sorted(set(blist))
        region_list = []
        # we don't account for adjacent regions
        for bound1, bound2 in pairwise(blist):
            assert bound1[1] <= bound2[0]
            region_list.append((bound1[1], bound2[0]))
        return region_list

    def _construct_grid(self):
        self.grid = []
        for x in range(len(self._x_boundaries)):
            x_row = []
            for y in range(len(self._y_boundaries)):
                x_row.append([0]*len(self._z_boundaries))
            self.grid.append(x_row)

    def set_cells(self, xrange, yrange, zrange, value):
        xind_min = self.get_index_from_value(self._x_boundaries, xrange[0], True)
        xind_max = self.get_index_from_value(self._x_boundaries, xrange[1], False)
        yind_min = self.get_index_from_value(self._y_boundaries, yrange[0], True)
        yind_max = self.get_index_from_value(self._y_boundaries, yrange[1], False)
        zind_min = self.get_index_from_value(self._z_boundaries, zrange[0], True)
        zind_max = self.get_index_from_value(self._z_boundaries, zrange[1], False)
        for xi in range(xind_min, xind_max+1):
            for yi in range(yind_min, yind_max+1):
                for zi in range(zind_min, zind_max+1):
                    self.grid[xi][yi][zi] = value

    def iterate_cells(self):
        for xi, xb in enumerate(self._x_boundaries):
            for yi, yb in enumerate(self._y_boundaries):
                for zi, zb in enumerate(self._z_boundaries):
                    yield xb, yb, zb, self.grid[xi][yi][zi]

    @classmethod
    def get_index_from_value(cls, blist, value, use_min):
        """Return the index in blist for the cell with the range value.  If use_min is true, check
        the minvalues, otherwise check the maxvalues"""
        for index, bval in enumerate(blist):
            if use_min:
                if bval[0] == value:
                    return index
            else:
                if bval[1] == value:
                    return index
        raise ValueError(f"No cell boundary for value={value}, use_min={use_min} in {blist}")

        

class Instruction:

    X_INDEX=0
    Y_INDEX=1
    Z_INDEX=2
    ON_STR='on'
    OFF_STR='off'

    @classmethod
    def parse(cls, line):
        def parse_range(range_part, expected_name):
            name, numpart = range_part.split('=')
            assert name == expected_name
            numpart = tuple([ int(r) for r in numpart.split('..') ])
            assert len(numpart) == 2
            assert numpart[0] <= numpart[1]
            return numpart

        tokens = line.strip().split(' ')
        assert len(tokens)==2
        command = tokens[0]
        assert command in [cls.ON_STR, cls.OFF_STR]
        ranges = tokens[1].split(',')
        assert len(ranges) == 3
        x_range = parse_range(ranges[0], 'x')
        y_range = parse_range(ranges[1], 'y')
        z_range = parse_range(ranges[2], 'z')

        return Instruction(command, x_range, y_range, z_range)

    def __init__(self, command, xrange, yrange, zrange):
        self.command = command
        self.xrange = xrange
        self.yrange = yrange
        self.zrange = zrange

    def get_range(self, range_ind):
        if range_ind == self.X_INDEX:
            return self.xrange
        elif range_ind == self.Y_INDEX:
            return self.yrange
        elif range_ind == self.Z_INDEX:
            return self.zrange
        else:
            raise IndexError(range_ind)

    def __str__(self):
        return f"Instruction(cmd={self.command}, x={self.xrange}, y={self.yrange}, x={self.zrange})"

    def __repr__(self):
        return self.__str__()


class Instruction:
    @classmethod
    def parse(cls, line):
        def parse_range(range_part, expected_name):
            name, numpart = range_part.split('=')
            assert name == expected_name
            numpart = tuple([ int(r) for r in numpart.split('..') ])
            assert len(numpart) == 2
            assert numpart[0] <= numpart[1]
            return numpart

        tokens = line.strip().split(' ')
        assert len(tokens)==2
        command = tokens[0]
        assert command in [ON_STR, OFF_STR]
        ranges = tokens[1].split(',')
        assert len(ranges) == 3
        x_range = parse_range(ranges[0], 'x')
        y_range = parse_range(ranges[1], 'y')
        z_range = parse_range(ranges[2], 'z')

        return Instruction(command, x_range, y_range, z_range)

    def __init__(self, command, x_range, y_range, z_range):
        self.command = command
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def __str__(self):
        return f"Instruction(cmd={self.command}, x={self.x_range}, y={self.y_range}, z={self.z_range})"

    def __repr__(self):
        return self.__str__()


class InstructionSet:

    @classmethod
    def parse(self, lines):
        instructions = [ Instruction.parse(line) for line in lines]
        return InstructionSet(instructions)

    def __init__(self, instructions):
        self.instructions = instructions

    def process_regions(self):
        """Output a list of region objects representing the regions of space that are ON with the
        regions of space that are OFF removed in the sequence of the instruction set"""

        x_bounds = []
        y_bounds = []
        z_bounds = []
        for instruction in self.instructions:
            #do min-1 -> min and max -> max+1 for each axis
            x_bounds.append((instruction.x_range[0]-1, instruction.x_range[0]))
            x_bounds.append((instruction.x_range[1], instruction.x_range[1]+1))
            y_bounds.append((instruction.y_range[0]-1, instruction.y_range[0]))
            y_bounds.append((instruction.y_range[1], instruction.y_range[1]+1))
            z_bounds.append((instruction.z_range[0]-1, instruction.z_range[0]))
            z_bounds.append((instruction.z_range[1], instruction.z_range[1]+1))
        self.grid = FlexGrid(x_bounds, y_bounds, z_bounds)

        for instruction in self.instructions:
            if instruction.command == ON_STR:
                set_value = 1
            else:
                set_value = 0
            print("Processing", instruction)
            self.grid.set_cells(instruction.x_range, instruction.y_range, instruction.z_range, set_value)
    
    def count_on_squares(self):
        total_on = 0
        for xrange, yrange, zrange, value in self.grid.iterate_cells():
            assert value in [0,1]
            if value == 1:
                xdim = abs(xrange[0]-xrange[1])+1
                ydim = abs(yrange[0]-yrange[1])+1
                zdim = abs(zrange[0]-zrange[1])+1
                total_on += xdim*ydim*zdim
        print("Total on: ", total_on)
        return total_on




if __name__ == "__main__":
    
    with open('day22.txt') as infile:
        data = infile.read()

    iset = InstructionSet.parse(data.strip().split('\n'))
    iset.process_regions()
    print("Count in init region:", iset.count_on_squares())

    # part3
    # Count in init region: 1228699515783640











