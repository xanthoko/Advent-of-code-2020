import numpy as np
from typing import List

from utils import get_input_text


def get_input_list():
    """Returns the grid as a list of lists."""
    input_text = get_input_text(17)

    rows = input_text.split('\n')
    input_2d_list = [[x for x in row] for row in rows]

    return input_2d_list


def solve1(input_2d_list: List[List[str]]):
    """Returns the number of active cubes in the 3d grid after 6 cycles."""
    grid = _get_initialized_3d_array(input_2d_list)

    for cycle in range(6):
        print(f'Cycle {cycle}')
        updated_grid = grid.copy()
        y, x, z = grid.shape
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    element = grid[i, j, k]
                    # find neighborhood
                    x_min = max(0, i - 1)
                    x_max = i + 2
                    y_min = max(0, j - 1)
                    y_max = j + 2
                    z_min = max(0, k - 1)
                    z_max = k + 2
                    neighborhood = grid[x_min:x_max, y_min:y_max, z_min:z_max]
                    # check activity
                    activity_count = dict(
                        zip(*np.unique(neighborhood, return_counts=True)))
                    activity_count[element] -= 1  # remove the current element
                    # apply rules
                    if element == 1 and activity_count.get(1, 0) not in [2, 3]:
                        updated_grid[i, j, k] = 0
                    elif element == 0 and activity_count.get(1, 0) == 3:
                        updated_grid[i, j, k] = 1
        # update grid
        grid = updated_grid.copy()

    activity_count = dict(zip(*np.unique(grid, return_counts=True)))
    return activity_count.get(1, 0)


def _get_initialized_3d_array(input_2d_list: List[List[str]]):
    """Returns a 3d array of the grid in its initial state.

    '.' -> 0
    '#' -> 1
    """
    rows = len(input_2d_list)
    grid_size = rows + 15  # NOTE: arbitrary
    # the initial state is in the middle of the grid
    offset_indexes = grid_size // 2 - 1

    grid = np.zeros(shape=(grid_size, grid_size, grid_size), dtype=np.int8)

    for i in range(rows):
        for j in range(rows):
            if input_2d_list[i][j] == '#':
                grid[i + offset_indexes, j + offset_indexes, offset_indexes] = 1
    return grid


def solve2(input_2d_list: List[List[str]]):
    """Returns the number of active cubes in the 4d grid after 6 cycles."""
    grid = _get_initialized_4d_array(input_2d_list)

    for cycle in range(6):
        print(f'Cycle: {cycle}')
        updated_grid = grid.copy()
        y, x, z, w = grid.shape
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    for m in range(w):
                        element = grid[i, j, k, m]
                        # find neighborhood
                        x_min = max(0, i - 1)
                        x_max = i + 2
                        y_min = max(0, j - 1)
                        y_max = j + 2
                        z_min = max(0, k - 1)
                        z_max = k + 2
                        w_min = max(0, m - 1)
                        w_max = m + 2
                        neighborhood = grid[x_min:x_max, y_min:y_max, z_min:z_max,
                                            w_min:w_max]
                        # check activity
                        activity_count = dict(
                            zip(*np.unique(neighborhood, return_counts=True)))
                        activity_count[element] -= 1  # remove the current element
                        # apply rules
                        if element == 1 and activity_count.get(1, 0) not in [2, 3]:
                            updated_grid[i, j, k, m] = 0
                        elif element == 0 and activity_count.get(1, 0) == 3:
                            updated_grid[i, j, k, m] = 1
        # update grid
        grid = updated_grid.copy()

    activity_count = dict(zip(*np.unique(grid, return_counts=True)))
    return activity_count.get(1, 0)


def _get_initialized_4d_array(input_2d_list: List[List[str]]):
    """Returns a 3d array of the grid in its initial state.

    '.' -> 0
    '#' -> 1
    """
    rows = len(input_2d_list)
    grid_size = rows * 4  # NOTE: arbitrary
    offset_indexes = grid_size // 2 - 1

    grid = np.zeros(shape=(grid_size, grid_size, grid_size, grid_size),
                    dtype=np.int8)

    for i in range(rows):
        for j in range(rows):
            if input_2d_list[i][j] == '#':
                grid[i + offset_indexes, j + offset_indexes, offset_indexes,
                     offset_indexes] = 1
    return grid


def solve():
    input_list = get_input_list()

    # PART 1
    active_cubes_1 = solve1(input_list)
    print(f'[PART 1] {active_cubes_1} active cubes')

    # PART 2
    active_cubes_2 = solve2(input_list)
    print(f'[PART 2] {active_cubes_2} active cubes')


if __name__ == '__main__':
    solve()
