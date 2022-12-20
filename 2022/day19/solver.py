import argparse
import re
import numpy as np

from copy import deepcopy
from typing import Any, Dict
from tqdm import tqdm


def parse(line: str):
    pattern = (r'Blueprint (\d+): '
               r'Each ore robot costs (\d+) ore. '
               r'Each clay robot costs (\d+) ore. '
               r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
               r'Each geode robot costs (\d+) ore and (\d+) obsidian.')

    match = re.fullmatch(pattern, line)

    return {
        'id': int(match.groups(0)[0]),
        'ore': {'ore': int(match.groups(0)[1])},
        'clay': {'ore': int(match.groups(0)[2])},
        'obsidian': {
            'ore': int(match.groups(0)[3]),
            'clay': int(match.groups(0)[4])
        },
        'geode': {
            'ore': int(match.groups(0)[5]),
            'obsidian': int(match.groups(0)[6])
        }
    }

def _build(state, blueprint, name):
    resources = {key: state['resources'][key] - blueprint[name][key] \
                 if key in blueprint[name] else state['resources'][key] \
                 for key in state['resources']}
    robots = {key: state['robots'][key] + (1 if key == name else 0) \
              for key in state['robots']}

    return {
        'resources': resources,
        'robots': robots
    }

def build(state, blueprint):
    resources = state['resources']
    new_states = [deepcopy(state)]

    if resources['obsidian'] >= blueprint['geode']['obsidian'] and \
       resources['ore'] >= blueprint['geode']['ore']:
        return [_build(state, blueprint, 'geode')]


    if resources['clay'] >= blueprint['obsidian']['clay'] and \
       resources['ore'] >= blueprint['obsidian']['ore']:
        return [_build(state, blueprint, 'obsidian')]


    if resources['ore'] >= blueprint['clay']['ore'] and \
       state['robots']['clay'] <= blueprint['obsidian']['clay']:
        new_states.append(_build(state, blueprint, 'clay'))

    max_ore_requirement = np.max([blueprint[key]['ore'] \
                                  for key in blueprint if key != 'id'])
    if resources['ore'] >= blueprint['ore']['ore'] and \
        state['robots']['ore'] <= max_ore_requirement:
        new_states.append(_build(state, blueprint, 'ore'))

    return new_states

def gather(robots):
    return {key: robots[key] for key in robots}

def memoize(f):
    memoized = {}

    def wrapper(state, blueprint, limit, minute: int = 0):
        key = f'id={blueprint["id"]},limit={limit}'
        key += 'resources=' + '-'.join([f'{key}={state["resources"][key]}' \
                                        for key in state['resources']])
        key += ',robots=' + '-'.join([f'{key}={state["robots"][key]}' \
                                      for key in state['robots']])
        key += f',minutes={minute}'

        if not key in memoized:
            memoized[key] = f(state, blueprint, limit, minute)

        return memoized[key]

    return wrapper

@memoize
def iterate(state: Dict[str, Any], blueprint: Dict[str, Any], limit: int, minute: int = 0):
    if minute == limit:
        return state['resources']['geode']

    robots = build(state, blueprint)
    new_ores = gather(state['robots'])

    max_value = -float('inf')

    for new_state in robots:
        for resource in new_ores:
            new_state['resources'][resource] += new_ores[resource]

        value = iterate(new_state, blueprint, limit, minute + 1)

        if value > max_value:
            max_value = value

    return max_value


def solve(input: str):
    with open(input, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    blueprints = [parse(line) for line in lines]

    start = {
        'robots': {
            'ore': 1,
            'clay': 0,
            'obsidian': 0,
            'geode': 0
        },
        'resources': {
            'ore': 0,
            'clay': 0,
            'obsidian': 0,
            'geode': 0
        }
    }

    values = [iterate(start, blueprint, limit=24) for blueprint in tqdm(blueprints)]
    print(f'Quality: {np.sum(values * np.arange(1, len(values) + 1))}')

    values = [iterate(start, blueprints[i], limit=32) \
              for i in tqdm(range(min(3, len(blueprints))))]
    print(np.prod(values))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 19')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


