import argparse
import numpy as np

from copy import copy
from typing import List


def mix(numbers: List[int], order: List[int]):
    order = copy(order)

    for i in range(len(order)):
        idx = order.index(i)
        value = numbers.pop(idx)
        destination = (value + idx) % len(numbers)
        numbers.insert(destination, value)
        value = order.pop(idx)
        order.insert(destination, value)

    return numbers, order

def solve(input: str):
    with open(input, 'r') as f:
        numbers = [int(x.strip()) for x in f.readlines()]

    order = np.arange(len(numbers)).tolist()

    single, _ = mix(copy(numbers), copy(order))
    coords = [single[(single.index(0) + (1000 * i)) % len(single)] \
             for i in range(1, 4)]
    print(f'Sum: {np.sum(coords)}')

    numbers = [811589153 * num for num in numbers]

    for _ in range(10):
        numbers, order = mix(numbers, order)

    coords = [numbers[(numbers.index(0) + (1000 * i)) % len(numbers)] \
              for i in range(1, 4)]
    print(f'Sum: {np.sum(coords)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 20')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


