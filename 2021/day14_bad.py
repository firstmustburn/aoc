from collections import defaultdict, Counter
from pprint import pprint
import re
import math

class Rule:
    RULE_REGEX=re.compile("([A-Z])([A-Z]) -> ([A-Z])") 

    def __init__(self, rulestr):
        match = self.RULE_REGEX.match(rulestr)
        assert match is not None
        self.left, self.right, self.insert = match.groups()

    def __str__(self):
        return f"{self.left}{self.right} -> {self.insert}"

class BaseRuleSet:

    def __init__(self, rule_string_list):
        self.rules = [ Rule(s) for s in rule_string_list ]


class NaiveRuleSet(BaseRuleSet):

    def __init__(self, rule_string_list):
        super().__init__(rule_string_list)
        #make a map of left value -> (map of right value -> rule object )
        self.rule_map = defaultdict(dict)
        for rule in self.rules:
            self.rule_map[rule.left][rule.right] = rule

    def polymerize(self, input):
        """Apply polymerization rules to input string"""
        output = input[0] #take the first value as the first "left"
        # in this loop, find the insertion rule and add the inserted character and the "right"
        # all the way through the input list
        for left, right in zip(input[:-1], input[1:]):
            rule = self.rule_map[left][right]
            # print(f"for {left}, {right}: rule {rule}")
            output += rule.insert + right
        # print(f"polymer {input} --> {output}")
        assert len(output) == (len(input) * 2) - 1
        return output

class PowerRuleSet(BaseRuleSet):

    def __init__(self, rule_string_list):
        super().__init__(rule_string_list)
        # map of input length -> (map of input string to output string) 
        self.rule_map = defaultdict(dict) 
        for rule in self.rules:
            input = rule.left+rule.right
            self.rule_map[2][hash(input)] = rule.left+rule.insert+rule.right

    @classmethod
    def _chunk(cls, input):
        """chunk the string up into power-of-two sizes with overlapping first and last parts, so
        that we can just stitch the resulting parts together again.

        Call recursively until we consume the whole string into chunks
        """
        # print("Chunking", input)
        if len(input) == 2:
            #halting condition for recursion
            return [input]
        #else break it up

        #compute the chunk size -- limit it to avoid running out of memeory
        largest_pwr = math.floor(math.log(len(input),2))
        if largest_pwr > 20:
            largest_pwr = 20
        chunk_size = int(math.pow(2, largest_pwr))
        if chunk_size == len(input):
            chunk_size = int(chunk_size/2)
        # print("chunk_size", chunk_size)

        #make as many chunks of chunk_size as we can and recurse the remainder
        chunks = []
        remainder=input
        while len(remainder) > chunk_size:
            chunks.append(remainder[:chunk_size])
            remainder = remainder[chunk_size-1:] #-1 means the remainder overlaps the chunk
        # print(chunks,  remainder)
        return chunks+cls._chunk(remainder)

    def polymerize(self, input, depth=0):
        # print(f"depth: {depth} input len:{len(input)}")
        #see if we already know the answer
        try:
            output = self.rule_map[len(input)][hash(input)]
            # print(f"{depth*' '}{input} -> {output}")
            return output
        except KeyError:
            pass

        chunks = self._chunk(input)
        # print(' '*depth, [ len(c) for c in chunks ] )

        output_chunks = [ self.polymerize(c, depth+1) for c in chunks ]

        #stitch the output chunks back together
        output = output_chunks[0] #take the whole first chunk
        #strip the leading character off the remaining chunks
        for chunk in output_chunks[1:]:
            output += chunk[1:]
        
        assert len(output) == (len(input) * 2) - 1
        # print(f"{depth*' '}{input} -> {output}")

        #save this result if it is an even number
        if len(input) % 2 == 0:
            self.rule_map[len(input)][hash(input)] = output
        #rule map size
        if depth == 0:
            print("RM size")
            total_size= 0 
            for rml, rm_inner in self.rule_map.items():
                rm_size = 0 
                for rmi, rmo in rm_inner.items():
                    rm_size += 8+len(rmo)
                total_size += rm_size
                print("  ", rml, rm_size/1000000)
            print("  Total size:", total_size/1000000)
            print("len(output)", len(output))
        # print([ f"{k}: {len(v)}" for k,v in self.rule_map.items() ])

        return output


def load(filename, ruleclass):
    """Return an initial polymer and a ruleset from the input file"""
    with open(filename) as infile:
        lines = infile.readlines()
    
    polymer = lines[0].strip()
    ruleset = ruleclass([ l.strip() for l in lines[2:]])

    return polymer, ruleset

def count_letters(polymer):
    count = Counter()
    for c in polymer:
        count[c] += 1
    count = [ (k,v) for k,v in count.items() ]
    count.sort(key= lambda n: n[1])

    return count





def compute_polymerization_difference(filename, iterations):

    polymer, ruleset = load(filename, PowerRuleSet)

    print(f"0: {polymer}")
    for i in range(iterations):
        polymer = ruleset.polymerize(polymer)
        print(f"{i+1}: length={len(polymer)}")
        # print(f"{i+1}: {polymer}")

    counts = count_letters(polymer)
    print("Counts:", counts)
    difference = counts[-1][1] - counts[0][1]
    print("Most freq - least freq:", difference)
    return difference

if __name__ == "__main__":
    assert compute_polymerization_difference("day14_test.txt", 10) == 1588
    assert compute_polymerization_difference("day14.txt", 10) == 3587
    # part 1
    # Counts: [('H', 564), ('N', 575), ('P', 1341), ('F', 1492), ('C', 1553), ('S', 2162), ('V', 2392), ('O', 2584), ('B', 2643), ('K', 4151)]
    # Most freq - least freq: 3587


