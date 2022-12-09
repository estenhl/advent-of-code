from __future__ import annotations

import argparse


class File():
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

class Directory():
    @property
    def size(self) -> int:
        return sum([self.children[child].size for child in self.children])

    def __init__(self, name: str, parent: Directory = None):
        self.name = name
        self.parent = parent
        self.children = {}

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    root = Directory('/')
    current = root
    folders = []
    i = 0

    while i < len(lines):
        tokens = lines[i].split(' ')

        if tokens[0] != '$':
            raise ValueError(f'Encountered non-command line {lines[i]}')

        if tokens[1] == 'cd':
            if tokens[2] == '/':
                current = root
            elif tokens[2] == '..':
                current = current.parent
            else:
                current = current.children[tokens[2]]
        elif tokens[1] == 'ls':
            i += 1
            while i < len(lines) and not lines[i].startswith('$'):
                tokens = lines[i].split(' ')

                child = File(tokens[1], int(tokens[0])) if tokens[0] != 'dir' \
                        else Directory(tokens[1], parent=current)

                if isinstance(child, Directory):
                    folders.append(child)

                current.children[child.name] = child

                i += 1
            i -= 1
        else:
            raise ValueError(f'Encountered unknown command {line}')

        i += 1

    sizes = [f.size for f in folders]
    small = [s for s in sizes if s < 100000]
    print(f'Total sizes of small folders: {sum(small)}')

    target = sorted([s for s in sizes if s > root.size - 40000000])[0]
    print(f'To delete: {target}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 7')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
