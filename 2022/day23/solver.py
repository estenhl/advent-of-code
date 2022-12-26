from __future__ import annotations

import argparse
import numpy as np

from functools import reduce
from typing import List, Tuple


DIRECTIONS = [
    ('N', np.asarray([-1, 0]), np.asarray([[-1, -1], [-1, 0], [-1, 1]])),
    ('S', np.asarray([1, 0]), np.asarray([[1, -1], [1, 0], [1, 1]])),
    ('W', np.asarray([0, -1]), np.asarray([[-1, -1], [0, -1], [1, -1]])),
    ('E', np.asarray([0, 1]), np.asarray([[-1, 1], [0, 1], [1, 1]]))
]

def build(elves: List[Elf]):
    positions = np.asarray([elf.position for elf in elves])
    ys = positions[:,0]
    xs = positions[:,1]

    ymin = np.amin(ys)
    ymax = np.amax(ys)
    xmin = np.amin(xs)
    xmax = np.amax(xs)

    height = ymax - ymin
    width = xmax - xmin

    map = np.zeros((height + 1, width + 1), dtype=object)
    map[:] = '.'

    for elf in elves:
        y, x = elf.position
        map[y - ymin, x - xmin] = '#'

    return map

def count(elves: List[Elf]):
    map = build(elves)

    return len(np.where(map == '.')[0])

def render(elves: List[Elf]):
    map = build(elves)

    for line in map:
        print(''.join(line.astype(str)))

    print()

class Elf:
    def __init__(self, name: str, y: int, x: int):
        self.name = name
        self.position = (y, x)
        self.idx = 0
        self.target = None

    def update(self, taken: List[Tuple[int]]):
        neighbours = [[(i, j) for j in [-1, 0, 1] \
                      if not (i == 0 and j == 0)] for i in [-1, 0, 1]]
        neighbours = reduce(lambda x, y: x + y, neighbours)
        neighbours = [tuple(self.position + np.asarray(neighbour)) \
                      for neighbour in neighbours]

        if len(set(neighbours) & taken) == 0:
            self.target = None
            return

        for i in range(4):
            direction, move, tiles = DIRECTIONS[(self.idx + i) % len(DIRECTIONS)]
            overlap = taken & set([tuple(np.asarray(self.position) + tile) \
                                  for tile in tiles])

            if len(overlap) == 0:
                self.target = tuple(np.asarray(self.position) + move)
                break



    def move(self):
        self.idx = (self.idx + 1) % len(DIRECTIONS)
        if self.target is not None:
            self.position = self.target

        self.target = None

def solve(input: str):
    with open(input, 'r') as f:
        map = np.asarray([[c for c in x.strip()] \
                         for x in f.readlines() if len(x) > 0])

    idx = np.where(map == '#')
    elves = [Elf(f'Elf {i}', idx[0][i], idx[1][i]) for i in range(len(idx[0]))]
    round = 0

    while True:
        taken = set([elf.position for elf in elves])

        for elf in elves:
            elf.update(taken)

        updates = {}
        for i in range(len(elves)):
            elf = elves[i]
            if not elf.target in updates:
                updates[elf.target] = []

            updates[elf.target].append(i)

        if len(updates.keys()) == 1:
            print(f'Final round: {round + 1}')
            break

        for key, values in updates.items():
            if len(values) > 1:
                for value in values:
                    elves[value].target = None

        for elf in elves:
            elf.move()

        if round == 9:
            print(f'Count at round 10: {count(elves)}')

        round += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 23')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


