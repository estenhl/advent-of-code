import argparse
import numpy as np

from queue import PriorityQueue


def solve(input: str):
    with open(input, 'r') as f:
        map = np.asarray([[c for c in line.strip()] for line in f.readlines() \
                         if len(line) > 0])

    height, width = map.shape

    start = np.where(map == 'S')
    start = (start[0][0], start[1][0])
    map[start] = 'a'
    end = np.where(map == 'E')
    end = (end[0][0], end[1][0])
    map[end] = 'z'

    seen = set([start])
    queue = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        steps, current = queue.get()

        if current == end:
            print(f'Steps from start to end: {steps}')
            break

        for step in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            idx = (current[0] + step[0], current[1] + step[1])

            if np.amin(idx) < 0 or idx[0] >= height or idx[1] >= width:
                continue

            if ord(map[idx]) - ord(map[current]) > 1:
                continue

            if idx in seen:
                continue

            queue.put((steps + 1, idx))
            seen.add(idx)

    seen = set([end])
    queue = PriorityQueue()
    queue.put((0, end))

    while not queue.empty():
        steps, current = queue.get()

        if map[current] == 'a':
            print(f'Steps from best start to end: {steps}')
            break

        for step in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            idx = (current[0] + step[0], current[1] + step[1])

            if np.amin(idx) < 0 or idx[0] >= height or idx[1] >= width:
                continue

            if ord(map[current]) - ord(map[idx]) > 1:
                continue

            if idx in seen:
                continue

            queue.put((steps + 1, idx))
            seen.add(idx)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 12')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
