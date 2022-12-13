import argparse
import numpy as np

from functools import cmp_to_key, reduce
from typing import List


def compare(left: List[int], right: List[int]):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    else:
        for i in range(len(left)):
            if i >= len(right):
                return 1

            comparison = compare(left[i], right[i])

            if comparison != 0:
                return comparison

        return len(left) - len(right)

def solve(input: str):
    with open(input, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    pairs = [(eval(lines[i]), eval(lines[i+1])) \
             for i in range(0, len(lines), 3)]
    comparisons = np.asarray([compare(*pair) for pair in pairs])
    total = np.sum(np.where(comparisons < 0)[0] + 1)

    print(f'Sum of correct pairs: {total}')

    dividers = [([[2]], [[6]])]

    packets = reduce(lambda x, y: x + y, pairs + dividers)
    packets = sorted(packets, key=cmp_to_key(compare))
    idx = np.asarray([packets.index(divider) for divider in dividers[0]]) + 1

    print(f'Decoder key: {np.prod(idx)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 13')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
