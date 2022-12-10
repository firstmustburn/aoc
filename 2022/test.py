from day5 import multipop
from day8 import transpose_trees


def test_multipop():
    input = [1,2,3,4]
    popped, output = multipop(input,2)
    assert popped == [3,4]
    assert output == [1,2]

    input = [1,2,3,4]
    popped, output = multipop(input,4)
    assert popped == [1,2,3,4]
    assert output == []

def test_transpose_trees():
    input = [
        [1,2,3],
        [4,5,6],
        [7,8,9],
    ]

    transpose_trees(input)

    assert input == [
        [1,4,7],
        [2,5,8],
        [3,6,9],
    ]

    transpose_trees(input)

    assert input == [
        [1,2,3],
        [4,5,6],
        [7,8,9],
    ]
