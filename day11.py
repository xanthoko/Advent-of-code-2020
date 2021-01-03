import numpy as np
from typing import List

from utils import get_input_text_from_url


def get_input_list():
    input_text = get_input_text_from_url(11)
    str_input_list = input_text.split('\n')
    return str_input_list


def solve_1(seat_layout_list: List[str]):
    """Finds the number of occupied seats after the seat change has ended.

    The state of a seat is described by a character.
    '#': occupied
    'L': empty
    '.': floor

    In every round of changes the seats change their state according to the
    following rules:
        - If a seat is empty and there are no occupied seats adjacent to it, the
          seat becomes occupied.
        - If a seat is occupied and four or more seats adjacent to it are also
          occupied, the seat becomes empty.
        - Otherwise, the seat's state does not change.

    After a number of rounds there will be no changes.

    Args:
        seat_input_list (list of strings): ['L.L.LLLL.L', 'L...LLL..L', ]
    Returns:
        integer: The occupied seats
    """
    # convert to numpy 2d array
    seat_2d_list = [[x for x in row] for row in seat_layout_list]
    # seat_2d_list = [['L', '.', 'L', ...], ]
    seat_layout_array = np.array(seat_2d_list)

    last_layout_array = seat_layout_array
    while True:
        updated_layout_array = _get_updated_seat_layout(last_layout_array)
        # terminate when the two arrays are equal
        if np.array_equal(updated_layout_array, last_layout_array):
            break

        last_layout_array = updated_layout_array

    return _get_occupied_seats(updated_layout_array)


def _get_updated_seat_layout(seat_layout_array):
    """Returns an updated seat layout array.

    Args:
        seat_layout_array (np.array): 2d array
    Returns:
        np.array: The update layout array
    """
    # the changes are made to a copy, because we want to update the array after
    # ALL the changes have taken place
    updated_layout_array = seat_layout_array.copy()
    rows, cols = seat_layout_array.shape
    # O(n * m)
    for row in range(rows):
        for col in range(cols):
            updated_seat = _get_updated_seat(seat_layout_array, row, col)
            updated_layout_array[row, col] = updated_seat
    return updated_layout_array


def _get_updated_seat(seat_layout_array, row: int, col: int):
    """Returns the updated seat value."""
    row_min = max(0, row - 1)
    col_min = max(0, col - 1)
    # we do not need to enforce limits for the max values because in numpy
    # index > len(rows) equals with index = len(rows)
    neighbourhood = seat_layout_array[row_min:row + 2, col_min:col + 2]
    # numpy unique is O(n logn), however n = 3 so its small
    seat_count = dict(zip(*np.unique(neighbourhood, return_counts=True)))

    seat = seat_layout_array[row, col]
    # we must reduce the count of the seat symbol because we want only the count
    # of the adjacent seats
    seat_count[seat] -= 1

    # apply the rules
    if seat == 'L' and not seat_count.get('#', 0):
        return '#'
    elif seat == '#' and seat_count.get('#', 0) > 3:
        return 'L'
    else:
        # seat's state does not change
        return seat


def _get_occupied_seats(seat_layout_array):
    seat_count = dict(zip(*np.unique(seat_layout_array, return_counts=True)))
    return seat_count.get('#', 0)


def _print_layout(seat_layout_array):
    """Prints the numpy array as a joined string"""
    seat_layout_list = seat_layout_array.tolist()
    s = [''.join(x) for x in seat_layout_list]
    print('\n'.join(s))


def solve():
    seat_layout_list = get_input_list()

    # PART 1
    occupied_seats = solve_1(seat_layout_list)
    print(f'[PART 1] {occupied_seats} occupied seats')


if __name__ == '__main__':
    solve()
