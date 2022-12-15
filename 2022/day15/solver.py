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

def render(map: np.ndarray):
    for line in map:
        print(''.join(line))

def to_formula(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersect(l1, l2):
    l1 = to_formula(*l1)
    l2 = to_formula(*l2)
    D  = l1[0] * l2[1] - l1[1] * l2[0]
    Dx = l1[2] * l2[1] - l1[1] * l2[2]
    Dy = l1[0] * l2[2] - l1[2] * l2[0]

    if D != 0:
        x = Dx / D
        y = Dy / D
        return round(x), round(y)

    return False

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

    intersections = set()

    NUM_TESTS = 2

    for i in tqdm(range(NUM_TESTS)):
        for j in range(i, NUM_TESTS):
            if i == j:
                continue

            for k in range(4):
                for l in range(4):
                    intersection = intersect(edges[i][k], edges[j][l])

                    if intersection:
                        intersections.add(intersection)

    import matplotlib.pyplot as plt
    from skimage.draw import line_aa

    canvas = np.zeros((50, 50, 3))

    print(edges)

    for i in range(1, NUM_TESTS):
        for j in range(4):
            start, end = edges[i][j]
            print(start)
            print(end)
            ysign = np.sign(end[0] - start[0])
            xsign = np.sign(end[1] - start[1])
            for z in range(np.abs(end[0] - start[0])):
                print(z)
                canvas[start[0] + ysign * z, start[1] + xsign * z] = (1, 1, 1)
            #ysign = np.sign(end[0] - start[0])
            #xsign = np.sign()

    for i in intersections:
        print(i)
        canvas[i] = (1, 0, 0)

    plt.imshow(canvas)
    plt.show()
    raise ValueError()
    #(2906626, 2572895)
    #print(intersections)

    print(sorted(intersections))

    #for p in intersections:
    #    print(p[1] * 4000000 + p[1])
    candidates = set()

    for intersection in tqdm(intersections):
        for modification in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            candidate = np.asarray(intersection) + np.asarray(modification)

            if np.amin(candidate) >= 0 and np.amax(candidate) < bounds:
                candidates.add(tuple(candidate))

    print(sorted(candidates))

    for candidate in tqdm(candidates):
        inside = False
        for sensor, beacon in data:
            radius = cityblock(sensor, beacon)

            if cityblock(sensor, candidate) <= radius:
                inside = True
                break

        if not inside:
            print(candidate)
            print(candidate[1] * 4000000 + candidate[0])

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
