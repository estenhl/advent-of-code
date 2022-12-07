import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines() \
                 if len(x.strip()) > 0]

    contains = 0
    overlaps = 0

    for line in lines:
        pairs = line.split(',')
        pairs = [[int(x) for x in p.split('-')] for p in pairs]

        if pairs[0][0] <= pairs[1][0] and pairs[0][1] >= pairs[1][1] or \
           pairs[0][0] >= pairs[1][0] and pairs[0][1] <= pairs[1][1]:
            contains += 1

        ranges = [set(np.arange(p[0], p[1] + 1)) for p in pairs]

        if len(ranges[0] & ranges[1]) > 0:
            overlaps += 1

    print(f'Contains: {contains}')
    print(f'Overlaps: {overlaps}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 3')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
