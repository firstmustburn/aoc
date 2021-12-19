import sys
from collections import namedtuple

class Space:
    def __init__(self, value):
        self.value = value
        self.marked = False

    def mark(self):
        self.marked = True

    def __str__(self):
        return "{0:2d}{1}".format(
            self.value,
            "*" if self.marked else " "
        )

    def __repr__(self):
        return self.__str__()


class Board:
    def __init__(self, rows_nums):
        self.rows = []
        for row in rows_nums:
            self.rows.append([ Space(i) for i in row ])

    def mark(self, call):
        for r, row in enumerate(self.rows):
            for c, space in enumerate(row):
                if space.value == call:
                    # print(f"  Marking space {r},{c}={space.value}")
                    space.mark()

    def is_winner(self):
        for row in self.rows:
            if all([ r.marked for r in row ]):
                return True
        for index in range(len(self.rows[0])):
            if all([ row[index].marked for row in self.rows ]):
                return True
        return False

    def score(self):
        # print("***********")
        score = 0
        for row in self.rows:
            for space in row:
                if not space.marked:
                    score += space.value
                    # print(f"Added {space.value} to score {score}")
                else:
                    pass
                    # print(f'Skipped marked {space.value}')
        # print("***********")
        return score

    def __str__(self):
        s = ""
        for row in self.rows:
            s += " ".join([ str(i) for i in row ]) + "\n"
        return s

    def __repr__(self):
        return self.__str__()

class Bingo:
    @classmethod
    def loader(self, filename):
        with open(filename) as infile:
            lines = infile.readlines()
        calls = [int(i) for i in lines[0].split(',')]
        #read boards
        boards = []
        for start in range(2,len(lines),6):
            rows = []
            for i in range(5):
                index = start + i
                row = [ int(s) for s in lines[index].strip().split() ]
                assert len(row) == 5
                rows.append(row)
            if start+5 < len(lines):
                assert len(lines[start+5].strip()) == 0
            boards.append(Board(rows))
        return Bingo(calls, boards)

    def __init__(self, calls, boards):
        self.calls = calls
        self.boards = boards

    def has_winner(self):
        for board in self.boards:
            if board.is_winner():
                return board
        return None

    def mark_boards_to_win(self):
        for call in self.calls:
            print("Marking ", call)
            for i, board in enumerate(self.boards):
                # print("Board", i+1)
                board.mark(call)
        
            winning_board = self.has_winner()
            if winning_board != None:
                print("Winner:")
                print(winning_board)
                print("Board score:", winning_board.score())
                # print(winning_board)
                print("Last call: ", call)
                print("Game score", winning_board.score()*call)

                break

    def get_non_winner_boards(self):
        return [ b for b in self.boards if not b.is_winner()]

    def mark_boards_to_lose(self):
        last_board = None
        for call in self.calls:
            print("Marking ", call)
            for i, board in enumerate(self.boards):
                # print("Board", i+1)
                board.mark(call)

            if last_board is None:
                #looking for the last board to win
                non_win = self.get_non_winner_boards()
                if len(non_win) == 1:
                    last_board = non_win[0]
                    print("Found last board")
                    print(last_board)
            else:
                #waiting for the last board to win
                if last_board.is_winner():
                    #check:  all boards should be winners
                    for board in self.boards:
                        assert board.is_winner()

                    print("Last board finally won:")
                    print(last_board)
                    print("Board score:", last_board.score())
                    # print(last_board)
                    print("Last call: ", call)
                    print("Game score", last_board.score()*call)
    
                    return
        
    def __str__(self):
        s = ",".join([ str(i) for i in self.calls ]) + "\n\n"
        s += "\n".join([ str(b) for b in self.boards ])
        return s

    def __repr__(self):
        return self.__str__()


# part1 = Bingo.loader("day4_test.txt")
part1 = Bingo.loader("day4.txt")
with open("day4.check", "w") as outfile:
    outfile.write(str(part1))

# part1.mark_boards_to_win()
# Board score: 911
# Last call:  96
# Game score 87456

part1.mark_boards_to_lose()
# Board score: 399
# Last call:  39
# Game score 15561