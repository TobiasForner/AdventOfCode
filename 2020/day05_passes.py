from input_utils import get_input_file_lines


def calculate_pos(s, first, bounds):
    middle = bounds[0] + (bounds[1] - bounds[0])//2
    if not s:
        return bounds[0]
    if s[0] == first:
        return calculate_pos(s[1:], first, (bounds[0], middle))
    else:
        return calculate_pos(s[1:], first, (middle + 1, bounds[1]))


def calculate_row(s, bounds=(0, 127)):
    return calculate_pos(s, 'F', bounds)


def calculate_col(s, bounds=(0, 7)):
    return calculate_pos(s, 'L', bounds)


def get_ids(lines):
    res = []
    for line in lines:
        row = calculate_row(line[:7])
        col = calculate_col(line[7:10])
        res.append((row, col, row * 8 + col, line[:10]))
    return res


def find_gap(l):
    for i in range(1, len(l)):
        if l[i-1] < l[i]-1:
            return l[i]-1
    return


if __name__ == '__main__':
    test = False
    lines = get_input_file_lines('day05_passes.txt')
    if test:
        lines = ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']
    res = get_ids(lines)
    if test:
        print(res)
    else:
        m = max([x for (_, _, x, _) in res])
        print('max:', m)
        print('complete', [x for x in res if x[2] == m])
        print('seat:', find_gap(sorted([x for (_, _, x, _) in res])))
