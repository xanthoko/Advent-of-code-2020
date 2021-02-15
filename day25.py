from utils import get_input_text, get_example_input_text
from time import time


def get_input():
    input_text = get_input_text(25)
    # input_text = get_example_input_text()

    return map(int, input_text.split('\n'))


def solve1(card_pub: int, door_pub: int) -> int:
    generated_key, loop_size = _get_loop_size(7, door_pub, card_pub)

    if generated_key == door_pub:
        encryption_key = _get_key(card_pub, loop_size)
    else:
        encryption_key = _get_key(door_pub, loop_size)

    return encryption_key


def _get_loop_size(subject_number: int, wanted_key_1: int, wanted_key_2: int):
    loop_size = 0
    value = 1
    while value != wanted_key_1 and value != wanted_key_2:
        loop_size += 1
        value = (value * 7) % 20201227
    return value, loop_size


def _get_key(subject_number: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


def solve2():
    pass


def solve():
    card_pub, door_pub = get_input()

    # PART 1
    ecryption_key = solve1(card_pub, door_pub)
    print(f'[PART 1] The encryption key is {ecryption_key}')


if __name__ == '__main__':
    solve()
