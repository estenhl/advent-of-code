import argparse
import numpy as np

from copy import copy
from scipy.spatial.distance import cityblock
from typing import Tuple
from queue import PriorityQueue


DIRECTIONS = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0)
}

def render(map: np.ndarray):
    for line in map:
        print(''.join([x if len(x) == 1 else str(len(x)) for x in line]))
    print()

def update(map: np.ndarray):
    height, width = map.shape
    next = np.zeros((height, width), dtype=object)
    next[:,:] = '.'

    for i in range(height):
        for j in range(width):
            for c in map[i, j]:
                if c in DIRECTIONS:
                    direction = DIRECTIONS[c]
                    idx = ((i + direction[0]) % height, (j + direction[1]) % width)

                    next[idx] = c if next[idx] == '.' \
                            else next[idx] + c

    return next


def serialize(map: np.ndarray, position: Tuple[int]):
    return ''.join(map.flatten()) + f':{position}'

class State():
    @property
    def h(self):
        return cityblock(self.position, self.target)

    @property
    def key(self):
        return serialize(self.map, self.position)

    def __init__(self, position, minute, map, target: Tuple[int] = None,
                 history: Tuple[Tuple[int]] = ()):
        self.position = position
        self.minute = minute
        self.map = map
        self.target = target
        self.history = history

        if target is None:
            height, width = map.shape
            self.target = (height - 1, width - 1)

    def __lt__(self, other):
        return (self.minute + self.h) < (other.minute + other.h)

def search(map: np.ndarray, start: Tuple[int], end: Tuple[int]):
    height, width = map.shape
    queue = PriorityQueue()
    seen = set()

    for i in range(1, (height * width) + 1):
        map = update(map)

        if map[start] == '.':
            #print(f'Adding {i}')
            queue.put(State(start, i, map, target=end))

    while not queue.empty():
        state = queue.get()
        map = update(state.map)

        if state.key in seen:
            continue

        seen.add(state.key)

        y, x = state.position

        if y == end[0] and x == end[1]:
            return state.minute + 1, map

        for i in range(max(0, y - 1), min(height, y + 2)):
            for j in range(max(0, x - 1), min(width, x + 2)):
                if (i == y or j == x) and map[i, j] == '.':
                    queue.put(State((i, j), state.minute + 1, copy(map),
                              target=end, history=state.history + (state,)))


def solve(input: str):
    with open(input, 'r') as f:
        map = np.asarray([[c for c in x.strip()] \
                         for x in f.readlines() if len(x) > 0])

    map = map[1:-1,1:-1]
    height, width = map.shape

    minutes, map = search(map, (0, 0), (height - 1, width - 1))
    print(f'Found goal in {minutes} minutes')
    update(map)
    minutes, map = search(map, (height - 1, width - 1), (0, 0))
    print(f'Found start in {minutes} minutes')
    update(map)
    minutes, map = search(map, (0, 0), (height - 1, width - 1))
    print(f'Found goal in {minutes} minutes')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 24')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


