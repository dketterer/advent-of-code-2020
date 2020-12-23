import math


class Cup:
    def __init__(self, val, succ=None):
        self.val: int = val
        self.succ: Cup = succ

    def __next__(self):
        return self.succ

    def __iter__(self):
        pointer = self
        while True:
            yield pointer
            pointer = next(pointer)
            if self == pointer:
                break

    def __getitem__(self, item):
        if type(item) == slice:
            item: slice
            pointer = self
            l = []
            for _ in range(item.start):
                pointer = next(pointer)
            for _ in range(item.stop - item.start):
                l.append(pointer)
                pointer = next(pointer)
            return l
        else:
            raise NotImplemented

    def get_pick_up(self):
        return [self.succ, self.succ.succ, self.succ.succ.succ]

    def get_by_val(self, val):
        for cup in self:
            if cup.val == val:
                return cup


def make_game(init):
    by_val = {}
    head = Cup(init[0])
    by_val[init[0]] = head
    pointer = head
    for val in init[1:]:
        new = Cup(val)
        by_val[val] = new
        pointer.succ = new
        pointer = new
    pointer.succ = head
    return head, by_val


def crab_move_ll(curr: Cup, length, by_val, verbose):
    pick_up = curr.get_pick_up()
    pick_up_val = [c.val for c in pick_up]
    if verbose:
        print(f"pick up: {pick_up_val}")
    for offset in range(1, length):
        dest_val = (curr.val - offset) % (length + 1)
        if dest_val != 0 and dest_val not in pick_up_val:
            break
    if verbose:
        print(f'destination: {dest_val}')

    dest = by_val[dest_val]
    curr.succ = pick_up[2].succ
    # insert pick up after destination
    tmp = dest.succ
    dest.succ = pick_up[0]
    pick_up[2].succ = tmp
    return curr.succ


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    verbose = False
    orig_cups = [int(char) for char in lines[0]]

    curr, by_val = make_game(orig_cups)
    for j in range(100):
        if verbose:
            print(f'-- move {j + 1} --')
            for i, c in enumerate(curr):
                if c.val == curr.val:
                    print(f'({c.val}) ', end='')
                else:
                    print(f'{c.val} ', end='')
            print()
        curr = crab_move_ll(curr, 9, by_val, verbose)

    one = by_val[1]
    print(f"Part 1: {''.join([str(c.val) for c in one[1:9]])}")

    cups = list(range(1, 1000001))
    cups[0:9] = orig_cups.copy()
    curr, by_val = make_game(cups)

    for k in range(10000000):
        curr = crab_move_ll(curr, 1000000, by_val, False)

    one = by_val[1]
    print(f"Part 2: {math.prod([c.val for c in one[1:3]])}")
