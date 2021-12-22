from bitarray import bitarray

def pair_range(pair):
    return range(pair[0], pair[1]+1)

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


class InstructionSet:

    @classmethod
    def parse(self, lines):
        instructions = [ Instruction.parse(line) for line in lines]
        return InstructionSet(instructions)

    def __init__(self, instructions):
        self.instructions = instructions
        self._initialize_state()

    def _find_bounds(self, range_ind):
        min_val = float('inf')
        max_val = float('-inf')

        for inst in self.instructions:
            i_val = inst.get_range(range_ind)
            min_val = min(min_val, i_val[0])
            max_val = max(max_val, i_val[1])

        return min_val, max_val        

    def _initialize_state(self):
        x_bound = self._find_bounds(Instruction.X_INDEX)
        y_bound = self._find_bounds(Instruction.Y_INDEX)
        z_bound = self._find_bounds(Instruction.Z_INDEX)

        self.x_start = x_bound[0]
        self.y_start = y_bound[0]
        self.z_start = z_bound[0]
        
        self.x_len = x_bound[1]-x_bound[0]+1
        self.y_len = y_bound[1]-y_bound[0]+1
        self.z_len = z_bound[1]-z_bound[0]+1
        
        print("bounds", x_bound, y_bound, z_bound)
        print("starts", self.x_start, self.y_start, self.z_start)
        print("lengths", self.x_len, self.y_len, self.z_len)
        
        #initialize state
        self.state = []
        for x in range(self.x_len):
            y_row = []
            for y in range(self.y_len):
                z_bits = bitarray('0'*self.z_len)
                y_row.append(z_bits)
            self.state.append(y_row)
        
        #now index into the self.state with [x-self.x_start][y-self.y_start][z-self.z_start]
        def set_state(x,y,z,value):
            # print("setting",x,y,z,value)
            assert x >= self.x_start
            assert y >= self.y_start
            assert z >= self.z_start
            self.state[x-self.x_start][y-self.y_start][z-self.z_start] = value

        for instruction in self.instructions:
            print(instruction)
            for xi in pair_range(instruction.xrange):
                for yi in pair_range(instruction.yrange):
                    for zi in pair_range(instruction.zrange):
                        if instruction.command == Instruction.ON_STR:
                            set_state(xi,yi,zi,1)
                        elif instruction.command == Instruction.OFF_STR:
                            set_state(xi,yi,zi,0)
                        else:
                            raise RuntimeError(f"Unknown command {instruction.command}")

    def iterate_state(self):
        for x in range(self.x_len):
            for y in range(self.y_len):
                for z in range(self.z_len):
                    yield x+self.x_start, y+self.y_start, z+self.z_start, self.state[x][y][z]

        
    def count_number_on(self, x_min, x_max, y_min, y_max, z_min, z_max):
        count = 0
        for x,y,z,value in self.iterate_state():
            if (x <= x_max and x >= x_min 
                and y <= y_max and y >= y_min 
                and z <= z_max and z >= z_min
                and value == 1):
                count += 1
        return count




if __name__ == "__main__":
    pass













