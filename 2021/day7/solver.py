import argparse
import re
import numpy as np

from typing import List, Tuple


def solve(input: str):
    with open(input, 'r') as f:
        values = np.asarray([int(x) for x in f.read().strip().split(',')])


    costs = [np.sum(np.abs(values - i)) for i in range(np.amax(values) + 1)]
    print(f'Horizontal cost: {np.amin(costs)}')
    costs = [np.sum([np.sum(np.arange(np.abs(v - i) + 1)) for v in values]) \
             for i in range(np.amax(values) + 1)]
    print(f'Cost: {np.amin(costs)}')
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 7 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
