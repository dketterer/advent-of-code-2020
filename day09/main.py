import itertools

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    cypher = [int(line.strip()) for line in lines]

    relevant_length = 25

    for i in range(len(cypher) - relevant_length):
        combinations = map(lambda t: sum(t), itertools.combinations(cypher[i:i + relevant_length], 2))
        if cypher[i + relevant_length] not in combinations:
            invalid = cypher[i + relevant_length]
            print(f"Part 1: {invalid}")
            break

    for current_start in range(len(cypher)):
        current_list = []
        for i, val in enumerate(cypher[current_start:]):
            current_list.append(val)
            if sum(current_list) == invalid:
                print(f'Part 2: {min(current_list) + max(current_list)}')
                exit(0)
