import itertools
import numpy as np

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    numbers = [int(line.strip()) for line in lines]

    combos = itertools.combinations(numbers, 3)

    for comb in combos:
        if np.sum(comb) == 2020:
            print(comb)
            print(np.prod(comb))
            break
