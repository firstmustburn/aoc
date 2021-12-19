
FLASH_THRESHOLD = 9

class Octo:
    def __init__(self, state):
        self.state = state
        self.neighbors = []
        self.canFlash = False
        self.hasFlashed = False
    
    def increment(self):
        self.state += 1
        self.canFlash = True
        self.hasFlashed = False

    def try_flash(self):
        """Return True if there is any state change"""
        stateChanged = False
        if self.canFlash:
            if self.state > FLASH_THRESHOLD:
                #flash
                self.hasFlashed = True
                self.canFlash = False
                #increment neighbor state
                for n in self.neighbors:
                    n.state += 1
                stateChanged = True
        
        return stateChanged
    
    def reset(self):
        if self.hasFlashed:
            #reset state
            self.state = 0



class OctoGrid:

    @classmethod
    def load(cls, filename):
        with open(filename) as infile:
            lines = infile.readlines()

        rows = []
        for line in lines:
            rows.append([ Octo(int(c)) for c in line.strip() ])

        assert len(rows) == 10
        for row in rows:
            assert len(row) == 10

        return OctoGrid(rows)

    def __init__(self, octos):
        self.octos = octos
        self.row_count = len(self.octos)
        self.col_count = len(self.octos[0])
        self.total_flash_count = 0
        self.step_count = 0

        #collect neighbors
        for r, c, octo in self.iterate(True):
            octo.neighbors = self.get_neighbors(r, c)

        assert len(self.octos[0][0].neighbors) == 3
        assert len(self.octos[0][9].neighbors) == 3
        assert len(self.octos[9][0].neighbors) == 3
        assert len(self.octos[9][9].neighbors) == 3
        assert len(self.octos[5][0].neighbors) == 5
        assert len(self.octos[5][9].neighbors) == 5
        assert len(self.octos[0][5].neighbors) == 5
        assert len(self.octos[9][5].neighbors) == 5
        assert len(self.octos[5][5].neighbors) == 8
        assert len(self.octos[4][5].neighbors) == 8
        assert len(self.octos[5][4].neighbors) == 8
        assert len(self.octos[7][7].neighbors) == 8



    def get_neighbors(self, row, col):
        neighbors = []
        for r in range(row-1, row+2):
            if r < 0 or r >= self.row_count:
                continue
            for c in range(col-1, col+2):
                if c < 0 or c >= self.col_count:
                    continue
                if r == row and c == col:
                    continue
                #if we get to here, r, c is an in-bound neighbor
                neighbors.append(self.octos[r][c])
        return neighbors

    def iterate(self, includeRC = False):
        for rownum, row in enumerate(self.octos):
            for colnum, octo in enumerate(row):
                if includeRC:
                    yield rownum, colnum, octo
                else:
                    yield octo
            
    def step(self):
        self.step_count += 1
        for octo in self.iterate():
            octo.increment()
        stateChanged = True
        while stateChanged:
            stateChanged = False
            for octo in self.iterate():
                if octo.try_flash():
                    stateChanged = True
        for octo in self.iterate():
            octo.reset()
        #count the flashes
        flash_count = 0
        for octo in self.iterate():
            if octo.hasFlashed:
                flash_count += 1
        self.total_flash_count += flash_count
        print(f"After step {self.step_count}: {flash_count} flashes, {self.total_flash_count} total flashes")


# # part 1
# og = OctoGrid.load("day11_test.txt")
# # og = OctoGrid.load("day11.txt")
# for i in range(100):
#     og.step()
#     # part 1: After step 100: 11 flashes, 1793 total flashes

# part 2

# og = OctoGrid.load("day11_test.txt")
og = OctoGrid.load("day11.txt")

while True:
    og.step()
    state_total = sum([ o.state for o in og.iterate()])
    if state_total == 0:
        #everyone flashed, so halt
        print("Everyone flashed")
        break
# After step 247: 100 flashes, 4038 total flashes
# Everyone flashed





