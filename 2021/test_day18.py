
from day18 import *

# def test_explode_str():
#     tests = [
#         ('[[[[[9,8],1],2],3],4]','[[[[0,9],2],3],4]'),
#         ('[7,[6,[5,[4,[3,2]]]]]','[7,[6,[5,[7,0]]]]'),
#         ('[[6,[5,[4,[3,2]]]],1]','[[6,[5,[7,0]]],3]'),
#         ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
#         ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
#     ]

#     for inval, outval in tests:
#         result, was_exploded = StringSnails.explode(inval)
#         assert outval == result
#         assert was_exploded == True

def test_explode_obj():
    tests = [
        ('[[[[[9,8],1],2],3],4]','[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]','[7,[6,[5,[7,0]]]]'),
        ('[[6,[5,[4,[3,2]]]],1]','[[6,[5,[7,0]]],3]'),
        ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
        ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
        #my own test cases
        ('[[5,4],[[[[3,2],1],2],3]]','[[5,7],[[[0,3],2],3]]'),
        ('[[[[13,0],[[7,7],[7,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]]',
         '[[[[13,7],[0,[14,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]]')
    ]

    for inval, outval in tests:
        in_num = SnailOperations.parse_number(inval)
        out_num = SnailOperations.parse_number(outval)
        
        print("Exploding ", in_num)
        was_exploded = in_num.explode()
        print("      --> ", in_num)
        assert in_num == out_num
        assert was_exploded == True


def test_split_obj():
    tests = [
        ('[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[0,[11,3]],[[6,3],[8,8]]]]]',
         '[[[[4,0],[5,4]],[[7,0],[[7,8],5]]],[10,[[0,[11,3]],[[6,3],[8,8]]]]]')
    ]

    for inval, outval in tests:
        in_num = SnailOperations.parse_number(inval)
        
        was_split = in_num.split()
        print("      --> ", in_num)
        assert str(in_num) == outval
        assert was_split == True


# def test_extended_str():

#     val1 = '[[[[4,3],4],4],[7,[[8,4],9]]]'
#     val2 = '[1,1]'

#     # after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
#     value = StringSnails.StringSnails.add(val1, val2)
#     assert value == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'

#     # after StringSnails.explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
#     value, was_exp = StringSnails.explode(value)
#     assert was_exp == True
#     assert value == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'
#     # after StringSnails.explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
#     value, was_exp = StringSnails.explode(value)
#     assert was_exp == True
#     assert value == '[[[[0,7],4],[15,[0,13]]],[1,1]]'
#     # after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
#     value, was_spl = split(value)
#     assert was_spl == True
#     assert value == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
#     # after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
#     value, was_spl = split(value)
#     assert was_spl == True
#     assert value == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
#     # after StringSnails.explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
#     value, was_exp = StringSnails.explode(value)
#     assert was_exp == True
#     assert value == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

#     #test it as a single StringSnails.reduce action
#     value = StringSnails.add(val1, val2)
#     assert value == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'

#     value = StringSnails.reduce(value)
#     assert value == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'


def test_extended_obj():

    val1 = '[[[[4,3],4],4],[7,[[8,4],9]]]'
    val2 = '[1,1]'

    val1 = SnailOperations.parse_number(val1)
    val2 = SnailOperations.parse_number(val2)


    # after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    value = SnailOperations.add(val1, val2)
    assert str(value) == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'

    # after StringSnails.explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    was_exp = value.explode()
    assert was_exp == True
    assert str(value) == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'

    # after StringSnails.explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
    was_exp = value.explode()
    assert was_exp == True
    assert str(value) == '[[[[0,7],4],[15,[0,13]]],[1,1]]'
    # after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    was_spl = value.split()
    assert was_spl == True
    assert str(value) == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
    # after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    was_spl = value.split()
    assert was_spl == True
    assert str(value) == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
    # after StringSnails.explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    was_exp = value.explode()
    assert was_exp == True
    assert str(value) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'


    val1 = '[[[[4,3],4],4],[7,[[8,4],9]]]'
    val2 = '[1,1]'

    val1 = SnailOperations.parse_number(val1)
    val2 = SnailOperations.parse_number(val2)

    value = SnailOperations.add(val1, val2)
    assert str(value) == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'

    was_reduced = value.reduce()
    assert str(value) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
    assert was_reduced == True



# def test_specific_sequence_parts_str():
#     val1 = '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]'
#     val2 = '[2,9]'
#     expected = '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]'
#     result = StringSnails.add(val1, val2)
#     print(result)
#     result = StringSnails.reduce(result)
#     assert result == expected

#     val1 = '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]'
#     val2 = '[1,[[[9,3],9],[[9,0],[0,7]]]]'
#     expected = '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]'
#     result = StringSnails.add(val1, val2)
#     print(result)
#     result = StringSnails.reduce(result)
#     assert result == expected

#     val1 = '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]'
#     val2 = '[[[5,[7,4]],7],1]'
#     expected = '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]'
#     result = StringSnails.add(val1, val2)
#     print(result)
#     result = StringSnails.reduce(result)
#     assert result == expected

#     val1 = '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]'
#     val2 = '[[[[4,2],2],6],[8,7]]'
#     expected = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
#     result = StringSnails.add(val1, val2)
#     print(result)
#     result = StringSnails.reduce(result)
#     assert result == expected


# def test_addition_sequences_str():
#     inputs = [None]*4
#     outputs = [None]*4
    
#     outputs[0] = '[[[[1,1],[2,2]],[3,3]],[4,4]]'
#     inputs[0] = """[1,1]
# [2,2]
# [3,3]
# [4,4]
# """
#     outputs[1] = '[[[[3,0],[5,3]],[4,4]],[5,5]]'
#     inputs[1] = """[1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# """
#     outputs[2] = '[[[[5,0],[7,4]],[5,5]],[6,6]]'
#     inputs[2] = """[1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# [6,6]
# """

#     outputs[3] = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
#     inputs[3] = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
# [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
# [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
# [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
# [7,[5,[[3,8],[1,4]]]]
# [[2,[2,2]],[8,[8,1]]]
# [2,9]
# [1,[[[9,3],9],[[9,0],[0,7]]]]
# [[[5,[7,4]],7],1]
# [[[[4,2],2],6],[8,7]]
# """

#     for input, output in zip(inputs, outputs):
#         nums = StringSnails.parse_number_string_to_list(input)
#         result = StringSnails.add_number_list(nums)
#         assert result == output


def test_addition_sequences_obj():
    inputs = [None]*4
    outputs = [None]*4
    
    outputs[0] = '[[[[1,1],[2,2]],[3,3]],[4,4]]'
    inputs[0] = """[1,1]
[2,2]
[3,3]
[4,4]
"""
    outputs[1] = '[[[[3,0],[5,3]],[4,4]],[5,5]]'
    inputs[1] = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
"""
    outputs[2] = '[[[[5,0],[7,4]],[5,5]],[6,6]]'
    inputs[2] = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""

    outputs[3] = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    inputs[3] = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

    for input, output in zip(inputs, outputs):

        invals = SnailOperations.parse_number_list(input)
        result = SnailOperations.add_number_list(invals)
        assert str(result) == output


def test_magnitude():
    test_cases = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]

    for input, output in test_cases:

        input = SnailOperations.parse_number(input)
        assert input.magnitude() == output 

def test_copy():
    test_cases = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]

    for input, output in test_cases:

        input = SnailOperations.parse_number(input)
        copied = input.copy()
        assert copied.magnitude() == output
        assert input.magnitude() == output 

    output = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    input = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""


    num_list = SnailOperations.parse_number_list(input)
    copied_list = [ n.copy() for n in num_list ]

    result = SnailOperations.add_number_list(num_list)
    copied_result = SnailOperations.add_number_list(copied_list)
    assert result == copied_result

def test_final_example():
    inputs = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """
    output = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    expected_magnitude = 4140

    numbers = SnailOperations.parse_number_list(inputs)
    value = SnailOperations.add_number_list(numbers)
    assert str(value) == output
    assert value.magnitude() == expected_magnitude

def test_cross_sums():
    inputs = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """
    numbers = SnailOperations.parse_number_list(inputs)
    magnitude, value = find_largest_magnitude(numbers)
    assert magnitude == 3993
    assert str(value) == "[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]"

if __name__ == "__main__":
    test_explode_obj()