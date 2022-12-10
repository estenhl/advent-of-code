import argparse
import matplotlib.pyplot as plt
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    increments = [[0] if line == 'noop' else [0, int(line.split(' ')[1])] \
                  for line in lines]
    increments = reduce(lambda x, y: x + y, [[0]] + increments[:-1])
    values = np.cumsum(increments) + 1
    idx = np.arange(19, len(values), 40)
    signal_strengths = (idx + 1) * values[idx]

    print(f'Signal strengths: {np.sum(signal_strengths)}')

    pixels = np.arange(len(values)) % 40
    screen = (np.abs(pixels - values) <= 1).astype(int)
    screen = np.vstack(np.array_split(screen, len(screen) // 40))

    plt.imshow(screen)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 10')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
