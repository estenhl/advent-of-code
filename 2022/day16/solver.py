import argparse
import re
import numpy as np

from copy import deepcopy
from typing import Any, Dict


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

def solve(input: str):
    with open(input, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    nodes = [parse(line) for line in lines]
    nodes = {node['name']: node for node in nodes}
    nodes = prune(nodes)

    keys, edges = compute_edges(nodes)

    start = {
        'node': 'AA',
        'days': 0,
        'path': 'AA',
        'opened': np.zeros(len(keys)),
    }

    def serialize(state):
        return state['node'] + ''.join(state(['opened'])) + str(state['days'])

    queue = []
    queue.append(start)
    seen = {}

    while len(queue) > 0:
        current = queue.pop()
        print(current)

        if current['days'] >= 3:
            continue

        idx = keys.index(current['node'])

        for i in range(len(edges[idx])):
            if i == idx:
                continue

            queue.append({
                'node': keys[i],
                'days': current['days'] + 1 + edges[idx, i],
                'path': current['path'] + '->' + keys[i]
            })




if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 16')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)
