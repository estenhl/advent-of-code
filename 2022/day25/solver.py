import argparse
import numpy as np

from typing import Tuple


MAPPING = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
REVERSE_MAPPING = {value: key for key, value in MAPPING.items()}

def _add_one(digits: Tuple[int]):
    if len(digits) == 0:
        print('New digit')
        return (1,)
    elif digits[-1] == 2:
        return _add_one(digits[:-1]) + (-2,)

    print(f'Added: {digits[:-1] + (digits[-1] + 1,)}')

    return digits[:-1] + (digits[-1] + 1,)


def _to_snafu(previous: Tuple[int], rest: int, root: int):
    print(f'Previous: {previous}, rest: {rest}, root: {root}')
    if root < 0:
        return previous

    digit = rest // (5 ** root)

    if digit <= 2:
        return _to_snafu(previous + (digit,), rest % (5 ** root), root - 1)

    print(f'Shifting')
    digit = digit - 5
    previous = _add_one(previous)

    return _to_snafu(previous + (digit,), rest % (5 ** root), root - 1)

def to_snafu(num: int):
    first_root = 0

    while(num > 5 ** first_root):
        first_root += 1

    first_root = first_root - 1

    digits = _to_snafu((), num, first_root)

    return ''.join([REVERSE_MAPPING[x] for x in digits])

def solve(input: str):
    with open(input, 'r') as f:
        lines = np.asarray([x.strip() for x in f.readlines()])


    lines = [[MAPPING[c] for c in line] for line in lines]
    numbers = [np.sum(digits * (5 ** np.arange(len(digits) - 1, -1, -1))) \
               for digits in lines]
    print(to_snafu(np.sum(numbers)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 23')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


