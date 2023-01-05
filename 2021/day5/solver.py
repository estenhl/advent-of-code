import argparse
import re
import numpy as np

from typing import List, Tuple


def _parse(line: str):
    pattern = r'(\d+),(\d+) -\> (\d+),(\d+)\n'
    tokens = [int(x) for x in re.fullmatch(pattern, line).groups(0)]

    return (tokens[0], tokens[1]), \
           (tokens[2], tokens[3])

def plot(map: np.ndarray, entries: List[Tuple[Tuple[int]]],
         ignore_diagonals: bool = False):
    for start, end in entries:
        if start[0] == end[0] or start[1] == end[1]:
            ymin = min(start[0], end[0])
            ymax = max(start[0], end[0]) + 1
            xmin = min(start[1], end[1])
            xmax = max(start[1], end[1]) + 1

            idx = (np.arange(ymin, ymax), np.arange(xmin, xmax))
        else:
            if ignore_diagonals:
                continue

            ysign = np.sign(end[0] - start[0])
            xsign = np.sign(end[1] - start[1])
            idx = (np.arange(start[0], end[0] + ysign, ysign),
                   np.arange(start[1], end[1] + xsign, xsign))

        map[idx] += 1

    return map

def solve(input: str):
    with open(input, 'r') as f:
        lines = [_parse(x) for x in f.readlines()]

    ymax = np.amax([max(line[0][0], line[1][0]) for line in lines])
    xmax = np.amax([max(line[0][1], line[1][1]) for line in lines])

    map = plot(np.zeros((ymax + 1, xmax + 1)), lines, ignore_diagonals=True)
    print(f'Overlaps: {len(np.where(map > 1)[0])}')

    map = plot(np.zeros((ymax + 1, xmax + 1)), lines)
    print(f'Overlaps: {len(np.where(map > 1)[0])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 5 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
