import argparse
import numpy as np


def solve(input: str):
    with open(input, 'r') as f:
        data = [int(x) for x in f.readlines()]

    increases = [data[i-1] < data[i] for i in range(1, len(data))]
    print(f'Increases: {len(np.where(increases)[0])}')

    windows = [np.sum(data[i-2:i+1]) for i in range(2, len(data))]
    increasing_windows = [windows[i-1] < windows[i] \
                          for i in range(1, len(windows))]
    print(f'Increasing windows: {len(np.where(increasing_windows)[0])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 1 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
