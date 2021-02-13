import re
import numpy as np
from typing import List, Tuple

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(24)

    return input_text.split('\n')


def solve1(tiles: List[str]) -> set:
    black_tiles = set()
    for tile in tiles:
        rexp = re.compile(r'e|w|se|sw|ne|nw')
        moves = rexp.findall(tile)

        tile_index = _get_tile_index(moves)
        if tile_index not in black_tiles:
            # white face is being flipped
            black_tiles.add(tile_index)
        else:
            # black face is being flipped
            black_tiles.remove(tile_index)
    return black_tiles


def _get_tile_index(moves: List[str]) -> Tuple[int, int]:
    DIR_COR_MAP = {
        'w': (-1, 0),
        'e': (1, 0),
        'ne': (0.5, -1),
        'nw': (-0.5, -1),
        'se': (0.5, 1),
        'sw': (-0.5, 1)
    }

    tile_x = 0
    tile_y = 0
    for move in moves:
        dx, dy = DIR_COR_MAP[move]
        tile_x += dx
        tile_y += dy

    return (tile_x, tile_y)


def solve2(tiles: List[str]):
    flipped = solve1(tiles)
    for day in range(100):
        fcopy = flipped.copy()
        col_limit = max([
            abs(min(flipped, key=lambda x: x[0])[0]),
            abs(max(flipped, key=lambda x: x[0])[0])
        ])
        row_limit = max([
            abs(min(flipped, key=lambda x: x[1])[1]),
            abs(max(flipped, key=lambda x: x[1])[1])
        ])
        limit = max(col_limit, row_limit) + 5
        for row in range(-limit, limit):
            # move bot left and bot right from row to row
            addon = -0.5 if row % 2 else 0
            for col in np.arange(-limit + addon, limit):
                tile = (col, row)
                neighbors = _get_neighbor_indexes(tile)
                black_neighbors = len(flipped.intersection(neighbors))
                is_tile_black = tile in flipped

                if is_tile_black and black_neighbors not in [1, 2]:
                    fcopy.remove(tile)
                elif not is_tile_black and black_neighbors == 2:
                    fcopy.add(tile)

        flipped = fcopy

    return flipped


def _get_neighbor_indexes(tile_index: tuple) -> List[tuple]:
    n1 = (tile_index[0] - 1, tile_index[1])  # w
    n2 = (tile_index[0] - 0.5, tile_index[1] - 1)  # nw
    n3 = (tile_index[0] + 0.5, tile_index[1] - 1)  # ne
    n4 = (tile_index[0] + 1, tile_index[1])  # e
    n5 = (tile_index[0] + 0.5, tile_index[1] + 1)  # se
    n6 = (tile_index[0] - 0.5, tile_index[1] + 1)  # sw
    return set([n1, n2, n3, n4, n5, n6])


def solve():
    tiles = get_input_list()

    # PART 1
    black_tiles_1 = solve1(tiles)
    print(f'[PART 1] {len(black_tiles_1)} tiles are black')

    # PART 2
    black_tiles_2 = solve2(tiles)
    print(f'[PART 2] {len(black_tiles_2)} tiles are black')


if __name__ == '__main__':
    solve()
