from aoc2020.input_utils import get_input_file_lines_no_nl
import re
from functools import reduce

in_brackets_pattern = re.compile(r'\(([*+\d]*)\)')

addition_first_pattern = re.compile(r'(\d*)\+(\d*)([\d\+\*]*)')

mult_first_pattern = re.compile(r'(\d*)\*(\d*)([\d\+\*]*)')

addition_sequence_pattern = re.compile(r'((?:\d+\+)+\d+)')


def compute_product(num_list):
    return reduce(lambda x, y: x*y, num_list)


def evaluate_line_without_brackets_part2(line):
    match_add = re.search(addition_sequence_pattern, line)
    if match_add:
        add_sequence = match_add.group(1)
        sum_res = sum([int(x) for x in add_sequence.split('+')])
        new_line = line.replace(match_add[0], str(sum_res))
        return evaluate_line_without_brackets_part2(new_line)
    elif '*' in line:
        return str(compute_product([int(x) for x in line.split('*')]))
    return line


def evaluate_line_without_brackets(line):
    match_add = re.match(addition_first_pattern, line)
    if match_add:
        first, second, rest = match_add.groups()
        new_line = str(int(first)+int(second))+rest
        return evaluate_line_without_brackets(new_line)

    match_mult = re.match(mult_first_pattern, line)
    if match_mult:
        first, second, rest = match_mult.groups()
        new_line = str(int(first)*int(second))+rest
        return evaluate_line_without_brackets(new_line)

    return line


def remove_parantheses(line, evaluate_line_without_brackets):
    stripped_line = line
    while any([para in stripped_line for para in ['(', ')']]):
        para_match = re.search(in_brackets_pattern, stripped_line)
        if not para_match:
            raise ValueError('Invalid input string')
        matched_string = para_match[0]
        inside_brackets_without_brackets = remove_parantheses(
            para_match[1], evaluate_line_without_brackets)
        stripped_line = stripped_line.replace(
            matched_string, inside_brackets_without_brackets)

    return evaluate_line_without_brackets(stripped_line)


def evaluate_line(line):
    stripped_line = line.replace(' ', '')
    line_without_parantheses = remove_parantheses(
        stripped_line, evaluate_line_without_brackets)
    return int(line_without_parantheses)


def part01(lines, verbose=False):
    results = [evaluate_line(line) for line in lines]
    if verbose:
        print('results:', results)
    print(f'Part 1: {sum(results)}')


def part02(lines, verbose=False):
    results = [evaluate_line_part2(line) for line in lines]
    if verbose:
        print('results:', results)
    print(f'Part 2: {sum(results)}')


def evaluate_line_part2(line):
    stripped_line = line.replace(' ', '')
    line_without_parantheses = remove_parantheses(
        stripped_line, evaluate_line_without_brackets_part2)
    return int(line_without_parantheses)


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day18.txt')
    part01(lines)
    part02(lines)
