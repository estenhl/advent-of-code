import argparse
import numpy as np

from scipy.spatial.distance import euclidean
from typing import List


def update(h, t):
    if euclidean(h, t) <= np.sqrt(2):
        return t

    if h[0] == t[0]:
        t = (t[0], t[1] + np.sign(h[1] - t[1]))
    elif h[1] == t[1]:
        t = (t[0] + np.sign(h[0] - t[0]), t[1])
    else:
        t = (t[0] + np.sign(h[0] - t[0]), t[1] + np.sign(h[1] - t[1]))

    return t

def simulate(lines: List[str], size: int):
    directions = {
        'R': np.asarray((0, 1)),
        'U': np.asarray((1, 0)),
        'L': np.asarray((0, -1)),
        'D': np.asarray((-1, 0))
    }

    knots = np.zeros((size, 2), dtype=int)
    visited = []

    for line in lines:
        direction, length = line.split(' ')

        for _ in range(int(length)):
            knots[0] += directions[direction]

            for i in range(1, len(knots)):
                knots[i] = update(knots[i-1], knots[i])

            visited.append(knots[-1].copy())

    visited = [f'{v[0]}-{v[1]}' for v in visited]

    return visited

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    visited = simulate(lines, 2)
    print(f'Single knot: {len(set(visited))}')

    visited = simulate(lines, 10)
    print(f'Ten knots: {len(set(visited))}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 9')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
