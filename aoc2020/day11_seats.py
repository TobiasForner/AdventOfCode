from input_utils import get_input_file_lines_no_nl
from copy import deepcopy


def count_surrounding(i, j, seats):
    surrounding_seats = [seats[i+x, j+y] for x in [-1, 0, 1]
                         for y in [-1, 0, 1] if not (x, y) == (0, 0)]
    return surrounding_seats.count('#')


def print_seats(seats, nrow, ncol):
    out = ''
    for i in range(nrow):
        row = ''
        for j in range(ncol):
            row += seats[i, j]
        out += row + '\n'
    print(out)


def count_first_visible(i, j, seats):
    count = 0
    directions = [(x, y) for x in [-1, 0, 1]
                  for y in [-1, 0, 1] if not (x, y) == (0, 0)]
    for d in directions:
        pos = (i, j)
        while True:
            pos = pos[0] + d[0], pos[1] + d[1]
            if pos not in seats.keys() or seats[pos] == 'L':
                break
            elif seats[pos] == '#':
                count += 1
                break

    return count


def convertToSeats(lines):
    seats = deepcopy(lines)
    empty_row = ['.'*(len(seats[0])+2)]
    seats = empty_row + ['.' + l + '.' for l in seats] + empty_row
    nrow, ncol = len(seats), len(seats[0])
    seats = {(i, j): seats[i][j] for i in range(len(seats))
             for j in range(len(seats[0]))}
    return seats, nrow, ncol


def count_seats_after_reseating(seats, nrow, ncol, vis_limit, count_method=count_surrounding, verbose=False):
    change = True
    while change:
        if verbose:
            print('--------------------------------')
            print_seats(seats, nrow, ncol)
        change = False
        surrounding = {}
        for i in range(1, nrow-1):
            for j in range(1, ncol - 1):
                surrounding[(i, j)] = count_method(i, j, seats)
        for i in range(1, nrow-1):
            for j in range(1, ncol - 1):
                if seats[(i, j)] == 'L' and surrounding[(i, j)] == 0:
                    seats[(i, j)] = '#'
                    change = True
                elif seats[(i, j)] == '#' and surrounding[(i, j)] >= vis_limit:
                    seats[(i, j)] = 'L'
                    change = True
    return ''.join(seats.values()).count('#')


def part01(seats, nrow, ncol):
    print(f'part01: {count_seats_after_reseating(seats, nrow, ncol, 4)}')


def part02(seats, nrow, ncol):
    print(
        f'part02: {count_seats_after_reseating(seats, nrow, ncol, 5, count_first_visible)}')


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day11_seats.txt')
    res = convertToSeats(lines)
    part01(*res)
    part02(*res)
