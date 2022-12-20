import argparse
import re
import numpy as np

from copy import copy, deepcopy
from itertools import combinations
from typing import Any, Dict, List, Set
from tqdm import tqdm


def parse(line: str):
    pattern = (r'Valve (.*) has flow rate=(\d+); '
               r'tunnels? leads? to valves? (.*)')
    match = re.fullmatch(pattern, line)

    name = match.groups(0)[0]
    rate = int(match.groups(0)[1])
    neighbours = match.groups(0)[2].split(', ')

    return {
        'name': name,
        'rate': rate,
        'neighbours': {neighbour: 1 for neighbour in neighbours}
    }


def prune(nodes: Dict[str, Any]):
    nodes = deepcopy(nodes)

    keys = list(nodes.keys())

    for name in keys:
        neighbours = nodes[name]['neighbours']

        if name == 'AA':
            continue

        if nodes[name]['rate'] == 0:
            for other in nodes:
                if name == other:
                    continue

                if name in nodes[other]['neighbours']:
                    for neighbour in neighbours:
                        if neighbour == other:
                            continue

                        if not neighbour in nodes[other]['neighbours']:
                            distance = nodes[other]['neighbours'][name] + \
                                       nodes[name]['neighbours'][neighbour]
                            nodes[other]['neighbours'][neighbour] = distance

                    del nodes[other]['neighbours'][name]

            del nodes[name]

    return nodes

def floyd_warshall(edges: np.ndarray):
    distances = deepcopy(edges)

    for i in range(len(edges)):
        for j in range(len(edges)):
            for k in range(len(edges)):
                distances[j, k] = min(distances[j, k],
                                      distances[j, i] + distances[i, k])

    return distances

def compute_edges(nodes: Dict[str, Any]):
    keys = list(nodes.keys())

    edges = np.ones((len(keys), len(keys))) * np.inf
    edges[np.diag_indices(len(keys))] = 0

    for name in nodes:
        for neighbour in nodes[name]['neighbours']:
            y = keys.index(name)
            x = keys.index(neighbour)
            edges[y, x] = nodes[name]['neighbours'][neighbour]

    edges = floyd_warshall(edges)

    return keys, edges

def score(opened: np.ndarray, rates: List[int]):
    return np.sum([opened[i] * rates[i] \
                   for i in range(len(opened)) if opened[i] > 0])

def solve(input: str):
    with open(input, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    nodes = [parse(line) for line in lines]
    nodes = {node['name']: node for node in nodes}
    nodes = prune(nodes)

    keys, edges = compute_edges(nodes)
    rates = [nodes[key]['rate'] for key in keys]
    edges += 1 - np.eye(len(keys))

    def recurse(name: str, days: int, opened: np.ndarray, limit: int,
                allowed: Set, largest: int = 0):
        idx = keys.index(name)

        opened = copy(opened)
        opened[idx] = limit - days

        mock = copy(opened)
        mock[mock == 0] = limit - days
        potential = score(mock, rates)

        if largest > 0 and potential <= largest:
            return largest

        finished = [opened[i] for i in range(len(opened))\
                    if keys[i] in allowed]

        if days >= limit or np.all(np.asarray(finished) > 0):
            return score(opened, rates)

        scores = []

        for j in range(len(keys)):
            if idx != j and opened[j] == 0 and keys[j] in allowed:
                if len(scores) > 0 and scores[-1] > largest:
                    largest = scores[-1]
                scores.append(recurse(keys[j], days + edges[idx, j], opened,
                                      limit, allowed, largest))

        max_score = np.amax(scores)

        return max_score

    max_score = recurse('AA', 0, np.zeros(len(keys)), 30, set(keys))
    print(f'Max score: {max_score}')
    subsets = list(combinations(keys, len(keys) // 2))
    scores = [recurse('AA', 0, np.zeros(len(keys)), 26, subsets[i]) + \
              recurse('AA', 0, np.zeros(len(keys)), 26,
                      set([key for key in keys if key not in subsets[i]])) \
             for i in tqdm(range(len(subsets)))]
    print(f'Max in combination: {np.amax(scores)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 16')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
