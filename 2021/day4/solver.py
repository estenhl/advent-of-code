import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x for x in f.readlines()]

    draws = [int(x) for x in lines[0].split(',')]

    parse_board = lambda lines: np.asarray([[int(x) for x in line.split(' ') \
                                             if len(x) > 0] \
                                            for line in lines])
    boards = np.asarray([parse_board(lines[i:i+5]) \
                        for i in range(2, len(lines), 6)])
    print(draws)
    rounds = [np.where(boards == draw) for draw in draws]

    print(rounds[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 4 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
