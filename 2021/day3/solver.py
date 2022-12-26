import argparse
import numpy as np

from functools import reduce


def solve(input: str):
    with open(input, 'r') as f:
        bits = np.asarray([[int(x) for x in line.strip()] \
                           for line in f.readlines()])

    common = np.round(np.mean(bits + 1e-8, axis=0)).astype(int)

    to_decimal = lambda x: int(''.join([str(b) for b in x]), 2)
    print(f'Power consumption: {to_decimal(common) * to_decimal(1 - common)}')

    oxygen = bits.copy()
    co2 = bits.copy()

    for i in range(len(bits[0])):
        if len(oxygen) == 1:
            break

        common = np.round(np.mean(oxygen + 1e-8, axis=0)).astype(int)
        oxygen = np.asarray([l for l in oxygen if l[i] == common[i]])

    for i in range(len(bits[0])):
        if len(co2) == 1:
            break

        common = np.round(np.mean(co2 + 1e-8, axis=0)).astype(int)
        co2 = np.asarray([l for l in co2 if l[i] != common[i]])

    print(f'Life support rating: {to_decimal(oxygen[0]) * to_decimal(co2[0])}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves day 3 of AOC 2021')

    parser.add_argument('-i', '--input', required=True, help='Input file')

    args = parser.parse_args()

    solve(args.input)
