import unittest

from aoc2020.day20 import Tile
from aoc2020.input_utils import get_input_file_lines_no_nl


class TestDay20(unittest.TestCase):
    def test_turn_counter_clockwise(self):
        contents = [['1', '2'], ['3', '4']]
        tile = Tile(0, contents)
        tile.turn_counter_clockwise()
        exp_contents = [['2', '4'], ['1', '3']]
        self.assertEqual(tile.contents, exp_contents)

    def test_turn_clockwise(self):
        contents = [['2', '4'], ['1', '3']]
        tile = Tile(0, contents)
        tile.turn_clockwise()
        exp_contents = ['12', '34']
        self.assertEqual(tile.contents, exp_contents)
