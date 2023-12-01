
from pprint import pprint
from collections import namedtuple

File = namedtuple('File', ['name','size'])

class Directory:

    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.files = {}
        self.dirs = {}

    def get_parent(self):
        return self.parent

    def add_file(self, file):
        self.files[file.name] = file

    def add_dir(self, dir):
        self.dirs[dir.name] = dir

    def get_dir(self, dirname):
        return self.dirs[dirname]

    def size(self):
        return sum([ f.size for f in self.files.values() ] + [ d.size() for d in self.dirs.values() ])

    def walk(self):
        yield self
        for dir in self.dirs.values():
            yield from dir.walk()

    def dump(self, indent=0):
        print(' '*indent, '-', self.name)
        for file in self.files.values():
            print(' '*(indent+2),file.name, file.size)
        for dir in self.dirs.values():
            dir.dump(indent+2)

Command = namedtuple('Command', ['exec','arg'])
LsResult = namedtuple('LsResult', ['dirnames', 'files'])

def parse_command(line):
    tokens = line.split()
    assert len(tokens) <= 3
    assert tokens[0] == '$'
    
    exec = tokens[1]
    if len(tokens) == 3:
        arg = tokens[2]
    else:
        arg = None

    return Command(exec, arg)

def parse_ls_result(lines):
    dirnames = []
    files = []
    for line in lines:
        size, name = line.split()
        if size == 'dir':
            dirnames.append(name)
        else:
            files.append(File(name, int(size)))
    return LsResult(dirnames, files)

def load_input(filename):
    sequence = []

    ls_lines = []
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            if line.startswith('$'):
                #see if there are any ls_lines to capture
                if ls_lines:
                    sequence.append(parse_ls_result(ls_lines))
                    ls_lines = []
                #process the command
                command = parse_command(line)
                sequence.append(command)
            else:
                ls_lines.append(line)
        #see if there are any ls_lines to capture
        if ls_lines:
            sequence.append(parse_ls_result(ls_lines))
            ls_lines = []
    return sequence

def build_tree(sequence):
    #set up the initial directory
    root = Directory('/', None)
    command = sequence.pop(0)
    assert command.exec == 'cd'
    assert command.arg == '/'
    print("Processing",command)
    #current directory lets us keep track of where we are as we process commands
    current_directory = root
    while len(sequence) > 0:
        command = sequence.pop(0)
        print("Processing",command)
        #switch on command
        if command.exec == 'cd':
            #swich cd on arg
            if command.arg == '/':
                current_directory = root
            elif command.arg == '..':
                current_directory = current_directory.get_parent()
            else:
                current_directory = current_directory.get_dir(command.arg)
        elif command.exec == 'ls':
            #pop the next item in the sequence as the ls result:
            ls_data = sequence.pop(0)
            print("ls_data", ls_data)
            assert isinstance(ls_data, LsResult)
            if current_directory.files or current_directory.dirs:
                raise RuntimeError("ls for directory that already has files or dirs")
            for dirname in ls_data.dirnames:
                current_directory.add_dir(Directory(dirname, current_directory))
            for file in ls_data.files:
                current_directory.add_file(file)
        else:
            raise RuntimeError(f"Unknown command {command}")
    return root


def part1(filesystem):
    size_limit = 100000
    size_total = 0
    for dir in filesystem.walk():
        size = dir.size()
        # print(dir.name, size)
        if size <= size_limit:
            size_total += size
    return size_total

def part2(stream):
    disk_size = 70000000
    disk_needed = 30000000
    unused_space = disk_size - filesystem.size()
    target_dir_size = disk_needed - unused_space

    smallest_dir_size = disk_size
    for dir in filesystem.walk():
        size = dir.size()
        if size >= target_dir_size:
            #this is a candidate for deletion
            if size < smallest_dir_size:
                smallest_dir_size = size
        #else do nothing
    return smallest_dir_size

if __name__ == '__main__':

    # filename='day7/test.txt'
    filename='day7/input.txt'

    seq = load_input(filename)

    filesystem = build_tree(seq)
    filesystem.dump()

    print('part 1', part1(filesystem))

    print('part 2', part2(filesystem))

