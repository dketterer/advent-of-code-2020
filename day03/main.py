import numpy as np

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    numbers = []
    for line in lines:
        numbers.append([0 if char == '.' else 1 for char in line])

    start_field = np.array(numbers)
    start_field = start_field

    slopes = []
    # Right 1, down 1.
    slopes.append((np.arange(1, len(numbers)), np.arange(1, len(numbers))))
    # Right 3, down 1. (This is the slope you already checked.)
    slopes.append((np.arange(3, 3 * len(numbers), 3), np.arange(1, len(numbers), 1)))
    # Right 5, down 1.
    slopes.append((np.arange(5, 5 * len(numbers), 5), np.arange(1, len(numbers), 1)))
    # Right 7, down 1.
    slopes.append((np.arange(7, 7 * len(numbers), 7), np.arange(1, len(numbers), 1)))
    # Right 1, down 2.
    slopes.append((np.arange(1, len(numbers) // 2 + 1), np.arange(2, len(numbers), 2)))

    needed_width = 7 * len(numbers)
    start_width = len(numbers[0])
    repeat_times = (needed_width // start_width) + 1
    field = np.tile(start_field, repeat_times)

    trees = 1

    for slope in slopes:
        xs, ys = slope

        trees *= field[ys, xs].sum()

    part1 = field[slopes[1][1], slopes[1][0]].sum()
    print(f'Part1: {part1}')
    print(f'Part2: {trees}')
