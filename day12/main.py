from dataclasses import dataclass

import numpy as np


@dataclass
class WorldPos:
    x: int
    y: int
    theta: int


def transform_wp_ship(ship_pos, wp_pos):
    rad_theta = np.radians(ship_pos.theta)
    T_SW = np.array([[round(np.cos(rad_theta)), round(-np.sin(rad_theta)), ship_pos.x],
                     [round(np.sin(rad_theta)), round(np.cos(rad_theta)), ship_pos.y],
                     [0, 0, 1]])
    result = np.dot(T_SW, np.array([wp_pos.x, wp_pos.y, 1]).T)
    return WorldPos(int(result[0]), int(result[1]), 0)


def transform_ship_wp(ship_pos, wp_pos, target):
    rad_theta = np.radians(ship_pos.theta)
    T_SW = np.array([[round(np.cos(rad_theta)), round(-np.sin(rad_theta)), ship_pos.x],
                     [round(np.sin(rad_theta)), round(np.cos(rad_theta)), ship_pos.y],
                     [0, 0, 1]])
    T_WS = np.linalg.inv(T_SW)
    result = np.dot(T_WS, np.array([wp_pos.x, wp_pos.y, 1]).T)
    target.x = int(result[0])
    target.y = int(result[1])


test_wp = WorldPos(2, 0, 0)
test_ship = WorldPos(10, 10, 90)
transform_ship_wp(test_ship, transform_wp_ship(test_ship, test_wp), test_wp)
assert (test_wp.x == 2)
assert (test_wp.y == 0)


def move1(ship_pos, instruction):
    char, num = instruction
    if char == 'N':
        ship_pos.y += num
    elif char == 'S':
        ship_pos.y -= num
    elif char == 'E':
        ship_pos.x -= num
    elif char == 'W':
        ship_pos.x += num
    elif char == 'L':
        ship_pos.theta = (ship_pos.theta + num) % 360
    elif char == 'R':
        ship_pos.theta = (ship_pos.theta - num) % 360
    elif char == 'F':
        # world_pos.x += round(np.cos(world_pos.theta * np.pi / 180)) * num
        # world_pos.y += round(np.sin(world_pos.theta * np.pi / 180)) * num
        if ship_pos.theta == 0:
            move1(ship_pos, ('E', num))
        elif ship_pos.theta == 90:
            move1(ship_pos, ('N', num))
        elif ship_pos.theta == 180:
            move1(ship_pos, ('W', num))
        elif ship_pos.theta == 270:
            move1(ship_pos, ('S', num))


def move2(ship_pos, wp_pos, instruction):
    # wp_pos is a relative position
    char, num = instruction
    if char == 'N':
        wp_in_ship_frame = transform_wp_ship(ship_pos, wp_pos)
        wp_in_ship_frame.y += num
        transform_ship_wp(ship_pos, wp_in_ship_frame, wp_pos)
    elif char == 'S':
        wp_in_ship_frame = transform_wp_ship(ship_pos, wp_pos)
        wp_in_ship_frame.y -= num
        transform_ship_wp(ship_pos, wp_in_ship_frame, wp_pos)
    elif char == 'E':
        wp_in_ship_frame = transform_wp_ship(ship_pos, wp_pos)
        wp_in_ship_frame.x += num
        transform_ship_wp(ship_pos, wp_in_ship_frame, wp_pos)
    elif char == 'W':
        wp_in_ship_frame = transform_wp_ship(ship_pos, wp_pos)
        wp_in_ship_frame.x -= num
        transform_ship_wp(ship_pos, wp_in_ship_frame, wp_pos)
    elif char == 'L':
        ship_pos.theta = (ship_pos.theta + num) % 360
    elif char == 'R':
        ship_pos.theta = (ship_pos.theta - num) % 360
    elif char == 'F':
        for _ in range(num):
            wp_in_ship_frame = transform_wp_ship(ship_pos, wp_pos)
            ship_pos.x = wp_in_ship_frame.x
            ship_pos.y = wp_in_ship_frame.y


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    instructions = [(line.strip()[0], int(line.strip()[1:])) for line in lines]
    ship_pos1 = WorldPos(0, 0, 0)
    ship_pos2 = WorldPos(0, 0, 0)
    wp_pos = WorldPos(10, 1, 0)

    for inst in instructions:
        print(inst)
        move1(ship_pos1, inst)
        move2(ship_pos2, wp_pos, inst)
        print('ship\t', ship_pos2)
        print('wp\t\t', wp_pos)
    print(f'Part 1: {abs(ship_pos1.x) + abs(ship_pos1.y)}')
    print(f'Part 2: {abs(ship_pos2.x) + abs(ship_pos2.y)}')
