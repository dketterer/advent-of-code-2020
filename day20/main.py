import math
import re
from collections import defaultdict

import numpy as np


def boundary_to_signature(boundary):
    return tuple(sorted([boundary, boundary[::-1]]))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    assert not lines[-1], 'Must have 2 empty lines at the end of the input file!'

    tiles_by_id = {}
    tiles_by_signature = defaultdict(list)
    np_tiles_by_id = {}

    id = None
    front = ""
    back = ""
    top = ""
    bottom = ""

    tile_size = 10

    tile = np.zeros((tile_size, tile_size), dtype=np.uint8)

    id_pat = re.compile(r"^Tile (\d+):$")
    tile_row = 0
    for i, line in enumerate(lines):
        if not line:
            bottom = lines[i - 1]
            front = front[::-1]
            bottom = bottom[::-1]

            front = boundary_to_signature(front)
            bottom = boundary_to_signature(bottom)
            back = boundary_to_signature(back)
            top = boundary_to_signature(top)

            tiles_by_id[id] = [front, back, bottom, top]
            tiles_by_signature[front].append(id)
            tiles_by_signature[back].append(id)
            tiles_by_signature[top].append(id)
            tiles_by_signature[bottom].append(id)

            np_tiles_by_id[id] = tile
            print(tile)

            id = None
            front = ""
            back = ""
            top = ""
            bottom = ""
            tile = np.zeros((tile_size, tile_size), dtype=np.uint8)
        elif id_pat.match(line):
            id = int(id_pat.match(line)[1])
            top = lines[i + 1]
            tile_row = 0
        else:
            tile[tile_row, :] = np.array([int(char) for char in line.replace('#', '1').replace('.', '0')])
            tile_row += 1
            front += line[0]
            back += line[-1]

    # print(tiles_by_signature)
    # print(np_tiles_by_id)

    outer_ids = set()
    for boundary, ids in tiles_by_signature.items():
        if len(ids) == 1:
            for id in ids:
                outer_ids.add(id)

    print(outer_ids)
    corner_ids = []
    for id in list(outer_ids):
        non_matching = 0
        for boundary in tiles_by_id[id]:
            if len(tiles_by_signature[boundary]) == 1:
                non_matching += 1
        if non_matching == 2:
            corner_ids.append(id)

    print(f'Part 1: {math.prod(corner_ids)}')
