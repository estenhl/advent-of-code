import argparse
import re
import numpy as np

from typing import List, Tuple


def solve(input: str):
    with open(input, 'r') as f:
        characters = np.asarray([int(x) for x in f.read().strip().split(',')])

    bins = {i: len(np.where(characters == i)[0]) for i in range(7)}
    waiting = {0: 0, 1: 0}

    for day in range(1, 257):
        spawns = bins[0]
        for i in range(6):
            bins[i] = bins[i + 1]
        bins[6] = spawns
        bins[6] += waiting[0]
        waiting[0] = waiting[1]
        waiting[1] = spawns

        if day == 80:
            total = np.sum(list(bins.values())) + np.sum(list(waiting.values()))
            print(f'Day 80: {total}')

    total = np.sum(list(bins.values())) + np.sum(list(waiting.values()))
    print(f'Day 256: {total}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 6 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
