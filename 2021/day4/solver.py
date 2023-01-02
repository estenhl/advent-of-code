import argparse
import numpy as np


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x for x in f.readlines()]

    draws = [int(x) for x in lines[0].split(',')]

    parse_board = lambda lines: np.asarray([[int(x) for x in line.split(' ') \
                                             if len(x) > 0] \
                                            for line in lines])
    boards = np.asarray([parse_board(lines[i:i+5]) \
                        for i in range(2, len(lines), 6)])
    rounds = np.asarray([boards == draw for draw in draws])

    for i in range(1, len(rounds)):
        rounds[i] = np.logical_or(rounds[i - 1], rounds[i])

    results = [[p[0] for p in np.where(np.all(rounds, axis=axis))[:2]] \
               for axis in [2, 3]]
    idx, board = sorted(results, key=lambda x: x[0])[0]

    unmarked = np.sum(boards[board][np.where(~rounds[idx][board])])
    print(f'Best score: {unmarked * draws[idx]}')

    finished = [np.amin(
                    np.where(
                        np.logical_or(
                            np.any(np.all(rounds, axis=3), axis=-1),
                            np.any(np.all(rounds, axis=2), axis=-1))[:,i])[0]) \
                for i in range(len(boards))]
    board = np.argmax(finished)
    idx = finished[board]

    unmarked = np.sum(boards[board][np.where(~rounds[idx][board])])
    print(f'Worst score: {unmarked * draws[idx]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 4 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
