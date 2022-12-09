from __future__ import annotations

import argparse
import numpy as np


def solve(input: str):
    with open(input, 'r') as f:
        map = np.asarray([[int(c) for c in line.strip()] \
                          for line in f.readlines()])

    height, width = map.shape
    visible = np.zeros(map.shape)
    views = np.ones(map.shape)

    for _ in range(4):
        for i in range(1, height):
            for j in range(width):
                taller = np.where(map[:i, j] >= map[i, j])[0]
                distance = i if len(taller) == 0 else i - np.amax(taller)

                if len(taller) == 0:
                    visible[i, j] = 1

                views[i, j] *= distance

        map = np.rot90(map)
        visible = np.rot90(visible)
        views = np.rot90(views)

    visible = np.sum(visible[1:-1, 1:-1])
    print(f'Visible: {2 * height + 2 * width - 4 + np.sum(visible)}')
    print(f'Max scenic score: {np.amax(views[1:-1, 1:-1])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 8')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
