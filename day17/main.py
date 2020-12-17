import itertools
from copy import deepcopy

import numpy as np


def in_world(world, q):
    return all([0 <= val < max_world for max_world, val in zip(world.shape, q)])


def get_neighbours(world, q):
    if "seen" not in get_neighbours.__dict__: get_neighbours.seen = {}
    if q in get_neighbours.seen:
        return get_neighbours.seen[q]
    candidates = []
    for tup in itertools.product(*[range(3) for _ in range(len(q))]):
        if all([xyz == 1 for xyz in tup]):
            continue
        candidate = []
        for idx, val in enumerate(tup):
            # (xi + x - 1, yi + y - 1, zi + z - 1)
            candidate.append(val + q[idx] - 1)
        candidates.append(tuple(candidate))

    result = [c for c in candidates if in_world(world, c)]
    get_neighbours.seen[q] = result
    return result


def count_neighbours_active(world, q):
    sum = 0
    for nb in get_neighbours(world, q):
        if world[nb] > 0:
            sum += world[nb]
    return sum


def print_game(game):
    print('========================================')
    for i in range(game.shape[2]):
        print('---------------------------------------')

        print(f'Z = {i}')
        print(game[..., i].T)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        raw_lines = f.readlines()

    lines = []
    for line in raw_lines:
        lines.append([int(char) for char in line.strip().replace('#', '1').replace('.', '0')])

    rounds = 6

    max_width = len(lines[0]) + 2 * rounds
    max_height = len(lines) + 2 * rounds
    max_depth = 2 * rounds + 1
    max_w = max_depth

    game1 = np.zeros((max_width, max_height, max_depth), dtype=np.uint8)
    game2 = np.zeros((max_width, max_height, max_depth, max_w), dtype=np.uint8)

    start_y = 6
    start_z = max_depth // 2
    start_w = start_z
    for i, line in enumerate(lines):
        start_x = 6
        game1[start_x:len(line) + start_x, start_y + i, start_z] = np.array(line)
        game2[start_x:len(line) + start_x, start_y + i, start_z, start_w] = np.array(line)
    # print_game(game)
    next_game = deepcopy(game1)
    for _ in range(6):
        for x in range(max_width):
            for y in range(max_height):
                for z in range(max_depth):
                    active_nbs = count_neighbours_active(game1, (x, y, z))
                    if game1[(x, y, z)] and (active_nbs < 2 or active_nbs > 3):
                        next_game[(x, y, z)] = 0
                    elif not game1[(x, y, z)] and active_nbs == 3:
                        next_game[(x, y, z)] = 1
                    else:
                        next_game[(x, y, z)] = game1[(x, y, z)]
        temp = game1
        game1 = next_game
        next_game = temp

    print(f'Part 1: {game1.sum()}')

    next_game = deepcopy(game2)
    for _ in range(6):
        for x in range(max_width):
            for y in range(max_height):
                for z in range(max_depth):
                    for w in range(max_w):
                        active_nbs = count_neighbours_active(game2, (x, y, z, w))
                        if game2[(x, y, z, w)] and (active_nbs < 2 or active_nbs > 3):
                            next_game[(x, y, z, w)] = 0
                        elif not game2[(x, y, z, w)] and active_nbs == 3:
                            next_game[(x, y, z, w)] = 1
                        else:
                            next_game[(x, y, z, w)] = game2[(x, y, z, w)]

        temp = game2
        game2 = next_game
        next_game = temp

    print(f'Part 2: {game2.sum()}')
