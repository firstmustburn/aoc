
from util import load_token_list

ROCK = 1
PAPER = 2
SCISSORS = 3

LOSS = 0
WIN = 6
DRAW = 3

X = "X"
Y = "Y"
Z = "Z"
A = "A"
B = "B"
C = "C"

coding = {
    A:ROCK,
    B:PAPER,
    C:SCISSORS,
    X:ROCK,
    Y:PAPER,
    Z:SCISSORS,
}
#win implies winner for the second player
game_score = {
    (ROCK,ROCK):DRAW,
    (ROCK,PAPER):WIN,
    (ROCK,SCISSORS):LOSS,
    (PAPER,PAPER):DRAW,
    (PAPER,ROCK):LOSS,
    (PAPER,SCISSORS):WIN,
    (SCISSORS,SCISSORS):DRAW,
    (SCISSORS,PAPER):LOSS,
    (SCISSORS,ROCK):WIN,
}
choice_score = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

# X = lose, Y = draw, Z = win
chosen_outcome = {
    (ROCK,X): SCISSORS,
    (ROCK,Y): ROCK,
    (ROCK,Z): PAPER,
    (PAPER,X): ROCK,
    (PAPER,Y): PAPER,
    (PAPER,Z): SCISSORS,
    (SCISSORS,X): PAPER,
    (SCISSORS,Y): SCISSORS,
    (SCISSORS,Z): ROCK,
}

def compute_score_1(play):
    #convert the letters into rock, paper, or scissors context
    p1 = coding[play[0]]
    p2 = coding[play[1]]
    return game_score[(p1,p2)] + choice_score[p2]

def compute_score_2(play):
    #convert the letters into rock, paper, or scissors context
    p1 = coding[play[0]]
    #for the second letter, look up the chosen outcome instead
    p2 = chosen_outcome[(p1,play[1])]
    return game_score[(p1,p2)] + choice_score[p2]

def play_games(games, score_fun):
    scores = []

    for game in games:
        this_score = score_fun(game)
        scores.append(this_score)
        # print(game, this_score)

    return sum(scores)

def part1(games):
    return play_games(games, compute_score_1)

def part2(games):
    return play_games(games, compute_score_2)


# filename="day2/test.txt"
filename="day2/input.txt"

games = load_token_list(filename)

print("part 1", part1(games))

print("part 2", part2(games))

