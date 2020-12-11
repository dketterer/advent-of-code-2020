import time
from copy import deepcopy

import numpy as np


def in_ferry(world, q):
    x, y = q
    world_x, world_y = world.shape
    if 0 <= x < world_x and 0 <= y < world_y:
        return True
    return False


def get_neighbours(world, q):
    if "seen" not in get_neighbours.__dict__: get_neighbours.seen = {}
    x, y = q
    if q in get_neighbours.seen:
        return get_neighbours.seen[q]
    # top, top-left, left, bottom-left, bottom, bottom-right, right, top-right
    candidates = [(x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y),
                  (x + 1, y - 1)]
    result = [c for c in candidates if in_ferry(world, c)]
    get_neighbours.seen[q] = result
    return result


def count_neighbours_occupied(world, q):
    sum = 0
    for nb in get_neighbours(world, q):
        if world[nb] > 0:
            sum += world[nb]
    return sum


def get_neigbours_diagonal(world, q):
    if "seen" not in get_neigbours_diagonal.__dict__: get_neigbours_diagonal.seen = {}
    x, y = q
    if q in get_neigbours_diagonal.seen:
        return get_neigbours_diagonal.seen[q]
    world_x, world_y = world.shape
    neighbours = []
    # top, top-left, left, bottom-left, bottom, bottom-right, right, top-right
    for step_x, step_y in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]:
        diag_list = []
        for offset in range(1, max([world_y, world_x])):
            candidate = (x + step_x * offset, y + step_y * offset)
            if in_ferry(world, candidate):
                diag_list.append(candidate)
            else:
                break
        neighbours.append(diag_list)
    get_neigbours_diagonal.seen[q] = neighbours
    return neighbours


def count_neighbours_occupied2(world, q):
    neighbour_list = get_neigbours_diagonal(world, q)
    sum = 0
    for diag in neighbour_list:
        for c in diag:
            if world[c] > 0:
                sum += 1
                break
            if world[c] == 0:
                break
    return sum


def get_seats(world):
    world_x, world_y = world.shape
    seats = []
    for x in range(world_x):
        for y in range(world_y):
            if world[x, y] > -1:
                seats.append((x, y))
    return seats


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    ferry = []
    for line in lines:
        ferry.append([int(c) for c in line.replace('L', '1').replace('.', '0')])
    ferry = np.array(ferry).T - 1
    orig_ferry = deepcopy(ferry)
    seats = get_seats(ferry)

    tic = time.time()
    next_ferry = deepcopy(ferry)
    while True:
        for seat in seats:
            nb_occ = count_neighbours_occupied(ferry, seat)
            if nb_occ == 0:
                next_ferry[seat] = 1
            elif ferry[seat] == 1 and nb_occ >= 4:
                next_ferry[seat] = 0
            else:
                next_ferry[seat] = ferry[seat]

        if (ferry == next_ferry).all():
            break
        temp = ferry
        ferry = next_ferry
        next_ferry = temp
    print(f'Part 1: {np.sum(ferry == 1)}')
    print(time.time() - tic)

    tic = time.time()
    ferry = orig_ferry
    next_ferry = deepcopy(ferry)
    while True:
        for seat in seats:
            nb_occ = count_neighbours_occupied2(ferry, seat)
            if nb_occ == 0:
                next_ferry[seat] = 1
            elif ferry[seat] == 1 and nb_occ >= 5:
                next_ferry[seat] = 0
            else:
                next_ferry[seat] = ferry[seat]
        if (ferry == next_ferry).all():
            break
        temp = ferry
        ferry = next_ferry
        next_ferry = temp
    print(f'Part 2: {np.sum(ferry == 1)}')
    print(time.time() - tic)
