import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x for x in f.readlines()]

    directions = {
        'forward': lambda x: (0, int(x)),
        'up': lambda x: (-int(x), 0),
        'down': lambda x: (int(x), 0)
    }

    moves = [directions[line.split(' ')[0]](line.split(' ')[1]) \
             for line in lines]
    position = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), moves)

    print(f'Position: {position}')

    factors = {
        'down': 1,
        'up': -1,
        'forward': 0
    }

    commands = [line.split(' ')[0] for line in lines]
    units = [int(line.split(' ')[1]) for line in lines]
    aims = np.cumsum([units[i] * factors[commands[i]] \
                      for i in range(len(commands))])
    changes = [(units[i], units[i] * aims[i]) for i in range(len(commands)) \
               if commands[i] == 'forward']
    position = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), changes)

    print(f'Position: {np.prod(position)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 2 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
