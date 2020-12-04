import numpy as np
import re


def validate(line, required_fields):
    parts = line.split(' ')
    found = set()
    d = {}

    part1 = 0
    part2 = 0
    for part in parts:
        key, *value = part.split(':')
        value = value[0] if value else ''
        found.add(key)
        d[key] = value
    if set(required_fields).issubset(found):
        part1 = 1
        part2 = 1
        try:
            if not (len(d['byr']) == 4 and 1920 <= int(d['byr']) <= 2002):
                part2 = 0
            if not (len(d['iyr']) == 4 and 2010 <= int(d['iyr']) <= 2020):
                part2 = 0
            if not (len(d['eyr']) == 4 and 2020 <= int(d['eyr']) <= 2030):
                part2 = 0
            if d['hgt'][-2:] == 'cm' and 150 <= int(d['hgt'][:-2]) <= 193:
                pass
            elif d['hgt'][-2:] == 'in' and 59 <= int(d['hgt'][:-2]) <= 76:
                pass
            else:
                part2 = 0
            if not (re.match("^#[0-9A-Fa-f]{6}$", d['hcl'])):
                part2 = 0
            if not (d['ecl'] in 'amb blu brn gry grn hzl oth'.split(' ')):
                part2 = 0
            if not (re.match("^[0-9]{9}$", d['pid']) and int(d['pid']) > 0):
                part2 = 0
        except Exception as e:
            part2 = 0
    return part1, part2


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    grouped_lines = []
    curr_line = ''
    for line in lines:
        if line == '':
            grouped_lines.append(curr_line[:-1])
            curr_line = ''
        else:
            curr_line += line + ' '

    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    results = np.array([validate(line, required_fields) for line in grouped_lines])
    print(f'Part1: {sum(results[:, 0])}')
    print(f'Part2: {sum(results[:, 1])}')
