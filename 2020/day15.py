from input_utils import get_input_file_lines_no_nl
import time


def play_game(lines, max_turn, verbose=False, not_freq=100000):
    """
    plays the numbers game as specified in day 15 of AoC 2020

    Args:
        lines (string list): one line containing the starting numbers separated by commas
        max_turn (int): number of turns that are to be played
        verbose (bool, optional): whether to print any iteration output. Defaults to False.
        not_freq (int, optional): frequency of output, only if verbose. Defaults to 100000.

    Returns:
        int: number spoken at turn length
    """
    nums = [int(x) for x in lines[0].split(',')]
    start_time = time.perf_counter()
    last_spoken_in_turn = [None] * max_turn
    for turn, num in enumerate(nums):
        last_spoken_in_turn[num] = turn
        last_num_spoken = num
    for turn in range(len(nums), max_turn):
        if verbose and turn % not_freq == 0:
            print(f'turn {turn}')
        next_num = 0
        if last_spoken_in_turn[last_num_spoken] != None:
            next_num = turn - last_spoken_in_turn[last_num_spoken] - 1
        last_spoken_in_turn[last_num_spoken] = turn - 1
        last_num_spoken = next_num
    end_time = time.perf_counter()
    return last_num_spoken, end_time-start_time


def part01(lines, verbose=False):
    print('part 1:', play_game(lines, 2020, verbose))


def part02(lines, verbose=False):
    print('part 2:', play_game(lines, 30000000, verbose))


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day15.txt')
    part01(lines)
    part02(lines)
