from input_utils import get_input_file_lines
from copy import deepcopy


def part02(lines):
    """solves part 2 of day 8 of AoC 2020

    Args:
        lines (string list): input lines

    Returns:
        (int, boolean): accumulator and whether a hit was found, i.e. whether nop and jmp could be exchanged to obtain a terminating program
    """
    for i in range(len(lines)):
        lines_tmp = deepcopy(lines)
        if 'nop' in lines[i] and ' ' in lines[i]:
            lines_tmp[i] = lines[i].replace('nop', 'jmp')
        elif 'jmp' in lines[i] and ' ' in lines[i]:
            lines_tmp[i] = lines[i].replace('jmp', 'nop')
        else:
            continue
        acc, loop = part01(lines_tmp)
        if not loop:
            return acc, True
    return 0, False


def part01(lines):
    """solves part 1 of day 8 of AoC 2020, returns the value of the accumulator directly before the first reexecution of any line

    Args:
        lines (list(string)): lines of the input

    Returns:
        int, bool: [description]
    """
    pos = 0
    lines_executed = []
    acc = 0
    while True:
        if pos in lines_executed:
            #print(f'Part 01: Value in acc before repeat: {acc}')
            return acc, True
        elif pos == len(lines):
            return acc, False
        l = lines[pos]
        l = l.replace('\n', '')
        lines_executed.append(pos)
        if 'nop' in l:
            pos += 1
            continue
        command, val = l.split(' ')
        if command == 'acc':
            acc += int(val)
            pos += 1
        elif command == 'jmp':
            pos += int(val)


if __name__ == '__main__':
    part = 2
    part_to_call = {1: part01, 2: part02}
    lines = get_input_file_lines('day08_code.txt')
    acc, found = part_to_call[part](lines)
    if found:
        print(f'Part {part}: {acc}')
    else:
        print(f'Error in Part {part}: not found!')
