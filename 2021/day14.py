from collections import defaultdict, Counter
from pprint import pprint
import re
import math

class Rule:
    RULE_REGEX=re.compile("([A-Z])([A-Z]) -> ([A-Z])") 

    def __init__(self, rulestr):
        self.rulestr = rulestr
        match = self.RULE_REGEX.match(rulestr)
        assert match is not None
        self.left, self.right, self.insert = match.groups()
        self.forward_mapping = None

    def __str__(self):
        return f"{self.left}{self.right} -> {self.insert}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.rulestr == other.rulestr

    def __hash__(self):
        return hash(self.rulestr)

class BaseRuleSet:

    def __init__(self, rule_string_list):
        self.rules = [ Rule(s) for s in rule_string_list ]

class IterativeRuleSet(BaseRuleSet):

    def __init__(self, rule_string_list):
        super().__init__(rule_string_list)

        #map the rules
        self.rule_map = defaultdict(dict)
        for rule in self.rules:
            self.rule_map[rule.left][rule.right] = rule
        
        #make the forward mapping for each rule
        for rule in self.rules:
            rule.forward_mapping = [ 
                self.rule_map[rule.left][rule.insert],
                self.rule_map[rule.insert][rule.right],
            ]

    def string_to_rule_list(self, input):
        rule_list = []
        for left, right in zip(input[:-1], input[1:]):
            rule_list.append(self.rule_map[left][right])
        return rule_list

    def count_rules_at_iterations(self, rule_list, iterations):
        initial_count = Counter()
        for rule in rule_list:
            initial_count[rule] += 1

        print(f"At depth 0, count: {initial_count}")

        previous_count = initial_count
        for index in range(iterations):
            new_count = Counter()
            # each rule in the previous count makes two other rules, so
            # for each new rule in the forward mapping,
            # increment the new counter for the number of times the the previous rule appeared
            for prev_rule, num_previous in previous_count.items():
                for new_rule in prev_rule.forward_mapping:
                    new_count[new_rule] += num_previous
            print(f"At depth {index+1}, count: {new_count}")
            previous_count = new_count

        return previous_count

    def compute_difference(self, input, iterations):
        initial_rule_list = self.string_to_rule_list(input)

        rule_counter = self.count_rules_at_iterations(initial_rule_list, iterations)

        letter_counter = Counter()
        #count the left letter of the first initial rule
        letter_counter[initial_rule_list[0].left] += 1
        #count the right letter for all the other rules that would be created
        for rule, rule_count in rule_counter.items():
            letter_counter[rule.right] += rule_count
        


        sorted_count = [ (k,v) for k,v in letter_counter.items() ]
        #sort by number
        sorted_count.sort(key= lambda n: n[1])

        print("Sorted letter count: ", sorted_count)

        difference = sorted_count[-1][1] - sorted_count[0][1]
        print(f"Most: {sorted_count[-1]}")
        print(f"Least: {sorted_count[0]}")
        print(f"Difference: {difference}")
        return difference



def load(filename, ruleclass):
    """Return an initial polymer and a ruleset from the input file"""
    with open(filename) as infile:
        lines = infile.readlines()
    
    polymer = lines[0].strip()
    ruleset = ruleclass([ l.strip() for l in lines[2:]])

    return polymer, ruleset






if __name__ == "__main__":


    test_polymer, test_ruleset = load("day14_test.txt", IterativeRuleSet)
    input_polymer, input_ruleset = load("day14.txt", IterativeRuleSet)

    assert test_ruleset.compute_difference(test_polymer, 10) == 1588
    assert input_ruleset.compute_difference(input_polymer, 10) == 3587

    assert test_ruleset.compute_difference(test_polymer, 40) == 2188189693529
    input_ruleset.compute_difference(input_polymer, 40)

# part2:

# Sorted letter count:  [('N', 622049381175), ('H', 653396479204), ('P', 1395064267140), ('C', 1534441588873), ('F', 1661479204940), ('V', 2351208720414), ('S', 2457036427061), ('O', 2805606543797), ('B', 2881943855967), ('K', 4528494459174)]
# Most: ('K', 4528494459174)
# Least: ('N', 622049381175)
# Difference: 3906445077999