import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Set

import numpy as np
from scipy.signal import convolve2d


@dataclass
class Tile:
    id: int
    full_tile: np.array
    non_matching_sides: Set = field(default_factory=set)

    @staticmethod
    def as_signature(boundary):
        return tuple(sorted([boundary, boundary[::-1]]))

    def rotate_left(self, times=1):
        self.full_tile = np.rot90(self.full_tile, times, (0, 1))

    def fliplr(self):
        self.full_tile = np.fliplr(self.full_tile)

    def flipud(self):
        self.full_tile = np.flipud(self.full_tile)

    def rotate_right(self, times=1):
        self.full_tile = np.rot90(self.full_tile, times, (1, 0))

    @property
    def inner_tile(self):
        return self.full_tile[1:-1, 1:-1]

    @property
    def top(self):
        return self.full_tile[0, :].tobytes()

    @property
    def left(self):
        return self.full_tile[:, 0].tobytes()

    @property
    def bottom(self):
        return self.full_tile[-1, :].tobytes()

    @property
    def right(self):
        return self.full_tile[:, -1].tobytes()

    @property
    def signatures(self):
        return list(map(self.as_signature, [self.top, self.left, self.bottom, self.right]))

    def match(self, other_signature):
        try:
            return self.signatures.index(other_signature)
        except:
            return -1

    def adjust_to_other(self, other_boundary, face_to='l'):
        boundary_idx = self.match(Tile.as_signature(other_boundary))
        if boundary_idx > -1:
            # we need to match the right side of a tile -> rotate matching to left
            if face_to == 'l':
                # rotate
                self.rotate_right((boundary_idx - 1) % 4)
                if self.left != other_boundary:
                    self.flipud()
                assert self.left == other_boundary
            elif face_to == 't':
                self.rotate_right(boundary_idx)
                if self.top != other_boundary:
                    self.fliplr()
                assert self.top == other_boundary
            return True
        else:
            return False


def build_picture(raw_picture, wh, tile_size):
    picture = np.zeros((wh * (tile_size - 2), wh * (tile_size - 2)), dtype=np.uint8)
    for key, value in raw_picture.items():
        x, y = key
        start_x = (tile_size - 2) * x
        start_y = (tile_size - 2) * y
        picture[start_y:start_y + tile_size - 2, start_x:start_x + tile_size - 2] = value.inner_tile
    return picture


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    assert not lines[-1], 'Must have 2 empty lines at the end of the input file!'

    tile_size = 10
    id_pat = re.compile(r"^Tile (\d+):$")

    tiles_by_id = {}
    tiles_by_signature = defaultdict(list)

    id = None
    np_tile = np.zeros((tile_size, tile_size), dtype=np.uint8)
    tile_row = 0

    for i, line in enumerate(lines):
        if not line:
            tile = Tile(id, np_tile)

            tiles_by_id[id] = tile
            for sign in tile.signatures:
                tiles_by_signature[sign].append(tile)

            id = None
            np_tile = np.zeros((tile_size, tile_size), dtype=np.uint8)
        elif id_pat.match(line):
            id = int(id_pat.match(line)[1])
            tile_row = 0
        else:
            np_tile[tile_row, :] = np.array([int(char) for char in line.replace('#', '1').replace('.', '0')])
            tile_row += 1
    num_tile_width = int(round(math.sqrt(len(tiles_by_id))))

    outer_ids = set()
    for boundary, tiles in tiles_by_signature.items():
        if len(tiles) == 1:
            for tile in tiles:
                outer_ids.add(tile.id)

    corner_ids = []
    for id in list(outer_ids):
        non_matching = 0
        for sign_idx, signature in enumerate(tiles_by_id[id].signatures):
            if len(tiles_by_signature[signature]) == 1:
                non_matching += 1
                tiles_by_id[id].non_matching_sides.add(sign_idx)
        if non_matching == 2:
            corner_ids.append(id)

    print(f'Part 1: {math.prod(corner_ids)}')

    # start puzzling
    raw_picture = {}

    # set top left corner
    curr_tile_id = corner_ids[0]
    corner_sides = list(tiles_by_id[curr_tile_id].non_matching_sides)
    if 0 in corner_sides and 3 in corner_sides:
        tiles_by_id[curr_tile_id].rotate_left()
    else:
        tiles_by_id[curr_tile_id].rotate_right(min(corner_sides))
    raw_picture[(0, 0)] = tiles_by_id[curr_tile_id]

    tiles_by_id.pop(curr_tile_id)
    open_list = list(tiles_by_id.values())
    for y in range(num_tile_width):
        for x in range(num_tile_width):
            if x == 0 and y == 0:
                continue
            candidates = open_list
            open_list = []
            # find the next matching at pos (x,y)
            if (x - 1, y) in raw_picture:
                for cand in candidates:
                    if cand.adjust_to_other(raw_picture[(x - 1, y)].right, 'l'):
                        raw_picture[(x, y)] = cand
                    else:
                        open_list.append(cand)
            elif (x, y - 1) in raw_picture:
                for cand in candidates:
                    if cand.adjust_to_other(raw_picture[(x, y - 1)].bottom, 't'):
                        raw_picture[(x, y)] = cand
                    else:
                        open_list.append(cand)

    picture = build_picture(raw_picture, num_tile_width, tile_size)

    seamonster_text = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']
    seamonster_text = [line.replace('#', '1').replace(' ', '0') for line in seamonster_text]
    seamonster_kernel = np.array([[int(char) for char in line] for line in seamonster_text])

    pictures = []
    pictures.append(picture.copy())
    picture = np.rot90(picture)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 2)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 3)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 4)
    picture = np.fliplr(picture)
    pictures.append(picture.copy())
    picture = np.rot90(picture)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 2)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 3)
    pictures.append(picture.copy())
    picture = np.rot90(picture, 4)

    sm_count = 0
    for picture in pictures:
        result_space = convolve2d(picture, seamonster_kernel, mode='valid')
        result_space = result_space.astype(np.uint8)
        count_monsters = np.count_nonzero(result_space == seamonster_kernel.sum())
        if count_monsters:
            sm_count = count_monsters

    print(f'Seamonsters: {sm_count}')
    rough_waters = picture.sum() - seamonster_kernel.sum() * sm_count
    print(f'Part 2: {int(rough_waters)}')
