def load_line_sep_groups(filename, linefunc):

    groups = []
    group = []
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            if line:
                group.append(linefunc(line))
            else:
                groups.append(group)
                group = []
        #add the last group
        groups.append(group)
    return groups

def load_token_list(filename):
    token_list = []

    with open(filename) as infile:
        for line in infile:
            token_list.append(line.strip().split())

    return token_list