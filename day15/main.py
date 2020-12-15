from collections import defaultdict

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    start = [int(char) for char in lines[0].split(',')]

    position = {}
    seen = defaultdict(bool)
    for count, val in enumerate(start):
        position[val] = count

    last = start[-1]
    for count in range(len(start), 30000000):
        nexxt = 0 if not seen[last] else count - position[last] - 1
        if nexxt not in position:
            position[nexxt] = count - 1
        else:
            seen[nexxt] = True
        position[last] = count - 1
        last = nexxt
        if count == 2019:
            print(f'Part 1: {last}')

    print(f'Part 2: {last}')
