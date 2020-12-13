from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def find_bus(start_time, bus_ids):
    for bus_id in bus_ids:
        if start_time % bus_id == 0:
            return bus_id


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    my_start_time = int(lines[0])
    bus_ids = sorted([int(char) for char in lines[1].split(',') if char != 'x'])
    curr_start_time = my_start_time
    while True:
        bus_id = find_bus(curr_start_time, bus_ids)
        if bus_id:
            print(f'Part 1: {(curr_start_time - my_start_time) * bus_id}')
            break
        curr_start_time += 1

    n = []
    a = []
    for offset, char in enumerate(lines[1].split(',')):
        if char != 'x':
            n.append(int(char))
            a.append(offset * -1)
    print(f'Part 2: {chinese_remainder(n, a)}')
