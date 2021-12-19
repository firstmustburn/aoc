from day14 import *

def test_chunks():
    input = "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    chunks = PowerRuleSet._chunk(input)
    print(input)
    for c in chunks:
        assert math.log(len(c),2) == math.floor(math.log(len(c),2))
    assert sum([ len(c) for c in chunks]) - len(chunks) + 1 == len(input)

def test_chunks_simple():
    input = "NNCB"
    chunks = PowerRuleSet._chunk(input)
    assert chunks == ["NN","NC","CB"]

if __name__ == "__main__":
    test_chunks_simple()