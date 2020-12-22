from copy import deepcopy

import numpy as np


def normal_game(player1, player2):
    while player1 and player2:
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])


def play_rec(player1, player2):
    seen = {}
    while player1 and player2:
        if tuple(player1 + [-1] + player2) in seen:
            # win for player1
            player1.extend(player2)
            return
        else:
            seen[tuple(player1 + [-1] + player2)] = True
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if len(player1) >= card1 and len(player2) >= card2:
            recursive_player1 = deepcopy(player1[:card1])
            recursive_player2 = deepcopy(player2[:card2])
            play_rec(recursive_player1, recursive_player2)
            if len(recursive_player1) > len(recursive_player2):
                player1.extend([card1, card2])
            else:
                player2.extend([card2, card1])
        else:
            if card1 > card2:
                player1.extend([card1, card2])
            else:
                player2.extend([card2, card1])


def calc_score(player1, player2):
    winning_deck = player1 if player1 else player2
    return np.arange(1, len(winning_deck) + 1, 1)[::-1].dot(np.array(winning_deck))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    orig_player1 = []
    orig_player2 = []
    for i, line in enumerate(lines):
        if line.startswith('Player') or not line:
            continue
        if i < len(lines) // 2:
            orig_player1.append(int(line))
        else:
            orig_player2.append(int(line))

    # Part 1
    player1 = deepcopy(orig_player1)
    player2 = deepcopy(orig_player2)
    normal_game(player1, player2)
    print(f'Part 1: {calc_score(player1, player2)}')

    # Part 2
    player1 = deepcopy(orig_player1)
    player2 = deepcopy(orig_player2)

    play_rec(player1, player2)
    print(f'Part 2: {calc_score(player1, player2)}')
