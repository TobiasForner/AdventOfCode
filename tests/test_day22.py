import unittest

from aoc2020.day22 import part01, part02
from aoc2020.input_utils import read_file_contents


class TestDay22(unittest.TestCase):

    def test_example_part01(self):
        lines = read_file_contents('../inputs/day22_test.txt')
        self.assertEqual(part01(lines), 306)

    def test_example_part02(self):
        lines = read_file_contents('../inputs/day22_test.txt')
        self.assertEqual(part02(lines), 291)

    def test_part01(self):
        lines = read_file_contents('../inputs/day22.txt')
        self.assertEqual(part01(lines), 32366)

    def test_part02(self):
        lines = read_file_contents('../inputs/day22.txt')
        self.assertEqual(part02(lines), 30891)
