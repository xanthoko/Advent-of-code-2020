import numpy as np
from math import prod
from collections import defaultdict, Counter

from utils import get_input_text, get_example_input_text


def get_input_list():
    input_text = get_input_text(20)
    input_text = get_example_input_text()

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


def solve2(tiles: dict):
    rows = []
    not_used_tiles = list(tiles.keys())


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


def solve():
    tiles = get_input_list()

    # PART 1
    # multiplied_edges = solve1(tiles)
    # print(f'[PART 1] The multiplied edges are {multiplied_edges}')

    # PART 2
    non_sea_monster = solve2(tiles)
    print(f'[PART 2] {non_sea_monster} # are not part of a monster')


if __name__ == '__main__':
    solve()
"""
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""