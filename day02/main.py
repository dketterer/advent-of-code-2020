if __name__ == '__main__':
    part1 = False

    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    print(f'len input: {len(lines)}')

    tuples = []

    for line in lines:
        part = line.split()
        lower = int(part[0].split('-')[0])
        upper = int(part[0].split('-')[1])
        char = part[1].rstrip(':')
        pw = part[2]

        tuples.append((lower, upper, char, pw))

    valids = 0

    for tup in tuples:
        lower, upper, char, pw = tup
        if part1:
            if lower <= pw.count(char) <= upper:
                valids += 1
        else:
            if bool(pw[lower - 1] == char) != bool(pw[upper - 1] == char):
                valids += 1
    print(valids)
