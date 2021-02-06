import numpy as np
from math import prod
from collections import defaultdict, Counter

from utils import get_input_text

MONSTER_PATTERN = ('                  # ', '#    ##    ##    ###',
                   ' #  #  #  #  #  #   ')


def get_input_list():
    input_text = get_input_text(20)

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
    corner_tile_ids = _get_corner_ids(tile_edges)
    return prod(corner_tile_ids)


def _get_tile_edges(tiles: dict):
    """Creates a dictionary that maps any edges and its reversed to a tile id."""
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


def _get_corner_ids(tile_edges: dict):
    """Gets the ids of the corner edges."""
    # lonely_edges = {x: v for x, v in tile_edges.items() if len(v) == 1}
    lonely_tile_ids = [v[0] for k, v in tile_edges.items() if len(v) == 1]
    ltc = Counter(lonely_tile_ids)
    # corner tiles must have 4 lonely edges (2 normal and 2 reversed)
    return [key for key in ltc if ltc[key] == 4]


def solve2(tiles: dict):
    tile_edges = _get_tile_edges(tiles)
    corner_ids = _get_corner_ids(tile_edges)

    number_of_rows = int(len(tiles)**0.5)
    np_image = None

    first_of_row_id = corner_ids[0]
    first_of_row = tiles[first_of_row_id]

    tiles_used = set()
    for _ in range(number_of_rows):
        # intialize row
        row = first_of_row
        tiles_used.add(first_of_row_id)

        while True:
            right_edge_of_row = ''.join(list(row[:, -1]))
            connected_to_right_edge = tile_edges[right_edge_of_row]
            try:
                neighbor_id = [
                    x for x in connected_to_right_edge if x not in tiles_used
                ][0]
                neighbor = tiles[neighbor_id]
                neighbor = _get_right_neighbor(row, neighbor)
                # update row to the right
                row = np.concatenate((row, neighbor), axis=1)
                tiles_used.add(neighbor_id)
            except IndexError:
                # row done
                break

        # update image with the filled row
        if np_image is None:
            np_image = row
        else:
            np_image = np.concatenate((np_image, row), axis=0)

        # find the bottom neighbor of the first tile in the row
        bot_edge_of_first = ''.join(list(first_of_row[-1, :]))
        connected_to_first = tile_edges[bot_edge_of_first]
        try:
            bot_neighbor = [x for x in connected_to_first
                            if x != first_of_row_id][0]
        except IndexError:
            # no other bot neighbors. All rows done
            break
        # update the details of the first tile of the next row
        first_of_row_id = bot_neighbor
        first_of_row = _get_down_neighbor(first_of_row, tiles[bot_neighbor])

    np_image = _remove_tile_borders(np_image)
    str_image = '\n'.join([''.join(list(x)) for x in np_image])
    number_of_monsters = _count_pattern(np_image, MONSTER_PATTERN)

    water_in_image = str_image.count('#')
    water_in_the_monster = sum([x.count('#') for x in MONSTER_PATTERN])
    water_in_all_monsters = water_in_the_monster * number_of_monsters
    return water_in_image - water_in_all_monsters


def _remove_tile_borders(image: np.array):
    """Removes the boreders of the tiles that compose the image."""
    number_of_rows = image.shape[0] // 10
    ind_to_delete = []
    for i in range(number_of_rows):
        # first(0) and last(9) col/row of each tile
        ind_to_delete.extend([i * 10, i * 10 + 9])

    for i, ind in enumerate(ind_to_delete):
        # -i: the rows/cols that have already been deleted
        image = np.delete(image, ind - i, 1)
        image = np.delete(image, ind - i, 0)
    return image


def _count_pattern(image, pattern):
    pattern_h, pattern_w = len(pattern), len(pattern[0])
    image_sz = image.shape[0]
    deltas = set()

    for r, row in enumerate(pattern):
        for c, cell in enumerate(row):
            if cell == '#':
                deltas.add((r, c))

    for img in _arrangements(image):
        n = 0
        for r in range(image_sz - pattern_h):
            for c in range(image_sz - pattern_w):
                if all(img[r + dr][c + dc] == '#' for dr, dc in deltas):
                    n += 1

        if n != 0:
            return n


def _arrangements(tile):
    yield from _orientations(tile)
    yield from _orientations(np.flip(tile, 0))


def _orientations(tile):
    yield tile
    for _ in range(3):
        tile = np.rot90(tile, 1)
        yield tile


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
        return np.rot90(tile2, 1)
    elif tile1_edge == tile2_bot_edge:
        return np.rot90(tile2, -1)
    elif tile1_edge == tile2_bot_edge[::-1]:
        return np.flip(np.rot90(tile2, -1), 0)
    else:
        return


def _get_down_neighbor(tile1: np.array, tile2: np.array):
    tile1_edge = list(tile1[-1, :])
    tile2_left_edge = list(tile2[:, 0])
    tile2_right_edge = list(tile2[:, -1])
    tile2_top_edge = list(tile2[0, :])
    tile2_bot_edge = list(tile2[-1, :])

    if tile1_edge == tile2_top_edge:
        return tile2
    elif tile1_edge == tile2_top_edge[::-1]:
        return np.flip(tile2, 1)  # flip in y axis
    elif tile1_edge == tile2_bot_edge:
        return np.flip(tile2, 0)  # flip in x axis
    elif tile1_edge == tile2_bot_edge[::-1]:
        return np.flip(tile2, (0, 1))  # flip in both axis
    elif tile1_edge == tile2_right_edge:
        return np.rot90(tile2, 1)
    elif tile1_edge == tile2_right_edge[::-1]:
        return np.flip(np.rot90(tile2, 1), 1)
    elif tile1_edge == tile2_left_edge:
        return np.flip(np.rot90(tile2, -1), 1)
    elif tile1_edge == tile2_left_edge[::-1]:
        return np.rot90(tile2, -1)
    else:
        return


def solve():
    tiles = get_input_list()

    # PART 1
    multiplied_edges = solve1(tiles)
    print(f'[PART 1] The multiplied edges are {multiplied_edges}')

    # PART 2
    non_sea_monster = solve2(tiles)
    print(f'[PART 2] {non_sea_monster} # are not part of a monster')


if __name__ == '__main__':
    solve()
