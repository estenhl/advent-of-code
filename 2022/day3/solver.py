import argparse
import numpy as np

from functools import reduce


def score(x):
    lower = x.lower()
    score = ord(lower) - 96
    if x != lower:
        score += 26

    return score

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    scores = [score((set(line[len(line) // 2:]) & \
                     set(line[:len(line) // 2])).pop()) \
             for line in lines]
    print(f'Sum: {np.sum(scores)}')

    priorities = [reduce(lambda x, y: set(x) & set(y), lines[i:i+3]) \
                  for i in range(0, len(lines), 3)]
    print(f'Sum: {sum([score(item.pop()) for item in priorities])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 3')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
