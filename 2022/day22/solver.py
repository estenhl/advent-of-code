from __future__ import annotations

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from typing import Dict, List, Tuple


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

DIRECTIONS = {
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

class Visualizer():
    def __init__(self, boards: np.ndarray):
        positions = list(boards.keys())
        self.height, self.width = boards[positions[0]].map.shape
        ymax = np.amax([position[0] for position in positions])
        xmax = np.amax([position[1] for position in positions])
        self.canvas = np.ones((self.height * (ymax + 1), self.width * (xmax + 1))) * -1

        for position in positions:
            y = position[0] * self.height
            x = position[1] * self.width
            self.canvas[y:y + self.height, x:x + self.width] = boards[tuple(position)].map

        self.image = np.zeros(self.canvas.shape + (3,), dtype=np.uint8)
        self.image[self.canvas == ENCODING['.']] = (255, 255, 255)
        self.image[self.canvas == ENCODING['#']] = (255, 0, 0)
        self.fig = plt.figure(figsize=(9, 9))
        self.drawing = plt.imshow(self.image)
        self.fig.show()
        self.fig.canvas.draw()
        self.prev_position = None


    def update(self, board, position, direction):
        if self.prev_position is not None:
            self.image[self.prev_position] = (255, 0, 255)

        row = board.position[0] * self.height + position[0]
        col = board.position[1] * self.width + position[1]
        self.image[(row, col)] = (0, 255, 0)
        self.prev_position = (row, col)
        self.drawing.set_data(self.image)
        plt.pause(0.01)
        self.fig.canvas.draw()

def render(map: np.ndarray):
    for line in map:
        print(''.join([REVERSE_ENCODING[x] for x in line]))

    print()

def parse_commands(s: str):
    pattern = r'(\d+|L|R)(.*)'
    tokens = []
    matched, next = re.match(pattern, s).groups(0)

    while next != '':
        tokens.append(matched)
        matched, next = re.match(pattern, next).groups(0)

    tokens.append(matched)

    return tokens

def parse(lines: List[str]):
    commands = lines[-1].strip()
    commands = parse_commands(commands)
    map = [[ENCODING[c] for c in line] for line in lines[:-2]]
    width = np.amax([len(line) for line in lines])
    map = np.asarray([line + [ENCODING[' ']] * (width - len(line)) \
                      for line in map])
    max_x = np.amax(np.where(map == ENCODING['.'])[1])
    map = map[:, :(max_x + 1)]

    return map, commands

class Board:
    def __init__(self, map: np.ndarray, position: np.ndarray):
        self.map = map
        self.position = position
        self.neighbours = {'R': None, 'D': None, 'L': None, 'U': None}

    def transition(self, direction: str, position: Tuple[int]):
        if not isinstance(self.neighbours['U'], tuple):
            neighbour = self.neighbours[direction]
            height, width = neighbour.map.shape

            coordinates = {
                'R': lambda x: (x[0], 0),
                'D': lambda x: (0, x[1]),
                'L': lambda x: (x[0], width - 1),
                'U': lambda x: (height - 1, x[1])
            }

            return neighbour, coordinates[direction](position)
        else:
            neighbour, rotations = self.neighbours[direction]
            height, width = neighbour.map.shape

            for _ in range((4 - rotations) % 4):
                prev = position
                position = (position[1], (width - 1) - position[0])
                #print(f'Rotated {prev} to {position}')

            prev = position
            position = (position[0] % height, position[1] % width)
            #print(f'Moduloed {prev} to {position}')

            directions = ['U', 'L', 'D', 'R']
            direction = directions[(directions.index(direction) + rotations) % 4]

            return neighbour, position, direction

    def __str__(self):
        if not isinstance(self.neighbours['U'], tuple):
            return (f'Board({self.position},\n'
                    f'\tR:{self.neighbours["R"].position},\n'
                    f'\tD:{self.neighbours["D"].position},\n'
                    f'\tL:{self.neighbours["L"].position},\n'
                    f'\tU:{self.neighbours["U"].position},\n')
        else:
            return (f'Board({self.position},\n'
                    f'\tR:{self.neighbours["R"][0].position},'
                    f'{self.neighbours["R"][1]}\n'
                    f'\tD:{self.neighbours["D"][0].position},'
                    f'{self.neighbours["D"][1]}\n'
                    f'\tL:{self.neighbours["L"][0].position},'
                    f'{self.neighbours["L"][1]}\n'
                    f'\tU:{self.neighbours["U"][0].position},'
                    f'{self.neighbours["U"][1]}\n')

    def __repr__(self):
        return str(self)

def split(map: np.ndarray):
    height, width = map.shape
    tiles = len(np.where(map != ENCODING[' '])[0])
    size = int(np.sqrt(tiles // 6))

    boards = []
    start = None

    for i in range(0, height, size):
        for j in range(0, width, size):
            if map[i, j] != ENCODING[' ']:
                start = start if start is not None else (i // size, j // size)
                boards.append(Board(map[i:i+size, j:j+size], (i // size, j // size)))

    for i in range(height // size):
        row = [b for b in boards if b.position[0] == i]
        row = sorted(row, key=lambda x: x.position[1])

        for j in range(len(row)):
            row[j].neighbours['L'] = row[(j - 1) % len(row)]
            row[j].neighbours['R'] = row[(j + 1) % len(row)]

    for i in range(width // size):
        col = [b for b in boards if b.position[1] == i]
        col = sorted(col, key=lambda x: x.position[0])

        for j in range(len(col)):
            col[j].neighbours['U'] = col[(j - 1) % len(col)]
            col[j].neighbours['D'] = col[(j + 1) % len(col)]

    return boards, start

def out_of_bounds(board: np.ndarray, position: Tuple[int]):
    height, width = board.map.shape

    return np.amin(position) < 0 or position[0] >= height or \
           position[1] >= width

def move(board: Tuple[int, int], position: Tuple[int], direction: str,
         steps: int):
    if steps == 0:
        return board, position

    current_board = board
    next_board = board
    next = position + DIRECTIONS[direction]['move']

    if out_of_bounds(next_board, next):
        next_board, next = current_board.transition(direction, next)

    if next_board.map[tuple(next)] == ENCODING['#']:
        return current_board, position

    return move(next_board, next, direction, steps-1)

def construct_cube(boards: Dict[Tuple[int], Board]):
    positions = np.asarray(sorted(list(boards.keys())))

    """
    neighbours = [
        {
            'U': (1, 2),
            'R': (5, 2),
            'D': (3, 0),
            'L': (2, 1)
        },
        {
            'U': (0, 2),
            'R': (2, 0),
            'D': (4, 2),
            'L': (5, 3)
        },
        {
            'U': (0, 3),
            'R': (3, 0),
            'D': (4, 1),
            'L': (1, 0)
        },
        {
            'U': (0, 0),
            'R': (5, 3),
            'D': (4, 0),
            'L': (2, 0)
        },
        {
            'U': (3, 0),
            'R': (5, 0),
            'D': (1, 2),
            'L': (2, 3)
        },
        {
            'U': (3, 1),
            'R': (0, 2),
            'D': (1, 1),
            'L': (4, 0)
        }
    ]
    """

    neighbours = [
        {
            'U': (5, 3),
            'R': (1, 0),
            'D': (2, 0),
            'L': (3, 2)
        },
        {
            'U': (5, 0),
            'R': (4, 2),
            'D': (2, 3),
            'L': (0, 0)
        },
        {
            'U': (0, 0),
            'R': (1, 1),
            'D': (4, 0),
            'L': (3, 1)
        },
        {
            'U': (2, 3),
            'R': (4, 0),
            'D': (5, 0),
            'L': (0, 2)
        },
        {
            'U': (2, 0),
            'R': (1, 2),
            'D': (5, 3),
            'L': (3, 0)
        },
        {
            'U': (3, 0),
            'R': (4, 1),
            'D': (1, 0),
            'L': (0, 1)
        }
    ]

    for i in range(len(neighbours)):
        for key in neighbours[i]:
            idx, rotations = neighbours[i][key]
            neighbours[i][key] = (boards[tuple(positions[idx])], rotations)
        boards[tuple(positions[i])].neighbours = neighbours[i]

    return boards[tuple(positions[0])]

def cube_move(board: Tuple[int, int], position: Tuple[int], direction: str,
         steps: int, visualizer):
    if steps == 0:
        return board, position, direction

    current_board = board
    next_board = board
    next = position + DIRECTIONS[direction]['move']
    last_direction = direction

    if out_of_bounds(next_board, next):
        next_board, next, direction = current_board.transition(direction, next)


    if next_board.map[tuple(next)] == ENCODING['#']:
        return current_board, position, last_direction

    return cube_move(next_board, next, direction, steps-1, visualizer)

def solve(input: str):
    with open(input, 'r') as f:
        lines = [x[:-1] for x in f.readlines() if len(x) > 0]

    map, commands = parse(lines)

    boards, start = split(map)
    boards = {board.position: board for board in boards}
    board = boards[start]
    position = np.asarray((0, 0))
    direction = 'R'

    for cmd in commands:
        if cmd in DIRECTIONS:
            direction = DIRECTIONS[direction]['next'][cmd]
            continue

        board, position = move(board, position, direction, int(cmd))

    visualizer = Visualizer(boards)
    height, width = board.map.shape
    row = board.position[0] * height + position[0] + 1
    col = board.position[1] * width + position[1] + 1
    print(f'Value: {1000 * row + 4 * col + DIRECTIONS[direction]["value"]}')

    board = construct_cube(boards)
    position = np.asarray((0, 0))
    direction = 'R'

    for i in range(len(commands)):
        cmd = commands[i]
        if cmd in DIRECTIONS:
            #print(f'Turning {cmd} ({i}/{len(commands)}')
            direction = DIRECTIONS[direction]['next'][cmd]
            continue

        board, position, direction = cube_move(board, position, direction, int(cmd), visualizer)

    row = board.position[0] * height + position[0] + 1
    col = board.position[1] * width + position[1] + 1
    print(f'Value: {1000 * row + 4 * col + DIRECTIONS[direction]["value"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 22')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


