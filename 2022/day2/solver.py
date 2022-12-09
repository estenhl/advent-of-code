with open('input.txt', 'r') as f:
    lines = [x.strip() for x in f.readlines()]

mapping = {
    'A X': 'A Z',
    'A Y': 'A X',
    'A Z': 'A Y',
    'B X': 'B X',
    'B Y': 'B Y',
    'B Z': 'B Z',
    'C X': 'C Y',
    'C Y': 'C Z',
    'C Z': 'C X'
}

scores = {
    'A X': 1 + 3,
    'A Y': 2 + 6,
    'A Z': 3 + 0,
    'B X': 1 + 0,
    'B Y': 2 + 3,
    'B Z': 3 + 6,
    'C X': 1 + 6,
    'C Y': 2 + 0,
    'C Z': 3 + 3
}

total = sum([scores[line] for line in lines])
mapped = sum([scores[mapping[line]] for line in lines])

print(f'Score: {total}')
print(f'Mapped score: {mapped}')

