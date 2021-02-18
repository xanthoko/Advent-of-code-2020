from typing import List

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(21)

    foods_str = input_text.split('\n')
    foods = []
    for food_str in foods_str:
        ingridients_str, allergens_str = food_str.split(' (')
        ingridients = ingridients_str.split(' ')
        allergens = allergens_str[:-1].split('contains ')[1].split(', ')
        foods.append({'ingridients': ingridients, 'allergens': allergens})

    return foods


def solve1(foods: List[dict]):
    """Solution is greatly influenced by this
    https://github.com/aboutroots/AoC2020/blob/master/day21.py"""
    all_ingredients_with_duplicates = []
    all_allergens = set()
    for food in foods:
        all_ingredients_with_duplicates.extend(food['ingridients'])
        all_allergens.update(set(food['allergens']))

    proposed_names = {}
    solved = {}

    while len(solved) != len(all_allergens):
        for food in foods:
            allergens = food['allergens']
            ingridients = food['ingridients']

            for allergen in allergens:
                if allergen in solved:
                    continue

                if allergen not in proposed_names:
                    proposed_names[allergen] = set(ingridients) - set(
                        solved.values())
                else:
                    proposed_names[allergen] &= set(ingridients)

                if len(proposed_names[allergen]) == 1:
                    name = proposed_names[allergen].pop()
                    solved[allergen] = name
                    del proposed_names[allergen]
                    for other_allergen in proposed_names.keys():
                        proposed_names[other_allergen].discard(name)

    return all_ingredients_with_duplicates, solved


def solve2(solved_pairs: dict):
    sorted_ingridents = [x[1] for x in sorted(solved_pairs.items())]
    formated_ingridients = ','.join(sorted_ingridents)
    return formated_ingridients


def solve():
    foods = get_input_list()

    # PART 1
    all_ingredients, solved = solve1(foods)
    times_of_appearance = sum(1 for ing in all_ingredients
                              if ing not in solved.values())
    print(f'[PART 1] {times_of_appearance} times appeared')

    # PART 2
    sorted_ingridients = solve2(solved)
    print(f'[PART 2] {sorted_ingridients}')


if __name__ == '__main__':
    solve()
