
from pprint import pprint
from collections import namedtuple

class Tree:
    def __init__(self, height):
        self.height = height
        self.visible = False
        self.scenic_score = 0

    def __str__(self):
        visible = 'v' if self.visible else 'n'
        return f"{self.height}{visible}{self.scenic_score}"

    def __repr__(self):
        return self.__str__()

def dump(tree_rows):
    for row in tree_rows:
        print(' '.join([ str(t) for t in row ]))
    print('')

def reverse_trees(tree_rows):
    for row in tree_rows:
        row.reverse()

def transpose_trees(tree_rows):
    tree_size = len(tree_rows)
    for i in range(tree_size):
        for j in range(i,tree_size):
            temp = tree_rows[i][j]
            tree_rows[i][j] = tree_rows[j][i]
            tree_rows[j][i] = temp

def load_input(filename):
    with open(filename) as infile:
        trees=[]
        for line in infile:
            tree_row=[]
            for c in line.strip():
                tree_row.append(Tree(int(c)))
            trees.append(tree_row)
    return trees

def mark_visibility(tree_rows):
    #iterate over the inner rows
    for row in tree_rows[1:-1]:
        outer_height = row[0].height
        for tree in row[1:-1]:
            if tree.height > outer_height:
                tree.visible = True
                outer_height = tree.height
            # else not visible

def mark_scenic_score(tree_rows, start_row, start_col):
    size = len(tree_rows)
    height = tree_rows[start_row][start_col].height
    #left
    left_tree_count = 0
    for i in range(start_col-1, -1, -1):
        left_tree_count += 1
        if tree_rows[start_row][i].height >= height:
            break
    #right
    right_tree_count = 0
    for i in range(start_col+1, size):
        right_tree_count += 1
        if tree_rows[start_row][i].height >= height:
            break
    #up
    up_tree_count = 0
    for j in range(start_row-1, -1, -1):
        up_tree_count += 1
        if tree_rows[j][start_col].height >= height:
            break
    #right
    down_tree_count = 0
    for j in range(start_row+1, size):
        down_tree_count += 1
        if tree_rows[j][start_col].height >= height:
            break
    print("i", start_row, "j", start_col, left_tree_count, right_tree_count, up_tree_count, down_tree_count)
    tree_rows[start_row][start_col].scenic_score = left_tree_count*right_tree_count*up_tree_count*down_tree_count

def part1(tree_rows):
    #mark borders as visible
    for tree in tree_rows[0]:
        tree.visible = True
    for tree in tree_rows[-1]:
        tree.visible = True
    for row in tree_rows:
        row[0].visible = True
        row[-1].visible = True
    #check inner trees from the left
    mark_visibility(tree_rows)
    #reverse and check from the left
    reverse_trees(tree_rows)
    mark_visibility(tree_rows)
    reverse_trees(tree_rows)
    #transpose and check from the left
    transpose_trees(tree_rows)
    mark_visibility(tree_rows)
    #reverse and check the transposed grid
    reverse_trees(tree_rows)
    mark_visibility(tree_rows)
    reverse_trees(tree_rows)
    #undo transpose
    transpose_trees(tree_rows)

    # dump(tree_rows)
    #count visible trees
    vis_count = 0
    for row in tree_rows:
        for tree in row:
            if tree.visible:
                vis_count += 1
    return vis_count

def part2(tree_rows):
    #iterate over the inner rows
    size = len(tree_rows)
    for i in range(1,size-1):
        for j in range(1,size-1):
            mark_scenic_score(tree_rows, i, j)

    dump(tree_rows)

    return max([ max([ tree.scenic_score for tree in row]) for row in tree_rows])

if __name__ == '__main__':

    # filename='day8/test.txt'
    filename='day8/input.txt'

    tree_rows = load_input(filename)
    dump(tree_rows)

    print('part 1', part1(tree_rows))

    print('part 2', part2(tree_rows))

