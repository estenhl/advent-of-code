import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        characters = f.read()

    for i in range(4, len(characters)):
        if len(set(characters[i-4:i])) == 4:
            print(f'Start of packet: {i}')
            break

    for i in range(14, len(characters)):
        if len(set(characters[i-14:i])) == 14:
            print(f'Start of message: {i}')
            return




if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 3')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
