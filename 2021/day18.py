import re
import math

CROSS_CHECK = True

def find_deepest_parens(strval):
    bracket_count = 0
    max_depth = 0
    for c in strval:
        if c == '[':
            bracket_count += 1
            max_depth = max(max_depth, bracket_count)
        elif c == ']':
            bracket_count -= 1
    return max_depth

class SnailBase:

    def __init__(self):
        self._parent = None

    def has_parent(self):
        return self._parent is not None

    def get_parent(self):
        return self._parent

    def set_parent(self, new_parent):
        assert self._parent is None
        self._parent= new_parent

    def clear_parent(self):
        self._parent = None

    def depth(self):
        if self._parent is None:
            return 0
        else:
            return self._parent.depth()+1

class SnailLiteral(SnailBase):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        return SnailLiteral(self.value)

    def is_literal(self):
        return True

    def is_list(self):
        return False

    def magnitude(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, SnailLiteral):
            return False
        return other.value == self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class SnailList(SnailBase):
    def __init__(self, items):
        super().__init__()
        assert len(items) == 2
        self.items=items
        for i in self.items:
            assert isinstance(i, SnailBase)
            i.set_parent(self)

    def __str__(self):
        return '[' + ','.join([ str(i) for i in self.items ]) + ']'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SnailList):
            return False
        return other.items[0] == self.items[0] and other.items[1] == self.items[1]

    def copy(self):
        item_copy = [ i.copy() for i in self.items ]
        return SnailList(item_copy)

    def magnitude(self):
        return 3 * self.items[0].magnitude() + 2 * self.items[1].magnitude()

    def is_list(self):
        return True

    def is_literal(self):
        return False

    def is_literal_list(self):
        """return True if both items are literals"""
        return all([ i.is_literal() for i in self.items ])

    def search_left(self, search_fcn):
        def search_up(target):
            if target.is_list():
                #search items
                for item in reversed(target.items):
                    #recurse first to go all the way to the end
                    item_search = search_up(item)
                    if item_search is not None:
                        return item_search
                    #check the item itself after recursing
                    if search_fcn(item):
                        return item
                    #else continue to the other item
            #no match found
            return None



        #if we are the root, there can be nothing to the left or right
        if not self.has_parent():
            return None
        #see if we have any siblings
        for left_sib in self.get_parent().get_left_siblings(self):
            if (search_fcn(left_sib)):
                return left_sib
            #try to recurse the sibling
            up_search =search_up(left_sib)
            if up_search is not None:
                return up_search
        if search_fcn(self.get_parent()):
            return self.get_parent()
        #recurse to parent
        return self.get_parent().search_left(search_fcn)


    def get_left_siblings(self, child):
        assert len(self.items) == 2
        assert child in self.items
        if self.items[1] is child:
            #return the one to the left
            return [self.items[0]]
        else:
            #return nothing
            return []

    def get_right_siblings(self, child):
        assert len(self.items) == 2
        assert child in self.items
        if self.items[0] is child:
            #return the one to the right
            return [self.items[1]]
        else:
            #return nothing
            return []

        

    def search_right(self, search_fcn):
        def search_down(target):
            if target.is_list():
                #search items
                for item in target.items:
                    if search_fcn(item):
                        return item
                    #recurse -- depth first
                    item_search = search_down(item)
                    if item_search is not None:
                        return item_search
                    #else continue to the other item
            #no match found
            return None

        #if we are the root, there can be nothing to the left or right
        if not self.has_parent():
            return None
        #see if we have any siblings
        for right_sib in self.get_parent().get_right_siblings(self):
            if (search_fcn(right_sib)):
                return right_sib
            #try to recurse the sibling
            down_search =search_down(right_sib)
            if down_search is not None:
                return down_search
        if search_fcn(self.get_parent()):
            return self.get_parent()
        #recurse to parent
        return self.get_parent().search_right(search_fcn)


    def split(self):
        """Recurse until we find the first candidate for splitting, halt after the first split
        Recursing depth first is the same as going through the number from the left"""
        for index, item in enumerate(self.items):
            if item.is_literal() and item.value >= 10:
                #do the split
                split_item = SnailList([ 
                    SnailLiteral(int(math.floor(item.value/2))),
                    SnailLiteral(int(math.ceil(item.value/2))),
                ])
                #replace the current item
                item.clear_parent()
                split_item.set_parent(self)
                self.items[index] = split_item
                return True
            elif item.is_list():
                #recurse into the list
                list_split_result = item.split()
                if list_split_result:
                    return True
        #we did not find a split in our items or any recursion
        return False

    def explode(self):
        """Recurse until we find the first candidate for explodeing, halt after the first explode
        Recursing depth first is the same as going through the number from the left"""

        def find_literal(item):
            return item.is_literal()

        for index, item in enumerate(self.items):
            if item.is_list() and item.is_literal_list() and item.depth() >= 4:
                #found a candidate for exploding, so explode it
                left_number = item.items[0].value
                right_number = item.items[1].value
                #find the literal to the left
                left_literal = item.search_left(find_literal)
                if left_literal is not None:
                    left_literal.value += left_number
                #find the literal to the right
                right_literal = item.search_right(find_literal)
                if right_literal is not None:
                    right_literal.value += right_number
                #replace the item itself with a 0
                item.clear_parent()
                exploded = SnailLiteral(0)
                exploded.set_parent(self)
                self.items[index] = exploded
                return True
            elif item.is_list():
                #recurse
                item_explode_result = item.explode()
                if item_explode_result:
                    return True
        #we did not find an explode in our items or any recursion
        return False
        
    DOUBLE_DIGIT_NUMBER_ONLY_SEARCH = re.compile(r'\d{2,}')
    def reduce(self):
        # print("*"*80)
        # print("Reducing             ", self) 
        was_reduced = False
        while 1:
            before_str = str(self)
            was_exploded = self.explode()
            if was_exploded:
                was_reduced = True
                # print("Reduced by explode to", self)
                if CROSS_CHECK:
                    string_result, was_exploded = StringSnails.explode(before_str)
                    if str(self) != string_result:
                        # print("Disagreement:")
                        # print("   obj:", str(self))
                        # print("   str:", string_result)
                        assert False
                continue
            else:
                #check the unexploded for deep parens
                assert find_deepest_parens(str(self)) <= 4

            was_split = self.split()
            if was_split:
                was_reduced = True
                # print("Reduced by split to  ", self)
                continue
            else:
                #make sure there's not a larger literal
                m = self.DOUBLE_DIGIT_NUMBER_ONLY_SEARCH.search(str(self))
                # print(self)
                assert m is None

            if not was_exploded and not was_split:
                break
        # print("*"*80)
        return was_reduced



class SnailOperations:

    @classmethod
    def parse_number_list(cls, number_string):
        number_list = number_string.strip().split("\n")
        number_list = [ cls.parse_number(n.strip()) for n in number_list ]
        return number_list

    @classmethod
    def add(cls, snl, snr):
        return SnailList([snl, snr])

    @classmethod
    def add_number_list(cls, num_list):
        assert len(num_list) > 2

        value = num_list[0]
        for to_add in num_list[1:]:
            value = cls.add(value, to_add)
            value.reduce()
        return value

    @classmethod
    def parse_number(cls, number_str):

        def recurse_parse(item):
            if isinstance(item, int):
                sl = SnailLiteral(item)
                return sl
            elif isinstance(item, list):
                sub_items = [ recurse_parse(i) for i in item ]
                return SnailList(sub_items)
            else:
                raise RuntimeError(f"Unsupported type {type(item)}: {item}")

        return recurse_parse(eval(number_str))



class StringSnails:
    PAIR_SEARCH = re.compile(r"[^]]*(\[\d+,\d+\])")
    LAST_NUMBER_SEARCH = re.compile(r'.*?(\d+)\D*$')
    FIRST_NUMBER_SEARCH = re.compile(r'^\D*(\d+)')
    DOUBLE_DIGIT_NUMBER_ONLY_SEARCH = re.compile(r'\d{2,}')

    @classmethod
    def is_balanced(cls, num):
        bracket_count = 0
        for c in num:
            if c == '[':
                bracket_count += 1
            if c == ']':
                bracket_count -= 1
        return bracket_count == 0

    @classmethod
    def add(cls, l, r):
        result = f"[{l},{r}]"
        assert cls.is_balanced(result)
        return result

    @classmethod
    def get_pair_digits(cls, pair_str):
        tokens = pair_str.strip("[]").split(",")
        assert len(tokens) == 2
        return [ int(t) for t in tokens ]

    @classmethod
    def add_and_replace_number_found(cls, str_in, regex, number_to_add):
        match = regex.match(str_in)
        if match is None:
            # print("no match for number replace in '", str_in, "' with ", regex)
            return str_in
        number_start = match.start(1)
        number_end = match.end(1)
        number = int(match.group(1))
        # print("input str", str_in)
        # print("number start:", number_start)
        # print("number end:", number_end)
        # print("number value:", number)
        # print("new number value:", number + number_to_add)

        result = str_in[:number_start] + str(number + number_to_add) + str_in[number_end:]
        # print("result", result)
        return result

    @classmethod
    def explode(cls, num):
        # print(num)
        bracket_count = 0
        for i, c in enumerate(num):
            if c == "[":
                bracket_count += 1
            elif c == "]":
                bracket_count -= 1
            if bracket_count >= 4:
                #find the next pair
                m = cls.PAIR_SEARCH.match(num[i+1:])
                #no match, so nothing to explode
                if m == None:
                    continue
                #found a match for the pair at
                # i+1+m.start(1), i+1+m.end(1)
                # this is the start of the explosion!
                pair_start = i+1+m.start(1)
                pair_end = i+1+m.end(1)
                left_part = num[:pair_start]
                right_part = num[pair_end:]
                pair_digits = cls.get_pair_digits(m.group(1))

                #distribute the pair digits over the left and right parts
                left_part = cls.add_and_replace_number_found(left_part, cls.LAST_NUMBER_SEARCH, pair_digits[0])
                right_part = cls.add_and_replace_number_found(right_part, cls.FIRST_NUMBER_SEARCH, pair_digits[1])
                #replace the original pair with zerio
                num = left_part + "0" + right_part
                assert cls.is_balanced(num)
                return num, True
        return num, False

    @classmethod
    def split(cls, num):
        m = cls.DOUBLE_DIGIT_NUMBER_ONLY_SEARCH.search(num)
        if m is None:
            return num, False
        first_index = m.start(0)
        last_index = m.end(0)
        num_to_split = int(m.group(0))
        split_left = int(math.floor(num_to_split/2))
        split_right = int(math.ceil(num_to_split/2))
        result = num[:first_index] + f"[{split_left},{split_right}]" + num[last_index:]
        assert cls.is_balanced(result)
        return result, True

    @classmethod
    def reduce(cls, num):
        while 1:
            num, was_exploded = cls.explode(num)
            if was_exploded:
                # print("Reduced to", num)
                continue
            num, was_split = cls.split(num)
            if was_split:
                # print("Split to", num)
                continue
            if not was_exploded and not was_split:
                break
        assert cls.is_balanced(num)
        return num

    @classmethod
    def add_number_list(cls, number_list):
        assert len(number_list) >= 2

        result = number_list[0]
        for addend in number_list[1:]:
            result = cls.add(result, addend)
            result = cls.reduce(result)
            # print(result)
        
        assert cls.is_balanced(result)
        return result

    @classmethod
    def parse_number_string_to_list(cls, number_string):
        number_list = number_string.strip().split("\n")
        number_list = [ n.strip() for n in number_list ]
        return number_list


def find_largest_magnitude(numbers):
    max_sum_value = None
    max_magnitude = 0
    for n1 in numbers:
        for n2 in numbers:
            if n1 is n2:
                continue
            left = n1.copy()
            right = n2.copy()
            sum_value = SnailOperations.add(left, right)
            sum_value.reduce()
            magnitude = sum_value.magnitude()
            if magnitude > max_magnitude:
                max_magnitude = magnitude
                max_sum_value = sum_value

    print("Max sum", max_sum_value)
    print("Max magnitude: ", max_magnitude)

    return max_magnitude, max_sum_value


if __name__ == "__main__":

    with open('day18.txt') as infile:
        data = infile.read()

    numbers = SnailOperations.parse_number_list(data)
    sum_value = SnailOperations.add_number_list(numbers)
    print(sum_value)
    print("magnitude", sum_value.magnitude())

    # Part 1
    # [[[[7,7],[7,7]],[[7,7],[7,0]]],[[[7,7],[8,8]],[[8,8],[9,8]]]]
    # magnitude 4391

    numbers = SnailOperations.parse_number_list(data)
    find_largest_magnitude(numbers)
    
    # part 2
    # Max sum [[[[6,8],[9,7]],[[8,9],[5,6]]],[[[9,9],[5,9]],[[9,0],[9,9]]]]
    # Max magnitude:  4626 