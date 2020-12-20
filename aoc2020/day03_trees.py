from functools import reduce
from aoc2020.input_utils import get_input_file_lines


def count_trees_hit(lines, movement, start=(0, 0), verbose=True):
    hits = 0
    pos = start
    while pos[0] < len(lines):
        output = str(pos)
        if lines[pos[0]][pos[1]] == '#':
            hits += 1
            output += ' hit!'
        if verbose:
            print(output)
        pos = pos[0] + movement[0], (pos[1] +
                                     movement[1]) % (len(lines[0]) - 1)
    return hits


def trees_hit_prod(lines, patterns, verbose=False):
    return reduce((lambda x, y: x * y), [count_trees_hit(lines, pattern, verbose=False) for pattern in patterns])


if __name__ == '__main__':
    part = 2
    patterns = [[(1, 3)], [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]]
    lines = get_input_file_lines('day03_trees.txt')
    print('trees hit product:', trees_hit_prod(lines, patterns[part - 1]))
