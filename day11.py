import numpy as np
from typing import List

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(11)
    str_input_list = input_text.split('\n')
    return str_input_list


def get_occupied_seats(seat_layout_list: List[str], part: int):
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
        part (integer)
    Returns:
        integer: The occupied seats
    """
    # convert to numpy 2d array
    seat_2d_list = [[x for x in row] for row in seat_layout_list]
    # seat_2d_list = [['L', '.', 'L', ...], ]
    seat_layout_array = np.array(seat_2d_list)

    last_layout_array = seat_layout_array
    while True:
        if part == 1:
            updated_layout_array = _get_updated_seat_layout_1(last_layout_array)
        elif part == 2:
            updated_layout_array = _get_updated_seat_layout_2(last_layout_array)

        # terminate when the two arrays are equal
        if np.array_equal(updated_layout_array, last_layout_array):
            break

        last_layout_array = updated_layout_array

    return _get_occupied_seats_from_layout(updated_layout_array)


def _get_updated_seat_layout_1(seat_layout_array):
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
            updated_seat = _get_updated_seat_1(seat_layout_array, row, col)
            updated_layout_array[row, col] = updated_seat
    return updated_layout_array


def _get_updated_seat_1(seat_layout_array, row: int, col: int):
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


def _get_updated_seat_layout_2(seat_layout_array):
    """Finds the neighboor count of each seat and updates the layout.

    Args:
        seat_layout_array (numpy.array)
    """
    rows, cols = seat_layout_array.shape
    # tuple of tuples of the coordinates of the free and occupied seats
    free_seats = tuple(zip(*np.where(seat_layout_array == 'L')))
    occupied_seats = tuple(zip(*np.where(seat_layout_array == '#')))

    # a dictionary with (index: is_occupied) pairs
    seat_ids = {_to_index(x, cols): 0 for x in free_seats}
    seat_ids.update({_to_index(x, cols): 1 for x in occupied_seats})

    # pairs of {seat_id: number_of_neighboors}
    neighboor_count = {k: 0 for k in seat_ids.keys()}

    for row in range(rows):
        min_row_index = _to_index((row, 0), cols)
        max_row_index = _to_index((row, cols), cols)
        row_keys = [
            k for k, v in seat_ids.items() if min_row_index <= k < max_row_index
        ]
        _update_neighbour_count_of_same_keys(neighboor_count, seat_ids, row_keys)

    for col in range(cols):
        col_keys = [k for k, v in seat_ids.items() if k % cols == col]
        _update_neighbour_count_of_same_keys(neighboor_count, seat_ids, col_keys)

    for diag_1 in range(-rows + 1, rows):
        if diag_1 < 0:
            main_diag_keys = [
                k for k, v in seat_ids.items() if k % (cols + 1) == (cols + 1) +
                diag_1 and not _is_below_main_diag(k, cols)
            ]
        else:
            main_diag_keys = [
                k for k, v in seat_ids.items()
                if k % (cols + 1) == diag_1 and _is_below_main_diag(k, cols)
            ]
        _update_neighbour_count_of_same_keys(neighboor_count, seat_ids,
                                             main_diag_keys)

    for diag2 in range(-rows + 1, rows):
        if diag2 < 0:
            sec_diag_keys = [
                k for k, v in seat_ids.items() if k % (cols - 1) == (cols - 1) +
                diag2 and not _is_below_sec_diag(k, cols)
            ]
        else:
            sec_diag_keys = [
                k for k, v in seat_ids.items()
                if k % (cols - 1) == diag2 and _is_below_sec_diag(k, cols)
            ]
        _update_neighbour_count_of_same_keys(neighboor_count, seat_ids,
                                             sec_diag_keys)

    updated_layout_array = seat_layout_array.copy()
    for index, ncount in neighboor_count.items():
        coords = _to_coords(index, cols)
        if seat_ids[index] == 0 and ncount == 0:
            updated_layout_array[coords] = '#'
        if seat_ids[index] == 1 and ncount >= 5:
            updated_layout_array[coords] = 'L'

    return updated_layout_array


def _update_neighbour_count_of_same_keys(neighboor_count: dict, seat_ids: dict,
                                         keys: List[int]):
    """Updates the count of the occupied neighboors for each of the keys.

    For example if the keys are [1,2,3] and seat_ids = {1:1, 2:0, 3:1} after the
    iterations the neighboor count of seat with index 2 is increased by 2, while
    the other 2 keys are not affected (because they have 1 empty seat neighboor)
    """
    keys.sort()
    for ind, key in enumerate(keys):
        if not ind:
            # first key has no left neighboor
            prev_seat = None
        else:
            prev_seat_key = keys[ind - 1]
            prev_seat = seat_ids[prev_seat_key]
        if ind == len(keys) - 1:
            # last key has no right neighboor
            next_seat = None
        else:
            next_seat_key = keys[ind + 1]
            next_seat = seat_ids[next_seat_key]

        neighboor_count[key] += (int(next_seat == 1) + int(prev_seat == 1))


def _to_index(coords: List[int], cols: int):
    """Converts 2D coords to 1d index.

    The formula used for input (x,y) and matrix NxN is
    index = x * N + y
    """
    row, col = coords
    return row * cols + col


def _to_coords(index: int, cols: int):
    """Converts the index to 2D coords.

    The x coordinate is the quotient and the y the remained of the
    division index / cols
    """
    return divmod(index, cols)


def _is_below_main_diag(index: int, cols: int):
    """Returns if the element with the given index is below the main primary
    diagonal."""
    x, y = divmod(index, cols)
    return y >= x


def _is_below_sec_diag(index: int, cols: int):
    """Returns if the element with the given index is below the secondary
    diagonal."""
    x, y = divmod(index, cols)
    return y >= -x + cols - 1


def _get_occupied_seats_from_layout(seat_layout_array):
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
    occupied_seats_1 = get_occupied_seats(seat_layout_list, 1)
    print(f'[PART 1] {occupied_seats_1} occupied seats')

    # PART 2
    occupied_seats_2 = get_occupied_seats(seat_layout_list, 2)
    print(f'[PART 2] {occupied_seats_2} occupied seats')


if __name__ == '__main__':
    solve()
