import sys
from collections import defaultdict

class Digits:

    def __init__(self, test_digits, actual_digits):
        self.test_digits = test_digits
        self.actual_digits = actual_digits

    def decode(self):

        digit_map = {} #map of digit (integer) to digit string
        #do the unambiguous ones first
        unmapped_digits = defaultdict(list) #length -> list of digits
        for digit in self.test_digits:
            if len(digit) == 2:
                # 1 - 2 segments
                digit_map[1] = digit
            elif len(digit) == 3:
                # 7 - 3 segments
                digit_map[7] = digit
            elif len(digit) == 4:
                # 4 - 4 segments
                digit_map[4] = digit
            elif len(digit) == 7:
                # 8 - 7 segments
                digit_map[8] = digit
            else:
                unmapped_digits[len(digit)].append(digit)
        assert len(digit_map) == 4

        #three is the length 5 digit with the same segments as 1
        threes = [ d for d in unmapped_digits[5] if digit_map[1].issubset(d) ]
        assert len(threes) == 1
        digit_map[3] = threes[0]
        unmapped_digits[5].remove(threes[0])

        #0 is the length 6 digit that does not have the same segments as 4-7
        m74 = digit_map[4].difference(digit_map[7])
        zeros = [ d for d in unmapped_digits[6] if not m74.issubset(d) ] 
        assert len(zeros) == 1
        digit_map[0] = zeros[0]
        unmapped_digits[6].remove(zeros[0])

        #top left segment is the one that m74 and 0 share
        top_left = m74.intersection(digit_map[0])

        #two is the only remaining 5 segment with out a top left
        twos = [ d for d in unmapped_digits[5] if not top_left.issubset(d) ]
        assert len(twos) == 1
        digit_map[2] = twos[0]
        unmapped_digits[5].remove(twos[0])

        #five is the only remaining 5 segment digit
        assert len(unmapped_digits[5]) == 1
        digit_map[5] = unmapped_digits[5][0]
        unmapped_digits[5] = []

        #9 is the 6 segment digit that has 2 segments remaining when four is subracted
        nines = [ d for d in unmapped_digits[6] if len(d.difference(digit_map[4])) == 2 ]
        assert len(nines) == 1
        digit_map[9] = nines[0]
        unmapped_digits[6].remove(nines[0])
        
        #siz is the only remaining 6 segment digit
        assert len(unmapped_digits[6]) == 1
        digit_map[6] = unmapped_digits[6][0]
        unmapped_digits[6] = []

        #make sure we got all the digits
        for k,v in unmapped_digits.items():
            assert len(v) == 0
    
        for i in range(10):
            assert i in digit_map

        self.digit_map = digit_map
        self.reverse_map = { "".join(sorted(v)):k for k,v in digit_map.items() } 

        self.actual_value = 0
        for digit in self.actual_digits:
            self.actual_value  = self.actual_value*10 + self.reverse_map["".join(sorted(digit))]

        self.actual_value = int(self.actual_value)

    def dump(self):
        print("Digit Map:", self.digit_map)
        print("Actual digits", self.actual_digits)
        print("Actual value:", self.actual_value)




def load_digit_list(filename):

    with open(filename) as infile:
        lines = infile.readlines()

    digitlist = []
    for line in lines:
        parts = line.split("|")
        assert len(parts) == 2
        test_digits = [ set(d) for d in parts[0].strip().split() ]
        assert len(test_digits) == 10
        actual_digits = [ set(d) for d in parts[1].strip().split() ]
        assert len(actual_digits) == 4
        digitlist.append(Digits(test_digits, actual_digits))
    return digitlist

def count_unambiguous(dlist):

    #unambiguous lengths are:
    # 7 - 3 segments
    # 1 - 2 segments
    # 8 - 7 segments
    # 4 - 4 segments
    umambig_lengths = [2,3,4,7]
    unambig_count = 0
    for digits in dlist:
        # print("*****************")
        for digit in digits.actual_digits:
            # print(digit)
            if len(digit) in umambig_lengths:
                unambig_count += 1

    print("Number of unambig digits:", unambig_count)

# dlist = load_digit_list("day8_test.txt")
dlist = load_digit_list("day8.txt")

count_unambiguous(dlist)  
# Number of unambig digits: 303

digit_sum = 0
for ds in dlist:
    ds.decode()
    ds.dump()
    digit_sum += ds.actual_value

print("Sum of of actual values:", digit_sum) 


#Sum of of actual values: 961734
