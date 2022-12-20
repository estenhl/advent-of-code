import argparse
import numpy as np


EDGES = np.asarray([
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1)
])

def floodfill(arr: np.ndarray, pos: np.ndarray, value: int):
    height, width, depth = arr.shape
    queue = [pos]

    while len(queue) > 0:
        pos = queue.pop()

        if np.amin(pos) < 0 or \
        pos[0] >= height or pos[1] >= width or pos[2] >= depth:
            continue
        elif arr[tuple(pos)] != 0:
            continue

        arr[tuple(pos)] = value

        for edge in EDGES:
            queue.append(pos + edge)


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    coordinates = np.asarray([line.split(',') for line in lines]).astype(int)
    x, y, z = [coordinates[:, i] for i in range(3)]
    ymax, xmax, zmax = [np.amax(coordinates[:,i]) for i in range(3)]

    space = np.zeros((ymax + 2, xmax + 2, zmax + 2))
    space[tuple([x, y, z])] = 1

    surfaces = np.sum([[1 - (space[tuple(coordinate + edge)]) \
                        for edge in EDGES] \
                      for coordinate in coordinates])

    print(f'Surfaces: {surfaces}')

    floodfill(space, (0, 0, 0), 2)

    surfaces = np.sum([[1 if space[tuple(coordinate + edge)] == 2 else 0 \
                        for edge in EDGES] \
                      for coordinate in coordinates])

    print(f'Outer surfaces: {surfaces}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 18')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
