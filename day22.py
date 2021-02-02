from typing import List

from utils import get_input_text


def get_input():
    input_text = get_input_text(22)
    deck_1_str, deck_2_str = input_text.split('\n\n')
    deck_1_splitted = deck_1_str.split('\n')
    deck_2_splitted = deck_2_str.split('\n')
    p1_deck = list(map(int, deck_1_splitted[1:]))
    p2_deck = list(map(int, deck_2_splitted[1:]))

    return p1_deck, p2_deck


def solve1(p1_deck: List[int], p2_deck: List[int]):
    while len(p1_deck) and len(p2_deck):
        p1_card = p1_deck.pop(0)
        p2_card = p2_deck.pop(0)

        if p1_card > p2_card:
            p1_deck.extend([p1_card, p2_card])
        elif p1_card < p2_card:
            p2_deck.extend([p2_card, p1_card])

    if p1_deck:
        return _get_score(p1_deck)
    else:
        return _get_score(p2_deck)


def solve2(p1_deck: List[int], p2_deck: List[int]):
    _, winning_deck = _play_game(p1_deck, p2_deck)
    return _get_score(winning_deck)


def _play_game(p1_deck: List[int], p2_deck: List[int]):
    previous_rounds = set()
    while len(p1_deck) and len(p2_deck):
        round_key = tuple(p1_deck), tuple(p2_deck)

        if round_key in previous_rounds:
            return 1, p1_deck

        previous_rounds.add(round_key)

        p1_card = p1_deck.pop(0)
        p2_card = p2_deck.pop(0)

        if len(p1_deck) >= p1_card and len(p2_deck) >= p2_card:
            sub_p1_deck = p1_deck.copy()[:p1_card]
            sub_p2_deck = p2_deck.copy()[:p2_card]
            winner, _ = _play_game(sub_p1_deck, sub_p2_deck)
        else:
            if p1_card > p2_card:
                winner = 1
            elif p1_card < p2_card:
                winner = 2

        if winner == 1:
            p1_deck.extend([p1_card, p2_card])
        else:
            p2_deck.extend([p2_card, p1_card])

    if p1_deck:
        return 1, p1_deck
    else:
        return 2, p2_deck


def _get_score(deck: List[int]):
    score = 0
    for i, el in enumerate(reversed(deck)):
        score += el * (i + 1)
    return score


def solve():
    p1_deck, p2_deck = get_input()

    # PART 1
    winning_score_1 = solve1(p1_deck.copy(), p2_deck.copy())
    print(f'[PART 1] The score is {winning_score_1}')

    # PART 2
    winning_score_2 = solve2(p1_deck, p2_deck)
    print(f'[PART 2] The score is {winning_score_2}')


if __name__ == '__main__':
    solve()
