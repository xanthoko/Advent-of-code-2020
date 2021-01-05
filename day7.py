from utils import get_input_text


def get_input_list():
    input_text = get_input_text(7)
    return input_text.split('\n')


def solve_1(rules):
    """Calculates the number of bags that can contain at least one shiny gold.

    Given rules give the colors that every bag can contain. To solve the problem
    we reverse the rules and create a map that has for every bag, in which bags
    it can be contained.

    For example if a rule says 'bright white bags contain 1 shiny gold bag.',
    the created map says {'shiny gold': ['bright white', ...]}

    For the solution I use a recursive method that calculates the number of bags
    in which the given color can be contained.

    Args:
        rules (list of strings): Bag rules
    Returns:
        integer: The number of bags that contain at least one shiny gold bag
    """
    color_map = _create_color_map(rules)
    wanted_color = 'shiny gold'
    bags_list = _get_bags_that_can_contain_color(wanted_color, color_map)
    bags_set = set(bags_list)  # remove the duplicates
    return len(bags_set)


def _create_color_map(rules):
    """Creates the color map.

    The color map has the bags in which every color can be contained.
    For example color_map = {'yellow': ['red', 'blue']} mean that a yellow bag
    can be contained inside a red or a blue bag.
    """
    color_map = {}
    for rule in rules:
        main_color, contains_string = rule.split(' bags contain ')
        contains_colors = _get_colors_from_string(contains_string)
        for contains_color in contains_colors:
            try:
                color_map[contains_color].append(main_color)
            except KeyError:
                color_map[contains_color] = [main_color]

    return color_map


def _get_colors_from_string(contains_string):
    """Retrieves the colors from the given string.

    Args:
        contains_string (string): A string with the colors like
            '1 bright white bag, 2 muted yellow bags'
    Returns:
        list of string: The colors found in string
    """
    colors = []
    for phrase in contains_string.split(', '):
        words = phrase.split(' ')
        # join the middle words that are the colors
        color = ' '.join(words[1:3])
        colors.append(color)

    return colors


def _get_bags_that_can_contain_color(color, color_map):
    """The recursive method."""
    try:
        master_colors = color_map[color]
        ret = []
        for master_color in master_colors:
            # append the master color and the colors that it can be contained in
            ret.append(master_color)
            ret.extend(_get_bags_that_can_contain_color(master_color, color_map))
        return ret
    except KeyError:
        # end the recursion
        return []


def solve_2(rules):
    """Calculates the number of bags that can be contained inside the
    shiny gold one.

    Args:
        rules (list of strings): Bag rules
    Returns:
        integer: The number of bags a shiny gold bag can contain
    """
    bag_data_map = {}
    for rule in rules:
        main_color, contains_string = rule.split(' bags contain ')
        contains = _get_color_and_quantity_from_string(contains_string)
        bag_data_map[main_color] = contains

    return _get_number_of_bags_inside_color(bag_data_map, 'shiny gold', {})


def _get_color_and_quantity_from_string(contains_string):
    """Returns a list with the quantity and the color of the bags in the
    given string.

    Args:
        contains_string (string): A string with the colors like
            '1 bright white bag, 2 muted yellow bags'
    Returns:
        list of dictionaries
    """
    colors_quantity_list = []
    for phrase in contains_string.split(', '):
        words = phrase.split(' ')
        # join the middle words that are the colors
        try:
            quantity = int(words[0])
        except ValueError:
            # phrase = 'no other bags' so words[0] = 'no'
            quantity = 0
        color = ' '.join(words[1:3])
        colors_quantity_list.append({'quantity': quantity, 'color': color})
    return colors_quantity_list


def _get_number_of_bags_inside_color(data_map, color, cache):
    """A method that uses dynamic programming to get the number of bags inside
    the bag with the given color.

    Args:
        data_map (dictionary): {'red': [{'quantity': 2, 'color': 'blue}, ...], ...}
        color (string)
        cache (dictionary): A dictionary with the saved values found
    Returns:
        integer: The number of bags contained in the bag with the given color
    """
    containers = data_map[color]
    counter = 0
    for container in containers:
        contained_color = container['color']
        contained_quantity = container['quantity']
        # the termination condition
        if contained_quantity == 0:
            cache[contained_color] = 0
            return 0

        try:
            bags_inside = cache[contained_color]
        except KeyError:
            # color not found in cache, update it
            bags_inside = _get_number_of_bags_inside_color(
                data_map, contained_color, cache)
            cache[contained_color] = contained_quantity

        # if for example the gold bag contains 4 bags and we have 2 gold bags
        # the counter icreases by 2(golds) *(that have) 4(bags) + 2(golds) = 10
        counter += contained_quantity * bags_inside + contained_quantity

    return counter


def solve():
    rules_list = get_input_list()

    # PART 1
    number_of_bags = solve_1(rules_list)
    print(f'[PART 1] {number_of_bags} bags contain at least one shiny gold bag.')

    # PART 2
    bags_inside_gold = solve_2(rules_list)
    print(f'[PART 2] {bags_inside_gold}')


if __name__ == '__main__':
    solve()
