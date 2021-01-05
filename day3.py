from utils import get_input_text


def get_input_list():
    input_text = get_input_text(3)
    return input_text.split('\n')


def get_trees_encountered(map_rows, right_steps, down_steps):
    """
    Exaplanation of the mod condition:

    If for example down_steps is 2, we want the 1st row then the 3rd, 5th, etc
    with indexes 0, 2, 4, etc. In the same way, if down_steps is 3, the wanted
    indexes would be 0, 3, 6 etc. So the index must be an integral multiple of
    the down_steps.
    Exception to the above rule is the case down_steps=1 where there is no need
    to check any condition cause every row is wanted.

    Args:
        map_rows (list of strings): The rows of the map. '#' represent trees
            and '.' represent clear terrain.
        right_steps (integer): Right steps that slopes follows per step.
        down_steps (integer): Down steps that slopes follows per step.
    Returns:
        integer: The number of trees encountered.
    """
    trees_encountered = 0
    total_col_index = 0

    for ind, row in enumerate(map_rows):
        if down_steps > 1 and ind % down_steps:
            continue
        # because the map is extended with the SAME PATTERN, instead of extending
        # the map we can limit the col index inside the original row limits.
        real_index = total_col_index % len(row)
        is_tree = row[real_index] == '#'

        trees_encountered += is_tree
        total_col_index += right_steps

    return trees_encountered


def get_product_of_trees_in_given_slopes(input_list, slopes):
    product = 1
    for slope in slopes:
        product *= get_trees_encountered(input_list, *slope)

    return product


def solve():
    input_list = get_input_list()

    # PART 1
    trees_encountered = get_trees_encountered(input_list, 3, 1)
    print(f'[PART 1] {trees_encountered} trees encountered')

    # PART 2
    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    trees_encountered_2 = get_product_of_trees_in_given_slopes(input_list, slopes)
    print(f'[PART 2] {trees_encountered_2} trees encountered')


if __name__ == '__main__':
    solve()
