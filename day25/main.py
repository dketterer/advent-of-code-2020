def transform(inp, subj=7, mod=20201227):
    return (subj * inp) % mod


def full_transform(subject, loop, mod=20201227):
    val = 1
    for _ in range(loop):
        val = (val * subject) % mod
    return val


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    pub_key1 = int(lines[0])
    pub_key2 = int(lines[1])

    target1 = 1
    private1 = 0
    while True:
        private1 += 1
        target1 = transform(target1)
        if target1 == pub_key1:
            break
    enc_key = full_transform(pub_key2, private1)

    print(f'Part 1: {enc_key}')
