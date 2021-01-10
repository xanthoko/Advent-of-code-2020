from typing import List

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(15)
    str_input_list = input_text.split(',')
    return list(map(int, str_input_list))


def find_nth_number(numbers: List[int], n: int):
    """Finds the n-th number spoken.

    The rules are the following:
        - If the last spoken number has been spoken for the first time, the new
        number will be 0.
        - If the number has been spoken before, the current player announces how
        many turns apart the number is from when it was previously spoken.
    """
    turns = {number: ind for ind, number in enumerate(numbers)}
    index = len(turns)
    new_number = 0

    while index < n - 1:
        try:
            updated_number = index - turns[new_number]
        except KeyError:
            updated_number = 0
        turns[new_number] = index
        new_number = updated_number
        index += 1

    return new_number


def solve():
    numbers = get_input_list()

    # PART 1
    wanted_number_1 = find_nth_number(numbers, 2020)
    print(f'[PART 1] The 2020th number is {wanted_number_1}')

    # PART 2
    wanted_number_2 = find_nth_number(numbers, 30000000)
    print(f'[PART 2] The 30000000th number is {wanted_number_2}')


if __name__ == '__main__':
    solve()
