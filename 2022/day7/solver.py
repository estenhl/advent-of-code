from __future__ import annotations

import argparse

from typing import Union


class File():
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Folder():
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add_content(self, child: Union[Folder, File]):
        self.children.append(child)

    def change_directory(self, path: str):
        if self.name == '/' and path == '/':
            return self

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    root = Folder('/')
    current = root

    for i in range(len(lines)):
        tokens = lines[i].split(' ')
        print(tokens)

        if tokens[0] == '$':
            if tokens[1] == 'cd':
                current.change_directory(tokens[2])
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 3')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
