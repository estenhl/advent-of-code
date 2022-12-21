import argparse
import re


def parse(line: str):
    name, op = line.split(': ')

    try:
        op = int(op)
    except Exception:
        pass

    return {
        'name': name,
        'op': op
    }

def solve(input: str):
    with open(input, 'r') as f:
        monkeys = [parse(x.strip()) for x in f.readlines()]

    monkeys = {monkey['name']: monkey['op'] for monkey in monkeys}

    def recurse(name: str):
        op = monkeys[name]

        if isinstance(op, int):
            return op

        name1, operator, name2 = op.split(' ')

        if operator == '/':
            operator = '//'

        value1 = recurse(name1)
        value2 = recurse(name2)

        return eval(f'{value1} {operator} {value2}')

    print(f'Root yells: {recurse("root")}')

    def compile(name: str):
        if name == 'humn':
            return 'humn'

        op = monkeys[name]

        if isinstance(op, int):
            return op

        name1, operator, name2 = op.split(' ')

        if name == 'root':
            operator = '=='

        value1 = compile(name1)
        value2 = compile(name2)

        formula = f'({value1} {operator} {value2})'

        if 'humn' in formula:
            return formula

        return int(eval(formula))

    formula = compile('root')
    formula = formula[1:-1]
    lhs, rhs = formula.split(' == ')
    rhs = int(rhs)

    patterns = {
        r'\((\d+) \+ (.*)\)': lambda match, rhs: \
            (match.groups(0)[1], rhs - int(match.groups(0)[0])),
        r'\((.*) \+ (\d+)\)': lambda match, rhs: \
            (match.groups(0)[0], rhs - int(match.groups(0)[1])),
        r'\((\d+) \* (.*)\)': lambda match, rhs: \
            (match.groups(0)[1], rhs // int(match.groups(0)[0])),
        r'\((.*) \* (\d+)\)': lambda match, rhs: \
            (match.groups(0)[0], rhs // int(match.groups(0)[1])),
        r'\((\d+) - (.*)\)': lambda match, rhs: \
            (match.groups(0)[1], -(rhs - int(match.groups(0)[0]))),
        r'\((.*) - (\d+)\)': lambda match, rhs: \
            (match.groups(0)[0], rhs + int(match.groups(0)[1])),
        r'\((.*) / (\d+)\)': lambda match, rhs: \
            (match.groups(0)[0], rhs * int(match.groups(0)[1]))
    }

    while True:
        if lhs == 'humn':
            print(f'Human must yell: {rhs}')
            break


        matched = False
        for pattern in patterns:
            match = re.fullmatch(pattern, lhs)

            if match:
                lhs, rhs = patterns[pattern](match, rhs)
                matched = True
                continue

        if not matched:
            raise NotImplementedError()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves AOC 2022 day 21')

    parser.add_argument('-i', '--input', required=True,
                        help='Path to input file')

    args = parser.parse_args()

    solve(args.input)


