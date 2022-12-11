import argparse
import re
import numpy as np

from tqdm import tqdm


def _initialize(chunk):
    id = int(re.fullmatch(r'Monkey (\d+):', chunk[0]).groups(0)[0])
    starting = re.fullmatch(r'Starting items: (.*)', chunk[1]).groups(0)[0]
    starting = [int(x) for x in starting.split(', ')]
    op = re.fullmatch(r'Operation: (.*)', chunk[2]).groups(0)[0]
    divisor = int(re.fullmatch(r'Test: divisible by (\d+)',
                               chunk[3]).groups(0)[0])
    true_target = int(re.fullmatch(r'If true: throw to monkey (\d+)',
                                   chunk[4]).groups(0)[0])
    false_target = int(re.fullmatch(r'If false: throw to monkey (\d+)',
                                    chunk[5]).groups(0)[0])

    return {
        'id': id,
        'items': starting,
        'operation': op,
        'divisor': divisor,
        'targets': {
            True: true_target,
            False: false_target
        },
        'inspections': 0
    }

def evaluate(operation: str, old: int):
    return eval(operation.split('=')[1])


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    chunks = [lines[i:i+6] for i in np.arange(0, len(lines), 7)]
    monkeys = [_initialize(chunk) for chunk in chunks]

    for _ in tqdm(range(20)):
        for monkey in monkeys:
            items = monkey['items']

            for item in items:
                monkey['inspections'] += 1
                item = evaluate(monkey['operation'], item)
                item = item // 3
                target = monkey['targets'][item % monkey['divisor'] == 0]
                monkeys[target]['items'].append(item)

            monkey['items'] = []

    inspections = sorted([monkey['inspections'] for monkey in monkeys],
                          reverse=True)
    print(f'Monkey business: {inspections[0] * inspections[1]}')

    monkeys = [_initialize(chunk) for chunk in chunks]
    factor = np.prod([monkey['divisor'] for monkey in monkeys])

    for _ in tqdm(range(10000)):
        for monkey in monkeys:
            items = monkey['items']

            for item in items:
                monkey['inspections'] += 1
                item = evaluate(monkey['operation'], item)
                item = item % factor
                target = monkey['targets'][item % monkey['divisor'] == 0]
                monkeys[target]['items'].append(item)

            monkey['items'] = []

    inspections = sorted([monkey['inspections'] for monkey in monkeys],
                          reverse=True)
    print(f'Monkey business: {inspections[0] * inspections[1]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 11')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
