if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    seat_ids = [int(line.strip().replace('L', '0').replace('R', '1').replace('F', '0').replace('B', '1'), 2) for line in lines]
    seat_ids.sort()
    print(f'Part 1: {seat_ids[-1]}')

    last = seat_ids.pop(0)
    while seat_ids:
        i = seat_ids.pop(0)
        if last + 1 != i and last + 2 == i:
            print(f'Part 2: {last + 1}')
            break
        last = i
