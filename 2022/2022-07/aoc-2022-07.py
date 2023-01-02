class File(object):

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __repr__(self):
        return self.name + '(' + str(self.size) + ')'

    def calcsize(self) -> int:
        return self.size


class Dir(File):

    def __init__(self, name: str):
        super(Dir, self).__init__(name, size=0)

        self._contents = []

    def __repr__(self):
        return self.name + str(self._contents)

    def add_file(self, name: str, size: int) -> None:
        self._contents.append(File(name, size))

    def add_dir(self, dir) -> None:
        self._contents.append(dir)

    def dirs(self) -> list:
        return filter(lambda x: isinstance(x, Dir), self._contents)

    def calcsize(self) -> int:
        self.size = sum(map(lambda f: f.calcsize(), self._contents))
        return self.size


class Terminal(object):

    def __init__(self):
        self.filesystem = Dir('/')
        self.path = [self.filesystem]
        self.cwd = self.filesystem

    def cd(self, name) -> None:
        if name == '/':
            self.cwd = self.filesystem
            self.path = [self.filesystem]
        elif name == '..':
            self.path.pop()
            self.cwd = self.path[-1]
        else:
            d = Dir(name)
            self.cwd.add_dir(d)
            self.path.append(d)
            self.cwd = d


# Get a list of all directories with size < the target limit
def get_dirs(d: Dir, size_target: int, is_limit: bool) -> list:
    dir_list = []
    if is_limit and d.size < size_target:
        dir_list.append(d)
    elif not is_limit and d.size >= size_target:
        dir_list.append(d)
    for dir in d.dirs():
        dir_list.extend(get_dirs(dir, size_target, is_limit))
    return dir_list


CD_PREFIX = '$ cd '
LS_PREFIX = '$ ls'
COMMAND_PREFIX = '$'


def build_io(infile):
    command_list = []
    with open(infile, 'r') as input:
        last_command = ''
        last_output = []
        for line in input.readlines():
            if line.startswith(COMMAND_PREFIX):
                if last_command:
                    command_list.append((last_command, last_output))
            if line.startswith(CD_PREFIX):
                last_command = ''
                last_output = []
                command_list.append((line.strip(), []))
            elif line.startswith(LS_PREFIX):
                last_command = line.strip()
                last_output = []
            else:
                last_output.append(line.strip())
    if last_command:
        command_list.append((last_command, last_output))
    return command_list


def parse_commands(command_list: list, term: Terminal):
    for command, output in command_list:
        if command.startswith(CD_PREFIX):
            term.cd(command[5:])
        if command.startswith(LS_PREFIX):
            for o in output:
                tokens = o.split(' ')
                # skip dirs, just add them when we run cd at some point
                if not tokens[0].startswith('d'):
                    term.cwd.add_file(tokens[1], int(tokens[0]))


def main():
    #infile = 'input-test.txt'
    infile = 'input.txt'
    max_size = 70000000
    space_target = 30000000
    size_limit = 100000
    term = Terminal()

    # parse input
    io = build_io(infile)
    parse_commands(io, term)
    term.filesystem.calcsize()
    # get all dirs of size < 100000
    dir_list = get_dirs(term.filesystem, size_limit, is_limit=True)
    total_size = sum(map(lambda f: f.size, dir_list))
    print('total size: ' + str(total_size))

    # part B, get smallest file that meets the target
    extra_space_target = space_target - max_size + term.filesystem.size
    dir_list = get_dirs(term.filesystem, extra_space_target, is_limit=False)
    print('min dir: ' + str(min(map(lambda f: f.size, dir_list))))


main()
