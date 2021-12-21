from collections import namedtuple, Counter
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



####################################################################################################


GameConfig = namedtuple("GameConfig",["player_count","win_score", "board_length", "dice_rolls_per_turn", "dice_sides"])

class GameNode:

    COUNTER = 0

    @classmethod
    def get_counter(cls):
        cls.COUNTER += 1
        return cls.COUNTER

    @classmethod
    def reset_counter(cls):
        cls.COUNTER = 0

    def __init__(self, game_config, parent_sequence, node_cardinality, player_positions, player_scores, next_player):
        self.game_config = game_config
        self.parent_sequence = parent_sequence
        self.node_cardinality = node_cardinality # the number of times this games state can occur
        self.player_positions = player_positions
        self.player_scores = player_scores
        self.next_player = next_player
        self.index = self.get_counter()

    def get_winner(self):
        for i in range(len(self.player_scores)):
            if self.player_scores[i] >= self.game_config.win_score:
                return i
        return None

    def iterate_game(self, next_roll, num_rolls):
        #num_rolls is the number of ways we can get the rolls
        assert self.get_winner() is None

        # print(" "*self.parent_sequence, next_roll)

        new_next_player = (self.next_player + 1) % self.game_config.player_count
        new_player_positions = list(self.player_positions)
        new_player_scores = list(self.player_scores)
        new_sequence = self.parent_sequence + [next_roll]
        new_cardinality = self.node_cardinality * num_rolls

        #use self.next_player for this iteration, but increment for the child node
        new_player_positions[self.next_player] = (new_player_positions[self.next_player] + next_roll) % self.game_config.board_length
        new_player_scores[self.next_player] += new_player_positions[self.next_player]+1 # +1 because positions are zero indexed

        return GameNode(self.game_config, 
            new_sequence, new_cardinality,
            new_player_positions, new_player_scores, new_next_player)

    def __str__(self):
        return f"index={self.index}, cardinality={self.node_cardinality}, sequence={self.parent_sequence}, scores={self.player_scores}"

    def __repr__(self):
        return self.__str__()

class GameIterator:
    """walk a tree of the die states accumulating wins and losses for each player as we go
    each tree state is the state of the game through the sequence of moves for all its parents
    we stop walking the tree when we reach a win condition
    when we've completed all the iteratins for a branch, we delete it to avoid using up all our memory.
    """

    def __init__(self, game_config, initial_positions):
        self.game_config = game_config
        self.initial_positions = initial_positions

        self.dice_counts = self.permute_dice(self.game_config.dice_rolls_per_turn, self.game_config.dice_sides)

        num_players = len(initial_positions)

        self.root = GameNode(self.game_config, [], 1, initial_positions, [0]*num_players, 0)
        self.win_counts = [0]*num_players

    @staticmethod
    def permute_dice(rolls_per_turn, dice_sides):

        counts = Counter()

        def add_roll(sequence_to_extend):
            sequences = []
            for side in range(dice_sides):
                new_sequence = sequence_to_extend + [side+1]
                if len(new_sequence) == rolls_per_turn:
                    sequences.append(new_sequence)
                    # print(new_sequence)
                else:
                    #keep going deeper
                    sequences.extend(add_roll(new_sequence))
            return sequences

        all_sequences = add_roll([])

        for sequence in all_sequences:
            counts[sum(sequence)] = counts[sum(sequence)] + 1

        print(counts)

        assert sum([v for v in counts.values()]) == dice_sides**rolls_per_turn

        return counts


    def do_iteration(self):
        """top level start for tree iteration"""
        self._do_iteration_recursive(self.root)

        
    def _do_iteration_recursive(self, current_node):

        if current_node.index % 1000000 == 0:
            print(f"[{self.win_counts[0]:15d}] ,{self.win_counts[1]:15d}]", current_node)

        #one child for each dice roll
        for dice_roll, num_rolls in self.dice_counts.items():
            child_node = current_node.iterate_game(dice_roll, num_rolls)

            winner = child_node.get_winner()
            if winner is None:
                #recurse if no winner
                self._do_iteration_recursive(child_node)
            else:
                # there is a winner -- halting condition for the depth of the tree walk
                # record the score num_rolls time, because there are that many dice rolls to 
                # get to this outcome
                self.win_counts[winner] += child_node.node_cardinality

            


def play_p2(positions):
    start_positions = load(positions)

    config = GameConfig(
        player_count=2,
        win_score=21,
        board_length=10,
        dice_rolls_per_turn=3,
        dice_sides=3)    

    game = GameIterator(config, start_positions)
    game.do_iteration()

    print("**************************************************")
    print("Game win counts:", game.win_counts)





if __name__ == "__main__":
    #test case
#     start="""Player 1 starting position: 4
# Player 2 starting position: 8
# """

    #input case
    start="""Player 1 starting position: 6
Player 2 starting position: 3
"""
    play_p1(start)

    # part 1
    # Winner Player(ipos=5, pos=7, score=1006)
    # Losers [Player(ipos=2, pos=5, score=749)]
    # Die:  Die(rolls=1005)
    # Loser score * dice rolls =  752745

    play_p2(start)

    #     **************************************************
    # Game win counts: [309196008717909, 227643103580178]


