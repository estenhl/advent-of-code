import argparse
import numpy as np

from typing import List, Tuple


def render(map: np.ndarray):
    for line in map:
        print(''.join(line))

def fill(map: np.ndarray, trace: List[Tuple[int]], offset: int):
    for i in range(1, len(trace)):
        first_x, first_y = trace[i - 1]
        second_x, second_y = trace[i]

        min_y, max_y = sorted([first_y, second_y])
        min_x, max_x = sorted([first_x - offset, second_x - offset])

        map[min_y:max_y + 1, min_x:max_x + 1] = '#'

    return map

def fall(position: Tuple[int], map: np.ndarray):
    y, x = position

    if y + 1 >= len(map):
        print(f'y outside map')
        raise ValueError()
    if map[y + 1, x] == '.':
        return fall((y + 1, x), map)
    elif x < 0:
        print(f'x < 0')
        raise ValueError()
    elif map[y + 1, x - 1] == '.':
        return fall((y + 1, x - 1), map)
    elif x + 1 >= len(map[0]):
        print(position)
        print('x > map')
        raise ValueError()
    elif map[y + 1, x + 1] == '.':
        return fall((y + 1, x + 1), map)

    return position


def solve(input: str):
    with open(input, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    points = [[[int(x) for x in point.split(',')] \
               for point in line.split(' -> ')] \
              for line in lines]
    min_x = np.amin([np.amin([p[0] for p in trace]) for trace in points])
    max_x = np.amax([np.amax([p[0] for p in trace]) for trace in points])
    max_y = np.amax([np.amax([p[1] for p in trace]) for trace in points])
    map = np.zeros((max_y + 1, (max_x - min_x) + 1), dtype=object)
    map[:,:] = '.'
    map[0,500-min_x] = '+'

    for trace in points:
        map = fill(map, trace, min_x)

    while True:
        try:
            position = fall((0, 500-min_x), map)
        except ValueError:
            break

        map[position] = 'o'

    print(f'Units of sand: {len(np.where(map == "o")[0])}')

    map = np.zeros((max_y + 3, (max_x - min_x) + 1), dtype=object)
    map[:,:] = '.'
    map[-1,:] = '#'
    map[0,500-min_x] = '+'

    for trace in points:
        map = fill(map, trace, min_x)

    while True:
        if map[0, 500-min_x] == 'o':
            print('Full')
            break

        try:
            position = fall((0, 500-min_x), map)
        except ValueError:
            break

        map[position] = 'o'
        #render(map)

    #render(map)
    print(f'Units of sand: {len(np.where(map == "o")[0])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 14')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
