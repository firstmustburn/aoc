from day21 import *
import pytest


def test_game_node():

    GameNode.reset_counter()

    config = GameConfig(
        player_count=2,
        win_score=21,
        board_length=10,
        dice_rolls_per_turn=3,
        dice_sides=3)

    dice_counts = GameIterator.permute_dice(config.dice_rolls_per_turn, config.dice_sides)
    
    
    n = GameNode(config, [], 1, [4,8],[0,0], 0)
    assert n.index == 1
    assert n.parent_sequence == []
    assert n.node_cardinality == 1
    assert n.player_positions == [4,8]
    assert n.player_scores == [0,0]
    assert n.next_player == 0
    assert n.get_winner() == None

    n = n.iterate_game(3, dice_counts[3])
    assert n.index == 2
    assert n.parent_sequence == [3]
    assert n.node_cardinality == 1*dice_counts[3]
    assert n.player_positions == [7,8]
    assert n.player_scores == [8,0] #+ pos+1
    assert n.next_player == 1
    assert n.get_winner() == None

    n = n.iterate_game(7, dice_counts[7])
    assert n.index == 3
    assert n.parent_sequence == [3,7]
    assert n.node_cardinality == 1*dice_counts[3]*dice_counts[7]
    assert n.player_positions == [7,5]
    assert n.player_scores == [8,6] #+ pos+1
    assert n.next_player == 0
    assert n.get_winner() == None

    n = n.iterate_game(5, dice_counts[5])
    assert n.index == 4
    assert n.parent_sequence == [3,7,5]
    assert n.node_cardinality == 1*dice_counts[3]*dice_counts[7]*dice_counts[5]
    assert n.player_positions == [2,5]
    assert n.player_scores == [11,6] #+ pos+1
    assert n.next_player == 1
    assert n.get_winner() == None

    n = n.iterate_game(9, dice_counts[9])
    assert n.index == 5
    assert n.parent_sequence == [3,7,5,9]
    assert n.node_cardinality == 1*dice_counts[3]*dice_counts[7]*dice_counts[5]*dice_counts[9]
    assert n.player_positions == [2,4]
    assert n.player_scores == [11,11] #+ pos+1
    assert n.next_player == 0
    assert n.get_winner() == None

    n = n.iterate_game(7, dice_counts[7])
    assert n.index == 6
    assert n.parent_sequence == [3,7,5,9,7]
    assert n.node_cardinality == 1*dice_counts[3]*dice_counts[7]*dice_counts[5]*dice_counts[9]*dice_counts[7]
    assert n.player_positions == [9,4]
    assert n.player_scores == [21,11] #+ pos+1
    assert n.next_player == 1
    assert n.get_winner() == 0

    #can't iterate past the win
    with pytest.raises(AssertionError):
        n.iterate_game(5, dice_counts[5])




# def test_day21_2():

#     start_positions = [4,8]

#     config = GameConfig(
#         player_count=2,
#         win_score=11,
#         board_length=10,
#         dice_rolls_per_turn=2,
#         dice_sides=2)    

#     game = GameIterator(config, start_positions)
#     game.do_iteration()

#     print("**************************************************")
#     print("Game win counts:", game.win_counts)





def test_permute_dice():

    counts = GameIterator.permute_dice(3,3)
    assert sum([v for v in counts.values()] )== 27
    assert counts[3] == 1
    assert counts[4] == 3
    assert counts[5] == 6
    assert counts[6] == 7
    assert counts[7] == 6
    assert counts[8] == 3
    assert counts[9] == 1


def  test_die_generator():

    dg = DiracDieGenerator(3, 4)

    expected_sequence = [
        [1,1,1,1],
        [2,1,1,1],
        [3,1,1,1],
        [1,2,1,1],
        [2,2,1,1],
        [3,2,1,1],
        [1,3,1,1],
        [2,3,1,1],
        [3,3,1,1],

        [1,1,2,1],
        [2,1,2,1],
        [3,1,2,1],
        [1,2,2,1],
        [2,2,2,1],
        [3,2,2,1],
        [1,3,2,1],
        [2,3,2,1],
        [3,3,2,1],

        [1,1,3,1],
        [2,1,3,1],
        [3,1,3,1],
        [1,2,3,1],
        [2,2,3,1],
        [3,2,3,1],
        [1,3,3,1],
        [2,3,3,1],
        [3,3,3,1],

        [1,1,1,2],
        [2,1,1,2],
        [3,1,1,2],
        [1,2,1,2],
        [2,2,1,2],
        [3,2,1,2],
        [1,3,1,2],
        [2,3,1,2],
        [3,3,1,2],

        [1,1,2,2],
        [2,1,2,2],
        [3,1,2,2],
        [1,2,2,2],
        [2,2,2,2],
        [3,2,2,2],
        [1,3,2,2],
        [2,3,2,2],
        [3,3,2,2],

        [1,1,3,2],
        [2,1,3,2],
        [3,1,3,2],
        [1,2,3,2],
        [2,2,3,2],
        [3,2,3,2],
        [1,3,3,2],
        [2,3,3,2],
        [3,3,3,2],

        [1,1,1,3],
        [2,1,1,3],
        [3,1,1,3],
        [1,2,1,3],
        [2,2,1,3],
        [3,2,1,3],
        [1,3,1,3],
        [2,3,1,3],
        [3,3,1,3],

        [1,1,2,3],
        [2,1,2,3],
        [3,1,2,3],
        [1,2,2,3],
        [2,2,2,3],
        [3,2,2,3],
        [1,3,2,3],
        [2,3,2,3],
        [3,3,2,3],

        [1,1,3,3],
        [2,1,3,3],
        [3,1,3,3],
        [1,2,3,3],
        [2,2,3,3],
        [3,2,3,3],
        [1,3,3,3],
        [2,3,3,3],
        [3,3,3,3],
    ]

    for expected in expected_sequence:
        assert not dg.is_exhausted()
        die = dg.get_next_die()
        assert die.roll_sequence == expected

    assert dg.is_exhausted()

    #this last one should fail
    with pytest.raises(RuntimeError):
        die = dg.get_next_die()


def test_game():
    start="""Player 1 starting position: 4
Player 2 starting position: 8
"""
    start_positions = load(start)
    players = [Player(p) for p in start_positions ]
    die = DDie()
    game = Game(players, die)

    # Player 1 rolls 1+2+3 and moves to space 10 for a total score of 10.
    played = game.turn()
    assert played is players[0]
    assert played.score == 10
    assert played.position == (10-1)
    assert die.roll_count == 3

    # Player 2 rolls 4+5+6 and moves to space 3 for a total score of 3.
    # Player 1 rolls 7+8+9 and moves to space 4 for a total score of 14.
    # Player 2 rolls 10+11+12 and moves to space 6 for a total score of 9.
    # Player 1 rolls 13+14+15 and moves to space 6 for a total score of 20.
    # Player 2 rolls 16+17+18 and moves to space 7 for a total score of 16.
    # Player 1 rolls 19+20+21 and moves to space 6 for a total score of 26.
    # Player 2 rolls 22+23+24 and moves to space 6 for a total score of 22.
    # ...after many turns...

    # Player 2 rolls 82+83+84 and moves to space 6 for a total score of 742.
    # Player 1 rolls 85+86+87 and moves to space 4 for a total score of 990.
    # Player 2 rolls 88+89+90 and moves to space 3 for a total score of 745.
    # Player 1 rolls 91+92+93 and moves to space 10 for a final score, 1000.

    #play the rest of the turns
    while not game.is_win():
        game.turn()

    print("Winner", game.winner)
    print("Losers", game.losers)
    print("Die: ", die)

    # Since player 1 has at least 1000 points, player 1 wins and the game ends. At this point, the 
    # losing player had 745 points and the die had been rolled a total of 993 times; 
    # 745 * 993 = 739785.

    assert game.losers[0].score == 745
    assert die.roll_count == 993
    assert game.losers[0].score * die.roll_count == 739785

    assert len(game.losers) == 1
    print("Loser score * dice rolls = ",  )


