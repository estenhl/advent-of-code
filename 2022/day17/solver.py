import argparse
import matplotlib.pyplot as plt
import numpy as np

from copy import deepcopy
from time import sleep
from typing import Tuple


class Visualizer():
    def __init__(self):
        self.fig = plt.gcf()
        self.fig.show()
        self.fig.canvas.draw()
        print('Starting')


    def update(self, room: np.ndarray, highest: int, stone: np.asarray = None,
               position: Tuple[int] = None):
        img = np.ones((20, 7, 3))

        if stone is not None and position is not None:
            room = deepcopy(room)
            height, width = stone.shape
            room[position[0]:position[0] + height, \
                position[1]:position[1] + width] += stone[::-1] * 2

        highest = max(20, highest)
        subset = room[highest - 20:highest][::-1]
        img[subset == 1] = (0, 0, 0)
        img[subset == 2] = (0, 1, 0)
        img[subset == 3] = (1, 0, 0)
        plt.imshow(img)
        plt.pause(0.01)
        self.fig.canvas.draw()

def solve(input: str):
    with open(input, 'r') as f:
        characters = [c for c in f.read() if c in '<>']

    stones = [
        np.asarray([[1, 1, 1, 1]]),
        np.asarray([
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
        ]),
        np.asarray([
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1]
        ]),
        np.asarray([[1], [1], [1], [1]]),
        np.asarray([
            [1, 1],
            [1, 1]
        ])
    ]

    i = 0
    room = np.zeros((5000*4, 7), dtype=int)
    highest = 0
    wind_counter = 0
    states = {}
    heights = []

    while True:
        stone = stones[i % len(stones)]
        height, width = stone.shape
        current = (highest + 3, 2)

        while True:
            y, x = current
            region = room[y:y + height, x:x + width]

            if y < 0 or np.sum(region * stone[::-1]) > 0:
                room[y + 1:y + height + 1, x:x + width] = \
                    np.maximum(room[y + 1:y + height + 1, x:x + width],
                               stone[::-1,:])
                highest = np.amax(np.where(room != 0)[0]) + 1
                break

            wind = characters[wind_counter]

            if wind == '<' and current[1] > 0 and \
               np.sum(stone[::-1, 0] * room[y:y + height, x - 1]) == 0 and \
               (width == 1 or np.sum(stone[::-1, 1] * room[y:y + height, x]) == 0):
                current = (y, x - 1)
            elif wind == '>' and x + width < len(room[0]) and \
                 np.sum(stone[::-1,-1] * room[y:y + height, x + width]) == 0 and \
                (width == 1 or np.sum(stone[::-1, -2] * room[y:y + height, x + width - 1]) == 0):
                current = (y, x + 1)

            current = (current[0] - 1, current[1])

            wind_counter = (wind_counter + 1) % len(characters)


        encoding = (
            ''.join(room[highest-100:highest].flatten().astype(str)),
            i % len(stones),
            wind_counter
        )


        if encoding in states:
            starting_idx, starting_height = states[encoding]
            cycle_length = i - starting_idx
            cycle_height = highest - starting_height

            cycles = (1000000000000 - 1) // cycle_length
            remainder = (1000000000000- 1) % cycle_length
            remaining_height = heights[remainder]
            height = remaining_height + (cycle_height * cycles)
            print(f'After 2022 rocks: {heights[2021]}')
            print(f'After 1000000000000 rocks: {height}')

            break

        states[encoding] = (i, highest)
        i += 1
        heights.append(highest)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 17')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
