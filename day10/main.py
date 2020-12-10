from collections import defaultdict


def walk(jolts, map, index):
    if map[index]:
        return map[index]
    if index >= len(jolts) - 1:
        map[index] = 1
        return 1
    result = 0
    to_go = 3
    for offset in range(1, 4):
        if index + offset < len(jolts) and jolts[index + offset] <= to_go:
            result += walk(jolts, map, index + offset)
            to_go -= jolts[index + offset]
        else:
            break
    map[index] = result
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    jolts = [0] + sorted([int(line) for line in lines])
    delta_jolts = [jolts[i + 1] - jolt for i, jolt in enumerate(jolts[:-1])]

    diff_1 = sum(map(lambda j: j == 1, delta_jolts))
    diff_3 = sum(map(lambda j: j == 3, delta_jolts)) + 1
    print(f'Part 1: {diff_1 * diff_3}')
    print(f'Part 2: {walk([0] + delta_jolts, defaultdict(int), 0)}')
