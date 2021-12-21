from typing import Sequence

class Die:
    def __init__(self):
        self.roll_count = 0
    
    def roll(self):
        self.roll_count += 1

    def __str__(self):
        return f"Die(rolls={self.roll_count})"

    def __repr__(self):
        return self.__str__()


class DiracDieGenerator:
    """Generate die sequences using a base num_sides adder incremented for every die"""

    def __init__(self, num_sides, num_rolls):
        self.num_sides = num_sides
        self.roll_sequence = [0]* num_rolls
        self._is_exhausted = False

    def _make_die(self):
        #when making a die, increment the roll sequence so the die rolls are e.g., 1-3 instead of 0-2
        return DiracDie([ s+1 for s in self.roll_sequence ])

    def is_exhausted(self):
        return self._is_exhausted

    def get_next_die(self):
        if self._is_exhausted:
            raise RuntimeError("Ran out of rolls.  Make num_rolls larger")

        result = self._make_die()
        #increment the roll sequence
        carry = 1  #this carry in is what starts the addition sequence
        for current_place in range(len(self.roll_sequence)):
            self.roll_sequence[current_place] += carry
            if self.roll_sequence[current_place] >= self.num_sides:
                #roll over to the next place  
                self.roll_sequence[current_place] = 0
                carry = 1
            else:
                #no rollover
                carry = 0
                #we can stop if there's no carry
                break
        #if we get here with a carry out, we have asked for too many rolls
        if carry == 1:
            self._is_exhausted = True
        return result

class DiracDie(Die):
    def __init__(self, roll_sequence):
        super().__init__()
        self.roll_sequence = roll_sequence
        self.index = 0

    def roll(self):
        result = self.roll_sequence[self.index]
        self.index += 1
        return result

    def __str__(self):
        return f"Die(rolls={self.roll_count}, sequence={self.roll_sequence})"


class DeterministicDie(Die):
    def __init__(self):
        super().__init__()
        self.next_roll = 1

    def roll(self):
        super().roll()
        result = self.next_roll
        self.next_roll += 1
        return result


class Player:
    def __init__(self, initial_pos: int):
        self.initial_pos = initial_pos
        self._total_wins = 0
        self.reset()

    def add_win(self):
        self._total_wins = 0

    def get_total_wins(self):
        return self._total_wins

    def reset(self):
        """Clears intermediate state, but not total wins"""
        self.position = self.initial_pos
        self.score = 0


    def __str__(self):
        return f"Player(ipos={self.initial_pos}, pos={self.position}, score={self.score}, total_wins={self._total_wins})"

    def __repr__(self):
        return self.__str__()

class Game:

    def __init__(self, players: Sequence[Player], die:Die, roll_count:int = 3):
        self.players = players
        self.die = die

        self.board_length = 10
        self.win_score = 1000
        self.roll_count = roll_count

        self.next_player = 0
        self.winner = None
        self.losers = []

        for player in self.players:
            assert player.position >= 0 and player.position < self.board_length 

    def turn(self):
        assert not self.is_win() #don't keep playing
        #choose a player
        player = self.players[self.next_player]
        self.next_player = (self.next_player+1)%2

        advance = sum([ self.die.roll() for i in range(self.roll_count) ])

        new_position = (player.position + advance)%self.board_length
        player.position = new_position
        player.score += new_position+1 #spots are labeled one-indexed

        return player

    def is_win(self):
        if self.winner is not None:
            return True
        #otherwise check
        for player in self.players:
            if player.score >= self.win_score:
                self.winner = player
                self.losers = []
                for player in self.players:
                    if player is self.winner:
                        continue
                    assert player.score < self.win_score
                    self.losers.append(player)
                return True
        return False

def load(positions):
    def parse(p):
        tokens = p.split(":")
        assert len(tokens)==2
        return int(tokens[1].strip())-1

    p1, p2 = positions.strip().split('\n')
    return parse(p1),parse(p2)

def play_p1(positions):
    start_positions = load(positions)
    players = [Player(p) for p in start_positions ]
    die = DeterministicDie()
    game = Game(players, die)
    while not game.is_win():
        game.turn()

    print("Winner", game.winner)
    print("Losers", game.losers)
    print("Die: ", die)

    assert len(game.losers) == 1
    print("Loser score * dice rolls = ", game.losers[0].score * die.roll_count )


def play_games_to_length(players, length):

    print("Playing games of length", length)
    
    # play games for all the rolls of the specified length
    # add wins to player state **only** when they win at this length

    roll_count = 3

    #could optimize for die that iterates all three rolls as single state
    die_gen = DiracDieGenerator(3,length*roll_count)
    
    #stats to track
    #win counts are tracking in the player state
    longer_games_exist = False

    game_count = 0
    while not die_gen.is_exhausted():
        game_count += 1
        if game_count % 100000 == 0:
            print("   ",game_count, "games run")

        #set up the next game
        die = die_gen.get_next_die()
        # print(game_count, die)
        for p in players:
            p.reset()

        game = Game(players, die, roll_count=roll_count)

        for turn in range(length):
            game.turn()

            if game.is_win():
                break

        if turn == length-1:
            #we ran the full number of turns
            if game.is_win():
                game.winner.add_win()
            else:
                #no winner, so remember longer games exist
                longer_games_exist = True
        # else ignore games that finished in fewer turns, they were tracked on previous passes

    print("   ran", game_count, "games")

    # now we've played all the games to length
    return longer_games_exist

def play_p2(positions):
    start_positions = load(positions)
    
    players = [Player(p) for p in start_positions ]

    game_length = 5 #can't win a game in fewer than 5 moves
    more_games_exist = True

    while more_games_exist:

        more_games_exist = play_games_to_length(players, game_length)
        game_length += 1
        
    #print win counts
    for p in players:
        print(p)



    





    print("Winner", game.winner)
    print("Losers", game.losers)
    print("Die: ", die)

    assert len(game.losers) == 1
    print("Loser score * dice rolls = ", game.losers[0].score * die.roll_count )


if __name__ == "__main__":
    #test case
    start="""Player 1 starting position: 4
Player 2 starting position: 8
"""

    #input case
#     start="""Player 1 starting position: 6
# Player 2 starting position: 3
# """
    play_p1(start)

    # part 1
    # Winner Player(ipos=5, pos=7, score=1006)
    # Losers [Player(ipos=2, pos=5, score=749)]
    # Die:  Die(rolls=1005)
    # Loser score * dice rolls =  752745

    play_p2(start)