from math import prod
from utils import get_input_text


def get_input_list():
    """Returns list of integers"""
    input_text = get_input_text(1)
    splited_str_input_list = input_text.split('\n')
    input_list = list(map(int, splited_str_input_list))
    return input_list


def get_two_wanted_numbers(input_list):
    """Returns the two numbers of the list that sum up to 2020."""
    # O(n^2)
    for i in range(len(input_list)):
        for j in range(i + 1, len(input_list)):
            n1 = input_list[i]
            n2 = input_list[j]
            if n1 + n2 == 2020:
                return n1, n2
    return ()


def get_three_wanted_numbers(input_list):
    """Returns the three numbers of the list that sum up to 2020."""
    # O(n^3)
    for i in range(len(input_list)):
        for j in range(i + 1, len(input_list)):
            for k in range(1 + 2, len(input_list)):
                n1 = input_list[i]
                n2 = input_list[j]
                n3 = input_list[k]
                if n1 + n2 + n3 == 2020:
                    return n1, n2, n3
    return ()


def get_numbers_multiplied(wanted_numbers):
    return prod(wanted_numbers)


def solve():
    input_list = get_input_list()

    # PART 1
    two_wanted_numbers = get_two_wanted_numbers(input_list)
    multiplied = get_numbers_multiplied(two_wanted_numbers)
    s = f'The numbers are {two_wanted_numbers} and the result is {multiplied}'
    print(s)

    # PART 2
    three_wanted_numbers = get_three_wanted_numbers(input_list)
    multiplied = get_numbers_multiplied(three_wanted_numbers)
    s = f'The numbers are {three_wanted_numbers} and the result is {multiplied}'
    print(s)


if __name__ == '__main__':
    solve()
