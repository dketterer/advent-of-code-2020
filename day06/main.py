if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    sum1 = 0
    sum2 = 0
    everyone = []
    anyone = set()
    for line in lines:
        if not line:
            sum2 += len(set.intersection(*everyone))
            everyone = []
            sum1 += len(anyone)
            anyone = set()
        else:
            answers = set()
            for char in line:
                answers.add(char)
                anyone.add(char)
            everyone.append(answers)
    sum1 += len(anyone)
    sum2 += len(set.intersection(*everyone))

    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')


