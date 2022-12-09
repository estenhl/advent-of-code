import argparse

from copy import deepcopy


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x[:-1] for x in f.readlines()]

    stack_setup = [l for l in lines \
                   if not (l.startswith('move') or len(l) == 0)][:-1]
    commands = [l for l in lines if l.startswith('move')]

    stacks = {}

    for line in stack_setup[::-1]:
        for char in range(1, len(line), 4):
            if line[char] != ' ':
                idx = (char - 1) // 4

                if not idx in stacks:
                    stacks[int(idx)] = []

                stacks[int(idx)].append(line[char])

    stacks_9001 = deepcopy(stacks)

    for cmd in commands:
        _, count, _, source, _, dest = cmd.split(' ')

        for _ in range(int(count)):
            stacks[int(dest) - 1].append(stacks[int(source) - 1].pop())

        batch = []
        for _ in range(int(count)):
            batch = [stacks_9001[int(source) - 1].pop()] + batch

        stacks_9001[int(dest) - 1] += batch

    tops_9000 = [stacks[key][-1] for key in sorted(stacks.keys())]
    print(f'Top 9000: {"".join(tops_9000)}')

    tops_9001 = [stacks_9001[key][-1] for key in sorted(stacks.keys())]
    print(f'Top 9001: {"".join(tops_9001)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 5')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
