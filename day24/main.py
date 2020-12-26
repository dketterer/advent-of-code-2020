import re
from collections import defaultdict
from copy import copy


def move(x, y, inst):
    if inst == 'e':
        return x + 2, y
    elif inst == 'se':
        return x + 1, y - 1
    elif inst == 'sw':
        return x - 1, y - 1
    elif inst == 'w':
        return x - 2, y
    elif inst == 'nw':
        return x - 1, y + 1
    elif inst == 'ne':
        return x + 1, y + 1


def get_neighbors(x, y):
    if 'seen' not in get_neighbors.__dict__: get_neighbors.seen = {}
    if (x, y) not in get_neighbors.seen:
        get_neighbors.seen[(x, y)] = [move(x, y, inst) for inst in ['e', 'se', 'sw', 'w', 'nw', 'ne']]
    return get_neighbors.seen[(x, y)]


def sum_blacks(tiles):
    return sum([val for val in tiles.values()])


def sum_black_neighbors(pos, tiles):
    return sum([tiles[nb] for nb in get_neighbors(*pos)])


def sum_white_neighbors(pos, tiles):
    return sum([not tiles[nb] for nb in get_neighbors(*pos)])


def get_world_size(tiles):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for pos in tiles.keys():
        x, y = pos
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    return min_x, max_x, min_y, max_y


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    instructions = [line.strip() for line in lines]

    # white = False
    tiles = defaultdict(bool)

    inst_pat = re.compile(r"(e|se|sw|w|nw|ne)")

    for i_line in instructions:
        pos = (0, 0)
        for match in inst_pat.findall(i_line):
            pos = move(*pos, match)
        tiles[pos] = not tiles[pos]

    print(f'Part 1: {sum_blacks(tiles)}')

    next_tiles = copy(tiles)
    for day in range(100):
        min_x, max_x, min_y, max_y = get_world_size(tiles)
        for x in range(min_x - 2, max_x + 2 + 1):
            for y in range(min_y - 1, max_y + 1 + 1):
                white_nbs = sum_white_neighbors((x, y), tiles)
                black_nbs = sum_black_neighbors((x, y), tiles)
                if tiles[(x, y)] and (black_nbs == 0 or black_nbs > 2):
                    next_tiles[(x, y)] = False
                elif not tiles[(x, y)] and black_nbs == 2:
                    next_tiles[(x, y)] = True
                else:
                    next_tiles[(x, y)] = tiles[(x, y)]
        temp = tiles
        tiles = next_tiles
        next_tiles = temp
    print(f'Part 2: {sum_blacks(tiles)}')
