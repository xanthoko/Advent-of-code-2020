import numpy as np
from math import prod
from collections import defaultdict, Counter

from utils import get_input_text, get_example_input_text


def get_input_list():
    input_text = get_input_text(20)
    # input_text = get_example_input_text()

    full_tiles = input_text.split('\n\n')
    tiles = {}
    for full_tile in full_tiles:
        splited_tile = full_tile.split('\n')
        tile_id = splited_tile[0].split(' ')[1][:-1]
        tile_array = np.array([[x for x in row] for row in splited_tile[1:]])
        tiles[int(tile_id)] = tile_array
    return tiles


def solve1(tiles: dict):
    tile_edges = _get_tile_edges(tiles)
    # get lonely edges (do not belong to more than 1 tile)
    lonely_edges = {x: v for x, v in tile_edges.items() if len(v) == 1}
    lonely_tile_ids = [v[0] for k, v in lonely_edges.items()]
    ltc = Counter(lonely_tile_ids)
    # corner tiles must have 4 lonely edges (2 normal and 2 reversed)
    corner_tile_ids = [key for key in ltc if ltc[key] == 4]
    return prod(corner_tile_ids)


def _get_tile_edges(tiles: dict):
    tile_edges = defaultdict(list)
    for tile_id, tile in tiles.items():
        edge1_str = ''.join([x for x in tile[0, :]])  # first row
        edge1_rv_str = edge1_str[::-1]
        edge2_str = ''.join([x for x in tile[:, 0]])  # first col
        edge2_rv_str = edge2_str[::-1]
        edge3_str = ''.join([x for x in tile[-1, :]])  # last row
        edge3_rv_str = edge3_str[::-1]
        edge4_str = ''.join([x for x in tile[:, -1]])  # last col
        edge4_rv_str = edge4_str[::-1]

        tile_edges[edge1_str].append(tile_id)
        tile_edges[edge1_rv_str].append(tile_id)
        tile_edges[edge2_str].append(tile_id)
        tile_edges[edge2_rv_str].append(tile_id)
        tile_edges[edge3_str].append(tile_id)
        tile_edges[edge3_rv_str].append(tile_id)
        tile_edges[edge4_str].append(tile_id)
        tile_edges[edge4_rv_str].append(tile_id)
    return tile_edges


def solve2(tiles: dict):
    not_used_tiles = list(tiles.keys())
    rows = []
    # row_ids = []
    r = 0
    while not_used_tiles:
        if r == 2:
            break
        row, not_used_tiles = _get_filled_row(tiles, not_used_tiles)
        # print(not_used_tiles)
        rows.append(row)
        # print(row.shape)
        if r == 1:
            _print(row)
        print(row.shape)
        print('===')
        # print('adssad')
        r += 1


def _get_filled_row(tiles, not_used_tiles):
    row = tiles[not_used_tiles[0]]
    print(not_used_tiles[0])
    not_used_tiles = not_used_tiles[1:]  # remove first tile
    row, not_used_tiles, row_ids = _fill_to_the_right(tiles, not_used_tiles, row)
    # row = np.flip(row, 1)
    # print('flip')
    # row, not_used_tiles, row_ids2 = _fill_to_the_right(tiles, not_used_tiles, row)
    # print(row_ids + row_ids2)
    return row, not_used_tiles


def _fill_to_the_right(tiles, not_used_tiles, row):
    w = np.array(['|'] * 10)
    w = np.reshape(w, (10, 1))
    row_ids = []
    while True:
        for tile_id in not_used_tiles:
            check_tile = tiles[tile_id]
            neighbor = _get_right_neighbor(row, check_tile)
            if neighbor is not None:
                # if tile_id == 1847:
                # _print(row)
                # print('das---das')
                # _print(neighbor)
                # row = np.concatenate((row, w), axis=1)
                row = np.concatenate((row, neighbor), axis=1)
                row_ids.append(tile_id)
                not_used_tiles.remove(tile_id)
                break
        else:
            break
    return row, not_used_tiles, row_ids


def _get_right_neighbor(tile1: np.array, tile2: np.array):
    tile1_edge = list(tile1[:, -1])
    tile2_left_edge = list(tile2[:, 0])
    tile2_right_edge = list(tile2[:, -1])
    tile2_top_edge = list(tile2[0, :])
    tile2_bot_edge = list(tile2[-1, :])

    if tile1_edge == tile2_left_edge:
        return tile2
    elif tile1_edge == tile2_left_edge[::-1]:
        return np.flip(tile2, 0)  # flip in x axis
    elif tile1_edge == tile2_right_edge:
        return np.flip(tile2, 1)  # flip in y axis
    elif tile1_edge == tile2_right_edge[::-1]:
        return np.flip(tile2, (0, 1))  # flip in both axis
    elif tile1_edge == tile2_top_edge:
        return np.flip(np.rot90(tile2, 1), 0)
    elif tile1_edge == tile2_top_edge[::-1]:
        return np.rot90(tile2, 0)
    elif tile1_edge == tile2_bot_edge:
        return np.rot90(tile2, 3)
    elif tile1_edge == tile2_bot_edge[::-1]:
        return np.flip(np.rot90(tile2, 3), 0)
    else:
        return


def _print(tile):
    str_rows = [''.join(list(x)) for x in tile]
    print('\n'.join(str_rows))


def solve():
    tiles = get_input_list()

    # PART 1
    # multiplied_edges = solve1(tiles)
    # print(f'[PART 1] The multiplied edges are {multiplied_edges}')

    # PART 2
    non_sea_monster = solve2(tiles)
    # print(f'[PART 2] {non_sea_monster} # are not part of a monster')


if __name__ == '__main__':
    solve()
    pass
