import argparse
import re
import matplotlib.pyplot as plt
import numpy as np

from time import sleep


class Visualizer():
    def __init__(self, map: np.ndarray):
        self.fig = plt.figure(figsize=(10, 10))
        self.fig.show()

        self.img = np.zeros(map.shape + (3,))
        self.img[np.where(map == ENCODING['#'])] = (1, 0, 0)
        self.img[np.where(map == ENCODING['.'])] = (1, 1, 1)

        self.imshow = plt.imshow(self.img)

        self.fig.canvas.draw()

    def update(self, position: np.ndarray):
        self.img[tuple(position)] = (0, 1, 0)
        self.imshow.set_data(self.img)
        plt.pause(SLEEP)
        self.fig.canvas.draw()

ENCODING = {
    '.': 0,
    ' ': -1,
    '#': -2,
    '>': 1,
    'v': 2,
    '<': 3,
    '^': 4
}
REVERSE_ENCODING = {value: key for key, value in ENCODING.items()}
SLEEP = 0.01

def render(map: np.ndarray):
    for line in map:
        print(''.join([REVERSE_ENCODING[x] for x in line]))

    print()

def parse(s: str):
    pattern = r'(\d+|L|R)(.*)'
    tokens = []
    matched, next = re.match(pattern, s).groups(0)

    while next != '':
        tokens.append(matched)
        matched, next = re.match(pattern, next).groups(0)

    tokens.append(matched)

    return tokens

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x[:-1] for x in f.readlines() if len(x) > 0]

    commands = lines[-1].strip()
    commands = parse(commands)
    map = [[ENCODING[c] for c in line] for line in lines[:-2]]
    width = np.amax([len(line) for line in lines])
    map = np.asarray([line + [ENCODING[' ']] * (width - len(line)) \
                      for line in map])
    max_x = np.amax(np.where(map == ENCODING['.'])[1])
    map = map[:, :(max_x + 1)]

    directions = {
        'R': {
            'symbol': '>',
            'move': np.asarray([0, 1]),
            'next': {'R': 'D', 'L': 'U'},
            'value': 0
        },
        'D': {
            'symbol': 'v',
            'move': np.asarray([1, 0]),
            'next': {'R': 'L', 'L': 'R'},
            'value': 1
        },
        'L': {
            'symbol': '<',
            'move': np.asarray([0, -1]),
            'next': {'R': 'U', 'L': 'D'},
            'value': 2
        },
        'U': {
            'symbol': '^',
            'move': np.asarray([-1, 0]),
            'next': {'R': 'R', 'L': 'L'},
            'value': 3
        }
    }

    def out_of_bounds(position: np.ndarray):
        y, x = position
        return min(y, x) < 0 or y >= len(map) or x >= len(map[0])

    def loop(position: np.ndarray, direction: str):
        next = position + directions[direction]['move']
        next = np.asarray([next[0] % len(map), next[1] % len(map[0])])


        while map[tuple(next)] == ENCODING[' ']:
            next = next + directions[direction]['move']
            next = np.asarray([next[0] % len(map), next[1] % len(map[0])])

        return next

    def move(position: np.ndarray, direction: str, moves: int):
        if moves == 0:
            return position

        current = position

        for _ in range(moves):
            next = current + directions[direction]['move']

            if out_of_bounds(next) or map[tuple(next)] == ENCODING[' ']:
                next = loop(current, direction)
            if map[tuple(next)] == ENCODING['#']:
                return current

            map[tuple(next)] = ENCODING[directions[direction]['symbol']]
            #visualizer.update(next)
            #sleep(SLEEP)
            current = next

        return next

    #visualizer = Visualizer(map)
    current = np.asarray((0, np.amin(np.where(map[0] == ENCODING['.'])[0])))
    direction = 'R'

    for cmd in commands:
        map[tuple(current)] = ENCODING[directions[direction]['symbol']]

        if cmd in ['L', 'R']:
            direction = directions[direction]['next'][cmd]
            map[tuple(current)] = ENCODING[directions[direction]['symbol']]
            continue

        current = move(current, direction, int(cmd))
        #visualizer.update(current)
        #sleep(SLEEP)

    value = (current[0] + 1) * 1000 + \
            (current[1] + 1) * 4 + \
            directions[direction]['value']

    print(current)
    print(direction)
    print(f'Final value: {value}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 22')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


