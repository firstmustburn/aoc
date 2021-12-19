import math

pairs = {
    "{":"}",
    "(":")",
    "<":">",
    "[":"]",
}
opens = list(pairs.keys())
closes = list(pairs.values())


def check_syntax(line):
    stack = list()

    for c in line:
        if c in opens:
            stack.append(c)
        elif c in closes:
            matched_open = stack.pop()
            expected_close = pairs[matched_open]
            if expected_close != c:
                print(f"For line {line} - Expected {expected_close} but found {c} instead")
                return expected_close, c
        else:
            raise RuntimeError(f"Illegal character {c}")
    #if we get here, there were no syntax errors
    print(f"Line ok: {line}")
    return None, None

def score_syntax(filename):
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    with open(filename) as infile:
        lines = infile.readlines()

    score = 0
    for line in lines:
        expected, actual = check_syntax(line.strip())
        if actual is not None:
            score += scores[actual]
    
    print("Score is", score)



def complete_syntax(line):

    stack = list()

    for c in line:
        if c in opens:
            stack.append(c)
        elif c in closes:
            matched_open = stack.pop()
            expected_close = pairs[matched_open]
            if expected_close != c:
                print(f"Skipping invalid line {line} - Expected {expected_close} but found {c} instead")
                return None
        else:
            raise RuntimeError(f"Illegal character {c}")
    #if we get here, there were no syntax errors
    print(f"Line ok: {line}")

    #now score the remaining stack
    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    score = 0
    close_string = ""
    while len(stack) > 0:
        matched_open = stack.pop()
        matched_close = pairs[matched_open]
        close_string += matched_close
        score = (score * 5) + scores[matched_close]

    print(f"{close_string} - {score} points")

    return score


    return None, None

def complete_syntax_lines(filename):

    with open(filename) as infile:
        lines = infile.readlines()

    score_list = []
    for line in lines:
        score = complete_syntax(line.strip())
        if score is None:
            continue
        score_list.append(score)
    
    #sort the score list
    score_list.sort()

    assert (len(score_list) % 2) == 1
    
    # get the middle score
    winning_index = int(math.floor(len(score_list)/2))
    winning_score = score_list[winning_index]
    print("Winning score is", winning_score)


# score_syntax("day10_test.txt")
# score_syntax("day10.txt")  # Score is 392097

# complete_syntax_lines("day10_test.txt")
complete_syntax_lines("day10.txt")  # Winning score is 4263222782