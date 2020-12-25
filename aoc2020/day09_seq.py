from aoc2020.input_utils import get_input_file_lines
from copy import deepcopy


def can_be_sum(cache, next_val):
    for i in range(len(cache)):
        for j in range(i+1, len(cache)):
            if cache[i] + cache[j] == next_val:
                return True
    return False


def part01(lines):
    cache = [int(x) for x in lines[:25]]
    for i in range(26, len(lines)):
        next_val = int(lines[i])
        if not can_be_sum(cache, next_val):
            return next_val, i
        cache = cache[1:] + [next_val]


def part02(lines):
    error_num, line_num = part01(lines)
    for i in range(25, len(lines)):
        if i == line_num:
            continue
        acc = int(lines[i])
        for j in range(i+1, len(lines)):
            if j == line_num:
                continue
            if acc > error_num:
                break
            if(acc) == error_num:
                nums = [int(x) for x in lines[i:j]]
                return min(nums) + max(nums)
            acc += int(lines[j])


if __name__ == '__main__':
    part = 1
    part_to_call = {1: part01, 2: part02}
    lines = get_input_file_lines('day09_seq.txt')
    res = part_to_call[part](lines)
    print(f'Part {part}: {res}')
