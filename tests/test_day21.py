import unittest

from aoc2020.day21 import part01, part02, parse_input, allergens_to_possible_ingredient
from aoc2020.input_utils import get_input_file_lines_no_nl


class TestDay21(unittest.TestCase):
    def test_example_part1(self):
        ingredients_list, allergens_list = parse_input(['mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
                                                        'trh fvjkl sbzzf mxmxvkd (contains dairy)',
                                                        'sqjhc fvjkl (contains soy)',
                                                        'sqjhc mxmxvkd sbzzf (contains fish)'])
        alg_to_ing = allergens_to_possible_ingredient(
            ingredients_list, allergens_list)
        result = part01(ingredients_list, allergens_list, alg_to_ing)
        self.assertEqual(result, 5)

    def test_part1(self):
        lines = get_input_file_lines_no_nl('day21.txt')
        ingredients_list, allergens_list = parse_input(lines)
        alg_to_ing = allergens_to_possible_ingredient(
            ingredients_list, allergens_list)
        result = part01(ingredients_list, allergens_list, alg_to_ing)
        self.assertEqual(result, 2485)

    def test_example_part2(self):
        ingredients_list, allergens_list = parse_input(['mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
                                                        'trh fvjkl sbzzf mxmxvkd (contains dairy)',
                                                        'sqjhc fvjkl (contains soy)',
                                                        'sqjhc mxmxvkd sbzzf (contains fish)'])
        alg_to_ing = allergens_to_possible_ingredient(
            ingredients_list, allergens_list)
        result = part02(alg_to_ing)
        self.assertEqual(result, 'mxmxvkd,sqjhc,fvjkl')

    def test_part2(self):
        lines = get_input_file_lines_no_nl('day21.txt')
        ingredients_list, allergens_list = parse_input(lines)
        alg_to_ing = allergens_to_possible_ingredient(
            ingredients_list, allergens_list)
        result = part02(alg_to_ing)
        self.assertEqual(
            result, 'bqkndvb,zmb,bmrmhm,snhrpv,vflms,bqtvr,qzkjrtl,rkkrx')


if __name__ == '__main__':
    unittest.main()
