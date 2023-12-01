
from pprint import pprint
from collections import namedtuple

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

Point = namedtuple('Point',['x','y'])

Move = namedtuple('Move',['direction','distance'])

class End:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y
        self.history = []
        self.update_history()
    
    def update_history(self):
        self.history.append(Point(self.x, self.y))

class Follower:
    def __init__(self):
        self.followers = []
        
    def update_followers(self):
        for f in self.followers:
            f.follow_update(self)

    def add_follower(self, follower):
        self.followers.append(follower)

class Head(End, Follower):
    def __init__(self, initial_x, initial_y):
        End.__init__(self, initial_x, initial_y)
        Follower.__init__(self)

    def move(self, direction):
        if direction == UP:
            self.y += 1
        elif direction == DOWN:
            self.y -= 1
        elif direction == RIGHT:
            self.x += 1
        elif direction == LEFT:
            self.x -= 1
        else:
            raise RuntimeError(f"Unknown direction {direction}")
        self.update_history()
        self.update_followers()

class Tail(End, Follower):
    def __init__(self, initial_x, initial_y):
        End.__init__(self, initial_x, initial_y)
        Follower.__init__(self)

    def follow_update(self, source):
        
        x_move = False
        y_move = False
        if source.x - self.x > 1:
            #move in the +x direction
            self.x += 1
            x_move = True
        elif source.x - self.x < -1:
            #move in the -x direction
            self.x -= 1
            x_move = True

        if source.y - self.y > 1:
            #move in the +y direction
            self.y += 1
            y_move = True
        elif source.y - self.y < -1:
            #move in the -y direction
            self.y -= 1
            y_move = True
        
        #make the sideways adjustments
        if x_move and not y_move:
            self.y = source.y
        elif not x_move and y_move:
            self.x = source.x

        assert abs(self.x - source.x) <= 1
        assert abs(self.y - source.y) <= 1
        #update our history
        self.update_history()
        self.update_followers()

Track = namedtuple("Track", ['history','letter'])

class Grid:


    @staticmethod
    def from_track(track, min_range=None, default="."):
        if min_range is None:
            min_range = []
        x_list = []
        y_list = []
        for p in min_range:
            x_list.append(p.x)
            y_list.append(p.y)
        x_list += [ p.x for p in track.history ]
        y_list += [ p.y for p in track.history ]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)
        return Grid(Point(min_x, min_y), Point(max_x, max_y), default)

    def __init__(self, min_p, max_p, default="."):
        self.default = default

        self.min_p = min_p
        self.max_p = max_p

        self.grid = {}

        self.make_blank()

    def make_blank(self):
        for x in range(self.min_p.x, self.max_p.x + 1):
            for y in range(self.min_p.y, self.max_p.y + 1):
                self.grid[Point(x,y)] = self.default

    def draw(self):
        #print row
        for y in range(self.max_p.y, self.min_p.y - 1, -1): #reverse y so largest row printed first
            print(''.join([ self.grid[Point(x,y)] for x in range(self.min_p.x, self.max_p.x + 1) ]))
        print('')

    def fill_track(self, track):
        #write the track in     
        for p in track.history:
            self.grid[p] = track.letter
    
    def fill_point(self, point, letter):
        self.grid[point] = letter


def draw_sequence(grid, tracks):

    #go through each history point, place it on the grid, and draw it
    for index in range(len(tracks[0].history)):
        grid.make_blank()
        for track in tracks:
            grid.fill_point(track.history[index], track.letter)
        grid.draw()
    
def load_input(filename):
    move_list = []
    with open(filename) as infile:
        for line in infile:
            direction, distance = line.strip().split()
            distance = int(distance)
            move_list.append(Move(direction, distance))
    return move_list

def part1(move_list):
    head = Head(0,0)
    tail = Tail(0,0)
    head.add_follower(tail)
    for move in move_list:
        for d in range(move.distance):
            head.move(move.direction)
    
    head_track = Track(head.history, 'h')
    tail_track = Track(tail.history, 't')

    grid = Grid.from_track(head_track)

    # draw_sequence(grid, [tail_track, head_track])

    grid.make_blank()
    grid.fill_track(tail_track)
    grid.draw()

    #count the tail parts
    tail_count = 0
    for p, v in grid.grid.items():
        if v == 't':
            tail_count += 1
    return tail_count

def part2(move_list):
    #set up the knot sequence
    head = Head(0,0)

    tails = []
    prev = head
    for i in range(9):
        tail = Tail(0,0)
        tails.append(tail)
        prev.add_follower(tail)
        prev = tail

    for move in move_list:
        for d in range(move.distance):
            head.move(move.direction)
    
    tracks = []
    head_track = Track(head.history, 'h')
    tracks.append(head_track)
    for i, tail in enumerate(tails):
        tracks.append(Track(tail.history, f"{i+1:x}"))
    tracks.reverse() 

    grid = Grid.from_track(head_track)

    # draw_sequence(grid, tracks)

    grid.make_blank()
    grid.fill_track(tracks[0]) #because of the reverse, this is the last tail
    grid.draw()

    #count the tail parts
    tail_count = 0
    for p, v in grid.grid.items():
        if v == '9':
            tail_count += 1
    return tail_count

if __name__ == '__main__':

    # filename='day9/test.txt'
    # filename='day9/test2.txt'
    filename='day9/input.txt'

    move_list = load_input(filename)

    # print('part 1', part1(move_list))

    print('part 2', part2(move_list))

