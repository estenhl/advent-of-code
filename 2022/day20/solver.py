import argparse
import re
import numpy as np

from copy import deepcopy
from typing import Any, Dict
from tqdm import tqdm


def solve(input: str):
    with open(input, 'r') as f:
        numbers = [int(x.strip()) for x in f.readlines()]

    print(numbers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 20')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


