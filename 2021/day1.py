
import sys

with open('day1.txt') as infile:
    inputs = [ int(l.strip()) for l in infile.readlines()]


# inputs = inputs[:10]
# print(inputs)

inputs = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

#count number of increases
def count_increases(data):
    increase_count = 0
    decrease_count = 0
    print(data[0])
    for v1,v2 in zip(data[:-1],data[1:]):
        if v1 < v2:
            print(v2, "increase")
            increase_count += 1
        if v1 > v2:
            print(v2, "decrease")
            decrease_count += 1

    print("increases: ", increase_count)
    print("decreases: ", decrease_count)

def sliding_window(data, size):
    data_out = []
    for i in range(len(data)):
        window = data[i:i+size]
        if len(window) == size:
            data_out.append(sum(window))
    return data_out

#part 1
# count_increases(inputs)

#part 2
count_increases(sliding_window(inputs, 3))
