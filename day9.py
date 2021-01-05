from typing import List
from collections import deque

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(9)
    str_input_list = input_text.split('\n')
    input_list = list(map(int, str_input_list))
    return input_list


def find_XMAS_anomaly(input_list: List[int], preamble_len: int):
    """Finds the anomaly in the given XMAS encrypted input.

    The first {preamble_len} numbers of the input are the preamble. The next number
    must be a sum of two numbers inside the preamble. Then the {preamble_len + 1}th
    number replaces the first input of the preable and the process continues by
    checking the {preamble_len + 2}th number.

    We must find the number that does not follow this rule.
    """
    preamble_list = input_list[:preamble_len]
    holy_queue = deque(preamble_list)
    xmas_input = input_list[preamble_len:]

    index = 0
    # O(n * m) where n is the lenght of the input and m the length of the holy_queue
    while True:
        number = xmas_input[index]
        if not _is_sum_of_holy_queue(number, holy_queue):
            return number

        # update holy queue (append number and remove the first input)
        holy_queue.append(number)
        holy_queue.popleft()

        index += 1
    print('No anomaly found')


def _is_sum_of_holy_queue(number: int, holy_queue):
    # O(m) where m is the length of the holy_queue
    sum_dict = {}
    for ind, el in enumerate(holy_queue):
        # check if pair (el, number-el) exists
        if number - el in sum_dict:
            return True
        sum_dict[el] = ind
    return False


def find_encryption_weakness(input_list: List[int], anomaly: int):
    """Finds the weakness of the XMAS encryption.

    Finds a list of contiguous numbers that add up to the anomaly and returns
    the sum of the min and max elements of this list.

    Args:
        input_list (list of integer)
        anomaly (integer): The anomaly found in part 1
    """
    contiguous_list = _find_contiguous_list(input_list, anomaly)
    weakness = min(contiguous_list) + max(contiguous_list)
    return weakness


def _find_contiguous_list(input_list: List[int], anomaly: int):
    """Finds the list of contiguous numbers in the input list that sum
    up to the anomaly.

    The logic is that the contiguous list is extended with elements from the input
    list until the sum of them gets greater than the anomaly. In this case, the next
    iteration starts with the next number as the initial element of the contiguous
    list.

    Returns:
        list of integers: The list of numbers that sum up to the anomaly
    """
    # O(n^2) (I think) where n is the length of the input list
    primary_index = 0
    # -2 because of the secondary_index is primary_index + 1
    while primary_index < len(input_list) - 2:
        base_element = input_list[primary_index]
        contiguous_list = [base_element]

        secondary_index = primary_index + 1
        while True:
            contiguous_list.append(input_list[secondary_index])
            if (list_sum := sum(contiguous_list)) == anomaly:
                return contiguous_list
            elif list_sum > anomaly:
                break
            else:
                secondary_index += 1
                if secondary_index == len(input_list):
                    # secondary index out of input_list bounds
                    break
                    return
        primary_index += 1


def solve():
    input_list = get_input_list()

    # PART 1
    xmas_anomaly = find_XMAS_anomaly(input_list, 25)
    print(f'[PART 1] The anomaly is {xmas_anomaly}')

    # PART 2
    encryption_weakness = find_encryption_weakness(input_list, xmas_anomaly)
    print(f'[PART 2] The encryption weakness is {encryption_weakness}')


if __name__ == '__main__':
    solve()
