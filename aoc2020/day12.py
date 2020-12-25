from aoc2020.input_utils import get_input_file_lines_no_nl


def get_turned_dir(d, turn):
    directions = ['N', 'E', 'S', 'W']
    return directions[(directions.index(d) + turn // 90) % 4]


def part01(lines):
    ship_dir = 'E'
    coords = {'N': 0, 'E': 0, 'S': 0, 'W': 0}
    for l in lines:
        direction = l[0]
        val = int(l[1:])
        if direction == 'F':
            coords[ship_dir] += val
            coords[get_turned_dir(ship_dir, 180)] -= val
        elif direction in coords:
            coords[direction] += val
            coords[get_turned_dir(direction, 180)] -= val
        elif direction == 'R':
            ship_dir = get_turned_dir(ship_dir, val)
        elif direction == 'L':
            ship_dir = get_turned_dir(ship_dir, -val)
    res = abs(coords['N']) + abs(coords['E'])
    print(f'part01: {res}')


def part02(lines, verbose=False):
    waypoint_coords = {'N': 1, 'E': 10, 'S': -1, 'W': -10}
    coords = {'N': 0, 'E': 0, 'S': 0, 'W': 0}
    for l in lines:
        if verbose:
            print('-----------------------------------')
            print('ship:', coords)
            print('waypoint:', waypoint_coords)
        direction = l[0]
        val = int(l[1:])
        if direction == 'F':
            for d, v in waypoint_coords.items():
                coords[d] += val * v
        elif direction in coords:
            waypoint_coords[direction] += val
            waypoint_coords[get_turned_dir(direction, 180)] -= val
        elif direction == 'R':
            waypoint_coords = {get_turned_dir(
                d, val): v for (d, v) in waypoint_coords.items()}
        elif direction == 'L':
            waypoint_coords = {get_turned_dir(
                d, -val): v for (d, v) in waypoint_coords.items()}

    res = abs(coords['N']) + abs(coords['E'])
    if verbose:
        print(coords)
    print(f'part02: {res}')


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day12.txt')
    part01(lines)
    part02(lines)
