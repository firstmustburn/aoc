import copy

SOUTH=0
EAST=1
HERD_MAP = {
    '>':EAST,
    'v':SOUTH,
    '.':None,
}


class SeaBed:

    @classmethod
    def load(cls, data):
        lines = data.strip().split('\n')
        map = []
        for rownum, line in enumerate(lines):
            row = []
            for colnum, cuke_char in enumerate(line):
                row.append(HERD_MAP[cuke_char])
            map.append(row)
        return SeaBed(map)

    def __init__(self, seamap):
        self.seamap = seamap
        self.new_seamap = copy.deepcopy(seamap)
        self.row_count = len(seamap)
        self.col_count = len(seamap[0])
        self.step_count = 0

    def _next_position(self, r, c, direction):
        if direction == SOUTH:
            nr = (r + 1) % self.row_count
            nc = c
        elif direction == EAST:
            nr = r
            nc = (c + 1) % self.col_count
        else:
            raise RuntimeError(f"not supported: {direction}")
        return nr, nc

    def _move_herd(self, direction):
        move_count = 0
        #copy the current state to the other map
        for r in range(self.row_count):
            for c in range(self.col_count):
                self.new_seamap[r][c] = self.seamap[r][c]
        #make any moves that are possible, writing the moves into the new map
        for r in range(self.row_count):
            for c in range(self.col_count):
                #skip positions not in this herd
                if self.seamap[r][c] != direction:
                    continue
                nr, nc = self._next_position(r, c, direction)
                #skip if next position occupied
                if self.seamap[nr][nc] is not None:
                    continue
                #make the move in the *new* map
                self.new_seamap[r][c] = None
                self.new_seamap[nr][nc] = direction
                move_count += 1
        return move_count


    def run_to_no_motion(self):
        while 1:
            move_count = self.step()
            if move_count == 0:
                break

    def step(self):
        move_count = 0
        #move herd writes the moves into self.new_seamap
        move_count += self._move_herd(EAST)
        #swap the maps
        temp = self.seamap
        self.seamap = self.new_seamap
        self.new_seamap = temp
        
        #move herd writes the moves into self.new_seamap
        move_count += self._move_herd(SOUTH)
        #swap the maps
        temp = self.seamap
        self.seamap = self.new_seamap
        self.new_seamap = temp
        
        self.step_count += 1
        return move_count


    def __eq__(self, other):
        return self.seamap == other.seamap


if __name__ == "__main__":
    with open('day25.txt') as infile:
        data = infile.read()

    state = SeaBed.load(data)
    state.run_to_no_motion()

    print("Step count", state.step_count)

    # Part 1
    # Step count 380

