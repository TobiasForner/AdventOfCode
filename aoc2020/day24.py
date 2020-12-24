from aoc2020.input_utils import get_input_file_lines_no_nl


def part01(lines):
    dir_lists = parse_input(lines)
    black_positions = compute_black_positions(dir_lists)
    print('part 1:', len(black_positions))


def compute_black_positions(dir_lists):
    black_positions = set()
    for dirs in dir_lists:
        pos = compute_position_from(HexPosition(0, 0), dirs)
        if pos in black_positions:
            black_positions.remove(pos)
        else:
            black_positions.add(pos)
    return black_positions


def compute_position_from(pos, dirs):
    if not dirs:
        return pos
    else:
        next_pos = pos.get_pos_in_dir(dirs[0])
        return compute_position_from(next_pos, dirs[1:])


def parse_input(lines):
    dir_lists = []
    for line in lines:
        dirs = parse_dir_line(line)
        dir_lists.append(dirs)
    return dir_lists


def parse_dir_line(line):
    dirs = []
    line_rest = line
    while line_rest:
        if line_rest[0] in ['w', 'e']:
            dirs.append(line_rest[0])
            line_rest = line_rest[1:]
        else:
            dirs.append(line_rest[:2])
            line_rest = line_rest[2:]
    return dirs


class HexPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, obj):
        if isinstance(obj, HexPosition):
            return obj.x == self.x and obj.y == self.y
        return False

    def get_east_of(self):
        return HexPosition(self.x+1, self.y)

    def get_south_east_of(self):
        return HexPosition(self.x+1, self.y-1)

    def get_south_west_of(self):
        return HexPosition(self.x, self.y-1)

    def get_west_of(self):
        return HexPosition(self.x-1, self.y)

    def get_north_west_of(self):
        return HexPosition(self.x-1, self.y+1)

    def get_north_east_of(self):
        return HexPosition(self.x, self.y+1)

    def get_adjacent_positions(self):
        res = set()
        res.add(self.get_east_of())
        res.add(self.get_south_east_of())
        res.add(self.get_south_west_of())
        res.add(self.get_west_of())
        res.add(self.get_north_west_of())
        res.add(self.get_north_east_of())
        return res

    def get_pos_in_dir(self, dir):
        dir_to_function = {'e': self.get_east_of, 'se': self.get_south_east_of, 'sw': self.get_south_west_of,
                           'w': self.get_west_of, 'nw': self.get_north_west_of, 'ne': self.get_north_east_of}
        return dir_to_function[dir]()


class HexGameOfLife:
    def __init__(self, black_positions):
        self.black_positions = set(black_positions)

    def get_black_tile_nr(self):
        return len(self.black_positions)

    def play(self, round_nr=100):
        for _ in range(round_nr):
            self.__play_round()

    def __play_round(self):
        self.__determine_next_black_positions()

    def __determine_next_black_positions(self):
        positions_to_consider = set()
        positions_to_consider = positions_to_consider.union(
            self.black_positions)
        for pos in self.black_positions:
            positions_to_consider = positions_to_consider.union(
                pos.get_adjacent_positions())
        next_black_positions = set()
        for pos in positions_to_consider:
            if self.__pos_is_black_next_round(pos):
                next_black_positions.add(pos)
        self.black_positions = next_black_positions

    def __pos_is_black_next_round(self, pos):
        adjacent_positions = pos.get_adjacent_positions()
        adjacent_black_positions = adjacent_positions.intersection(
            self.black_positions)
        if pos in self.black_positions:
            if len(adjacent_black_positions) == 0 or len(adjacent_black_positions) > 2:
                return False
            return True
        else:
            if len(adjacent_black_positions) == 2:
                return True
            return False


def part02(lines):
    dir_lists = parse_input(lines)
    black_positions = compute_black_positions(dir_lists)
    game = HexGameOfLife(black_positions)
    game.play(100)
    print('Part 2:', game.get_black_tile_nr())


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day24.txt')
    part01(lines)
    part02(lines)
