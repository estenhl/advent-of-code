import argparse
import re
import numpy as np

from scipy.spatial.distance import cityblock
from tqdm import tqdm


def parse(line: str):
    pattern = (r'Sensor at x=(-?\d+), y=(-?\d+): '
               r'closest beacon is at x=(-?\d+), y=(-?\d+)')
    match = re.fullmatch(pattern, line)

    sensor = (int(match.groups(0)[1]), int(match.groups(0)[0]))
    beacon = (int(match.groups(0)[3]), int(match.groups(0)[2]))

    return sensor, beacon

def between(a, b, c):
    crossproduct = (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])

    if abs(crossproduct) > 0:
        return False

    dotproduct = (c[1] - a[1]) * (b[1] - a[1]) + (c[0] - a[0])*(b[0] - a[0])
    if dotproduct < 0:
        return False

    squaredlengthba = (b[1] - a[1])*(b[1] - a[1]) + (b[0] - a[0])*(b[0] - a[0])
    if dotproduct > squaredlengthba:
        return False

    return True

def intersect(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    if div == 0:
       raise ValueError()

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if not (between(line1[0], line1[1], (x, y)) and between(line2[0], line2[1], (x, y))):
        raise ValueError()

    return x, y

def parallell(line1, line2):
    slopes = [
        (line1[1][0] - line1[0][0]) / (line1[1][1] - line1[0][1]),
        (line2[1][0] - line2[0][0]) / (line2[1][1] - line2[0][1])
    ]

    return slopes[0] == slopes[1]

def compare_edges(*edges, bounds, data):
    if parallell(edges[0], edges[1]):
        raise ValueError()

    try:
        intersection = intersect(edges[0], edges[1])

        if not intersection[0] == int(intersection[0]):
            raise ValueError()

        intersection = tuple([int(x) for x in intersection])

        for modification in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            candidate = np.asarray(intersection) + np.asarray(modification)

            if np.amin(candidate) >= 0 and np.amax(candidate) < bounds:
                inside = False

                for sensor, beacon in data:
                    radius = cityblock(sensor, beacon)

                    if cityblock(sensor, candidate) <= radius:
                        inside = True
                        break

                if not inside:
                    return candidate[1] * 4000000 + candidate[0]

    except ValueError:
        pass

def compare_edge_sets(*edges, bounds, data):
    for i in range(4):
        for j in range(4):
            try:
                frequency = compare_edges(edges[0][i], edges[1][j],
                                          bounds=bounds, data=data)
                return frequency
            except Exception:
                pass

    return None

def solve(input: str, row: int, bounds: int):
    with open(input, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    data = [parse(line) for line in lines]
    seen = set()
    edges = []

    for sensor, beacon in tqdm(data):
        reach = cityblock(sensor, beacon)
        y, x = sensor
        remaining = reach - (abs(row - y))

        seen |= set([x + i for i in range(0, remaining + 1)])
        seen |= set([x - i for i in range(0, remaining + 1)])

        corners = ((
            (y, x + reach),
            (y, x - reach),
            (y + reach, x),
            (y - reach, x)
        ))

        edges.append((
            (corners[0], corners[2]),
            (corners[0], corners[3]),
            (corners[1], corners[2]),
            (corners[1], corners[3])
        ))

    beacons = set([point[1][1] for point in data if point[1][0] == row])
    seen = seen - beacons
    print(f'Searched positions on row {row}: {len(seen)}')

    for i in tqdm(range(len(edges))):
        for j in range(i, len(edges)):
            if i == j:
                continue

            frequency = compare_edge_sets(edges[i], edges[j], bounds=bounds,
                                          data=data)

            if frequency is not None:
                print(f'Tuning frequency: {frequency}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 15')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')
    parser.add_argument('-r', '--row', required=True, type=int,
                        help='Row to count sensors at')
    parser.add_argument('-b', '--bounds', required=True, type=int,
                        help='Maximum bounds of the distress signal')

    args = parser.parse_args()

    solve(args.input, row=args.row, bounds=args.bounds)
