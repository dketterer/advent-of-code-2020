if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    bpasses = [(line[:7], line[7:]) for line in lines]

    rows = [int(bpass[0].replace('F', '0').replace('B', '1'), 2) for bpass in bpasses]
    cols = [int(bpass[1].replace('L', '0').replace('R', '1'), 2) for bpass in bpasses]
    seat_ids = [(row * 8) + col for row, col in zip(rows, cols)]
    print(f'Part 1: {max(seat_ids)}')
    seat_ids.sort()
    last = seat_ids.pop(0)
    while seat_ids:
        i = seat_ids.pop(0)
        if last + 1 != i and last + 2 == i:
            print(f'Part 2: {last + 1}')
            break
        last = i
