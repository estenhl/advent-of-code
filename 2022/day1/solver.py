import argparse
import numpy as np


def solve(input: str):
    with open(input, 'r') as f:
        data = f.read()

    sums = sorted([np.sum([int(x) for x in d.split('\n') if len(x) > 0]) \
                   for d in data.split('\n\n')])[::-1]

    print(f'Highest: {sums[0]}')
    print(f'Three highest: {np.sum(sums[:3])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 1 of AOC 2022')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
