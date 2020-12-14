import re
from collections import defaultdict
from itertools import combinations


def parse_mask(mask_str) -> (int, int):
    zero_mask = int(mask_str.replace('1', '2').replace('0', '1').replace('X', '0').replace('2', '0'), 2)
    ones_mask = int(mask_str.replace('X', '0'), 2)
    x_masks = x_combinations(mask_str.replace('1', '0'))
    return zero_mask, ones_mask, x_masks


def x_combinations(x_str):
    indices = [i for i, x in enumerate(x_str[::-1]) if x == "X"]
    combs = set()
    for comb_len in range(len(indices) + 1):
        for tup in combinations(indices, comb_len):
            empty = 0
            for i in tup:
                empty += 2 ** i
            combs.add(empty)
    return sorted(list(combs))


def apply_mask_v1(val, masks):
    zero_mask, ones_mask = masks
    val = val | ones_mask
    val = ~val
    val = val | zero_mask
    val = ~val
    return val


def apply_mask_v2(val, masks):
    val = val | masks[1]
    val = val & ~masks[2][-1]
    return [val | offset for offset in masks[2]]


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    mem_pat = re.compile(r"mem\[(\d+)\] = (\d+)")

    memory_v1 = defaultdict(int)
    memory_v2 = defaultdict(int)
    masks = None

    for line in lines:
        if line.startswith('mask'):
            masks = parse_mask(line.split('=')[-1].strip())
            continue
        match = mem_pat.match(line)
        addr = int(match[1])
        value = int(match[2])
        memory_v1[addr] = apply_mask_v1(value, masks[:2])
        for a in apply_mask_v2(addr, masks):
            memory_v2[a] = value

    print(f'Part 1: {sum(memory_v1.values())}')
    print(f'Part 2: {sum(memory_v2.values())}')
