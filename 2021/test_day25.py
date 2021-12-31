from day25 import *


def test_day25_example_1():

    data_in = """...>>>>>..."""
    step1_out = """...>>>>.>.."""
    step2_out = """...>>>.>.>."""

    state = SeaBed.load(data_in)
    assert state.row_count == 1
    assert state.col_count == 11

    step1 = SeaBed.load(step1_out)
    step2 = SeaBed.load(step2_out)

    move_count = state.step()
    assert move_count == 1
    assert state == step1
    assert state.step_count == 1

    move_count = state.step()
    assert move_count == 2
    assert state == step2
    assert state.step_count == 2

def test_day25_example_2():

    data_in = """..........
.>v....v..
.......>..
.........."""
    step1_out = """..........
.>........
..v....v>.
.........."""

    state = SeaBed.load(data_in)
    assert state.row_count == 4
    assert state.col_count == 10

    step1 = SeaBed.load(step1_out)

    move_count = state.step()
    assert move_count == 3
    assert state == step1
    assert state.step_count == 1


def test_day25_example_3():

    data_in = """...>...
.......
......>
v.....>
......>
.......
..vvv..
"""
    step_outs = [
        """..vv>..
.......
>......
v.....>
>......
.......
....v..
""",
        """....v>.
..vv...
.>.....
......>
v>.....
.......
.......
""",
        """......>
..v.v..
..>v...
>......
..>....
v......
.......
""",
        """>......
..v....
..>.v..
.>.v...
...>...
.......
v......
"""
    ]
    move_counts = [
        5,7,7,6
    ]

    state = SeaBed.load(data_in)
    assert state.row_count == 7
    assert state.col_count == 7

    step_count = 0
    for step_out, expected_move_count in zip(step_outs, move_counts):
        step_count += 1

        step = SeaBed.load(step_out)

        move_count = state.step()

        assert move_count == expected_move_count
        assert state == step
        assert state.step_count == step_count

def test_day25_example_4():
    initial_state = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
    step_outs = {
        1:"""....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v
""",
        2:""">.v.v>>..v
v.v.>>vv..
>v>.>.>.v.
>>v>v.>v>.
.>..v....v
.>v>>.v.v.
v....v>v>.
.vv..>>v..
v>.....vv.
""",
        3:"""v>v.v>.>v.
v...>>.v.v
>vv>.>v>..
>>v>v.>.v>
..>....v..
.>.>v>v..v
..v..v>vv>
v.v..>>v..
.v>....v..
""",
        4:"""v>..v.>>..
v.v.>.>.v.
>vv.>>.v>v
>>.>..v>.>
..v>v...v.
..>>.>vv..
>.v.vv>v.v
.....>>vv.
vvv>...v..
""",
        5:"""vv>...>v>.
v.v.v>.>v.
>.v.>.>.>v
>v>.>..v>>
..v>v.v...
..>.>>vvv.
.>...v>v..
..v.v>>v.v
v.v.>...v.
""",
        10:"""..>..>>vv.
v.....>>.v
..v.v>>>v>
v>.>v.>>>.
..v>v.vv.v
.v.>>>.v..
v.v..>v>..
..v...>v.>
.vv..v>vv.
""",
        20:"""v>.....>>.
>vv>.....v
.>v>v.vv>>
v>>>v.>v.>
....vv>v..
.v.>>>vvv.
..v..>>vv.
v.v...>>.v
..v.....v>
""",    
        30:""".vv.v..>>>
v>...v...>
>.v>.>vv.>
>v>.>.>v.>
.>..v.vv..
..v>..>>v.
....v>..>v
v.v...>vv>
v.v...>vvv
""",
        40:""">>v>v..v..
..>>v..vv.
..>>>v.>.v
..>>>>vvv>
v.....>...
v.v...>v>>
>vv.....v>
.>v...v.>v
vvv.v..v.>
""",

        50:"""..>>v>vv.v
..v.>>vv..
v.>>v>>v..
..>>>>>vv.
vvv....>vv
..v....>>>
v>.......>
.vv>....v>
.>v.vv.v..
""",
        55:"""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv...>..>
>vv.....>.
.>v.vv.v..
""",
        56:"""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv....>.>
>vv......>
.>v.vv.v..
""",
        57:"""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..
""",
        58:"""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..
""",
    }

    state = SeaBed.load(initial_state)
    assert state.row_count == 9
    assert state.col_count == 10

    step_count = 0
    while 1:
        step_count += 1

        move_count = state.step()

        #check step against reference if there is one
        if step_count in step_outs:
            step = SeaBed.load(step_outs[step_count])
            assert step == state

        #stop when no more moves
        if move_count == 0:
            break

    assert step_count == 58

    #repeat test using run_to_no_motion
    state = SeaBed.load(initial_state)
    state.run_to_no_motion()
    assert state.step_count == 58
    assert state == SeaBed.load(step_outs[58])

