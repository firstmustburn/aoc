
import sys

with open('day1.input') as infile:
    inputs = [ int(l.strip()) for l in infile.readlines()]

# for i in range(len(inputs)-1):
#     for j in range(i+1, len(inputs)):
#         if inputs[i] + inputs[j] == 2020:
#             print(inputs[i], inputs[j], inputs[i]+inputs[j], inputs[i]*inputs[j])

for i in range(len(inputs)-2):
    for j in range(i+1, len(inputs)-1):
        for k in range(j+1, len(inputs)):
            a = inputs[i]
            b = inputs[j]
            c = inputs[k]
            if a + b + c == 2020:
                print(a,b,c,a+b+c, a*b*c)
                sys.exit()
 