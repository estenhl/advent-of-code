import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        characters = f.read()

    for name, count in [('packet', 4), ('message', 14)]:
        counts = [len(set(characters[i-count:i])) \
                  for i in range(count, len(characters))]
        print(f'First {name}: {counts.index(count) + count}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 6')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
