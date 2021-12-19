import sys

with open('day3.input') as infile:
    forest = infile.readlines()

row = 0
col = 0


# entries = entries[:5]

def count_letter(password, letter):
    count = 0
    for c in password:
        if c == letter:
            count += 1
    return count

# valid_count = 0
# for entry in entries:
#     letter_count = count_letter(entry.password, entry.letter)
#     is_valid = letter_count >= entry.min and letter_count <= entry.max
#     print(entry, is_valid)
#     if is_valid:
#         valid_count += 1

# print("Valid count", valid_count)

def letter_at_pos(password, letter, pos):
    return password[pos-1] == letter

valid_count = 0
for entry in entries:
    c1 = letter_at_pos(entry.password, entry.letter, entry.min)
    c2 = letter_at_pos(entry.password, entry.letter, entry.max)

    is_valid = (c1 and not c2) or (c2 and not c1)

    print(entry, is_valid)
    if is_valid:
        valid_count += 1

print("Valid count", valid_count)