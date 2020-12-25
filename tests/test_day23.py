import unittest

from aoc2020.day23 import part01


class TestDay23(unittest.TestCase):

    def test_example_part01(self):
        cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
        self.assertEqual(part01(cups), '67384529')
