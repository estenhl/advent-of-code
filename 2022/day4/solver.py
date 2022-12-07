import argparse
import numpy as np

from functools import reduce

def to_range(token: str):
    start, end = token.split('-')
    return set(np.arange(int(start), int(end) + 1))

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines() \
                 if len(x.strip()) > 0]

    ranges = [[to_range(x) for x in line.split(',')] for line in lines]
    contains = [r[0] & r[1] == r[0] or r[0] & r[1] == r[1] for r in ranges]
    print(f'Contains: {np.sum(contains)}')

    overlaps = [len(r[0] & r[1]) > 0 for r in ranges]
    print(f'Overlaps: {np.sum(overlaps)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 4')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
