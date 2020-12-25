from aoc2020.input_utils import get_input_file_lines_no_nl
from functools import reduce


def part01(ingredients_list, allergens_list, alg_to_ing):
    possible_ingredients = set([x for l in ingredients_list for x in l])
    ingredients_with_allergens = reduce(
        lambda x, y: x.union(y), alg_to_ing.values())
    ingredients_without_allergens = possible_ingredients - ingredients_with_allergens
    result = count_ingredients_without_allergens(
        ingredients_without_allergens, ingredients_list)
    print('Part 1:', result)
    return result


def count_ingredients_without_allergens(ingredients_without_allergens, ingredients_list):
    count = 0
    for ingredients in ingredients_list:
        for ing in ingredients_without_allergens:
            count += ingredients.count(ing)
    return count


def part02(alg_to_ing):
    alg_to_ing_solved = solve_alg_to_ing(alg_to_ing)
    sorted_allergens = sorted(list(alg_to_ing_solved.keys()))
    result = ','.join([list(alg_to_ing_solved[alg])[0]
                       for alg in sorted_allergens])
    print('Part 2:', result)
    return result


def solve_alg_to_ing(alg_to_ing):
    while any([len(x) > 1 for x in alg_to_ing.values()]):
        used_ingredients, alg_to_ing_new = ingredients_with_clear_allergen(
            alg_to_ing)
        alg_to_ing = compute_new_alg_to_ing(
            alg_to_ing, used_ingredients, alg_to_ing_new)
    return alg_to_ing


def ingredients_with_clear_allergen(alg_to_ing):
    alg_to_ing_new = {}
    used_ingredients = set()
    for alg, ing_set in alg_to_ing.items():
        if len(ing_set) == 1:
            alg_to_ing_new[alg] = ing_set
            used_ingredients = used_ingredients.union(ing_set)
    return used_ingredients, alg_to_ing_new


def compute_new_alg_to_ing(alg_to_ing, used_ingredients, alg_to_ing_new):
    for alg, ing_set in alg_to_ing.items():
        if len(ing_set) > 1:
            new_ing_set = ing_set - used_ingredients
            alg_to_ing_new[alg] = new_ing_set
    return alg_to_ing_new


def parse_input(lines):
    ingredients_lists = []
    allergens_lists = []
    for line in lines:
        ingredients_text, allergens_text = line.replace(
            ')', '').split(' (contains ')
        ingredients_lists.append(ingredients_text.split(' '))
        allergens_lists.append(allergens_text.split(', '))
    return ingredients_lists, allergens_lists


def allergens_to_possible_ingredient(ingredients_list, allergens_list):
    alg_to_ing = {}
    for index, allergens in enumerate(allergens_list):
        for alg in allergens:
            if alg not in alg_to_ing:
                alg_to_ing[alg] = set(ingredients_list[index])
            else:
                prev = alg_to_ing[alg]
                alg_to_ing[alg] = prev.intersection(
                    set(ingredients_list[index]))

    return alg_to_ing


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day21.txt')
    ingredients_list, allergens_list = parse_input(lines)
    alg_to_ing = allergens_to_possible_ingredient(
        ingredients_list, allergens_list)
    part01(ingredients_list, allergens_list, alg_to_ing)
    part02(alg_to_ing)
