import unittest

from aoc2020.day19 import part01, part02
from aoc2020.input_utils import get_input_file_lines_no_nl


class TestDay19(unittest.TestCase):

    def test01(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test.txt')
        assert part01(lines) == 2

    def test02(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test02.txt')
        assert part01(lines) == 1

    def test03(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test03.txt')
        assert part01(lines) == 1

    def test04(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test04.txt')
        assert part02(lines) == 12

    def test04_shortened(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test04_short.txt')
        assert part02(lines) == 1

    def test05(self):
        lines = get_input_file_lines_no_nl(
            '../inputs/day19_test04.txt')
        assert part01(lines) == 3


if __name__ == '__main__':
    unittest.main()
