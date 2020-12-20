from input_utils import get_input_file_lines, get_input_file_lines_no_nl
from copy import deepcopy
from math import factorial


def print_answer01(jolt_sequence):
    gaps = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in range(1, len(jolt_sequence)):
        gaps[abs(jolt_sequence[i] - jolt_sequence[i-1])] += 1
    print(f'1 gaps: {gaps[1]}, 3 gaps: {gaps[3]}')
    print(gaps[1] * gaps[3])


def part01(jolts):
    def get_possible_next(jolts_left, input_j, indices, prev_seq):
        possible_adapters = []
        for index, j in enumerate(jolts_left):
            if index in indices:
                continue
            if input_j in range(j-3, j+1):
                possible_adapters.append((prev_seq + [j], indices + [index]))
        return possible_adapters

    queue = get_possible_next(jolts, 0, [], [])
    while queue:
        seq, indices = queue[0]
        queue = queue[1:]
        possible_next = get_possible_next(jolts, seq[-1], indices, seq)
        for seq, ind in possible_next:
            if len(seq) == len(jolts):
                print('candidate:', seq)
                if seq[-1] in range(max(jolts) - 3, max(jolts)+1):
                    mod_seq = [0] + seq + [max(jolts)]
                    print_answer01(mod_seq)
                    return
            else:
                queue.append((seq, ind))
    print('Error: no sequence found')


def part01_trick(jolts):
    print_answer01([0] + sorted(jolts) + [max(jolts) + 3])


def binom(n, k):
    return factorial(n) / (factorial(n-k) * factorial(k))


def part02(jolts):
    def count_num_removable(jolts, start):
        count = -1
        while jolts[start] + 3 >= jolts[start + 2 + count] and start + 2 + count < len(jolts) - 1:
            count += 1
        count = sum([1 for i in range(start+1, start+3)
                     if i < len(jolts)-1 and abs(jolts[start] - jolts[i+1]) <= 3])
        return max(0, count)

    starting_point = [0] + sorted(jolts) + [max(jolts) + 3]
    removable = {}
    for i in range(0, len(starting_point) - 1):
        removable[i] = count_num_removable(starting_point, i)
    print(removable)
    options_accum = {len(starting_point)-2: 1, len(starting_point)-1: 1}

    for index in range(len(starting_point) - 3, -1, -1):
        options_accum[index] = sum(
            [options_accum[index + 1+i] for i in range(removable[index] + 1)])
    print(f'part 02: {options_accum[0]}')


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day10_adapters.txt')
    jolts = [int(x) for x in lines]
    # part01_trick(jolts)
    part02(jolts)
