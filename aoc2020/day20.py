from aoc2020.input_utils import read_file_contents

from functools import reduce
from math import sqrt, prod

SEAMONSTER_PATTERN = {'row_length': 20, 'patterns': [
    [18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]}
HASHTAG_PATTERN = {'row_length': 1, 'patterns': [[0]]}


class Tile:
    opposites = {'left': 'right', 'top': 'bottom',
                 'right': 'left', 'bottom': 'top'}

    def __init__(self, num, contents):
        self.contents = contents
        self.num = num
        self.possible_neighbors = []
        self.edges = {}
        self.__compute_edges()
        self.possible_edges = []
        self.__compute_possible_edges()

    def has_edges_in_common_with(self, other_tile):
        if any([other_tile.has_possible_edge(edge) for edge in self.possible_edges]):
            return True

    def tile_fits_at_position(self, tile, pos):
        return self.edges[pos] == tile.edges[Tile.opposites[pos]]

    def has_possible_edge(self, edge):
        return edge in self.possible_edges

    def mirror_vertically(self):
        self.contents = [row[::-1] for row in self.contents]
        self.__compute_edges()

    def turn_counter_clockwise(self):
        new_contents = [[self.contents[j][i] for j in range(
            len(self.contents))] for i in range(len(self.contents[0])-1, -1, -1)]
        self.contents = new_contents
        self.__compute_edges()

    def turn_clockwise(self):
        new_contents = [self.__inverted_column(
            i) for i in range(len(self.contents))]
        self.contents = new_contents
        self.__compute_edges()

    def get_without_borders(self):
        new_contents = [''.join(self.contents[i][1:-1])
                        for i in range(1, len(self.contents)-1)]
        return Tile(10*self.num, new_contents)

    def count_occurrences_of_pattern(self, pattern):
        count = 0
        pattern_row_nr = len(pattern['patterns'])
        pattern_row_length = pattern['row_length']
        for row_index in range(len(self.contents)-pattern_row_nr+1):
            for col_index in range(len(self.contents[row_index])-pattern_row_length+1):
                if self.__pattern_starts_at(row_index, col_index, pattern):
                    count += 1
        return count

    def __pattern_starts_at(self, row_index, col_index, pattern):
        pattern_row_length = pattern['row_length']
        row_patterns = pattern['patterns']
        for pattern_row_ind, pattern_row in enumerate(row_patterns):
            line_section = self.contents[row_index +
                                         pattern_row_ind][col_index:col_index + pattern_row_length]
            if not all([line_section[pos] == '#' for pos in pattern_row]):
                return False
        return True

    def __inverted_column(self, i):
        column = self.__column_i(i)
        return column[::-1]

    def __column_i(self, i):
        return ''.join([row[i] for row in self.contents])

    def __compute_edges(self):
        top_edge = ''.join(self.contents[0])
        bottom_edge = ''.join(self.contents[-1])
        left_edge = ''.join([line[0] for line in self.contents])
        right_edge = ''.join([line[-1] for line in self.contents])
        self.edges = {'top': top_edge, 'right': right_edge,
                      'left': left_edge, 'bottom': bottom_edge}

    def __compute_possible_edges(self):
        new_edges = [edge[::-1] for edge in self.edges.values()]
        self.possible_edges = list(self.edges.values()) + new_edges

    def __str__(self):
        return '\n'.join(self.contents)

    def has_edge_in_common(self, dirs, tiles):
        for tile in tiles:
            if tile.num != self.num:
                for dir in dirs:
                    if tile.has_possible_edge(self.edges[dir]):
                        return True
        return False


class TileArrangement:
    def __init__(self, width, length, tiles):
        self.arrangement = [
            [None for _ in range(width)] for _ in range(length)]
        self.tiles = tiles
        self.used_tiles = []
        self.width = width
        self.length = length
        self.__compute_all_possible_tile_neighbors()

    def arrange_tiles(self):
        corner_tiles = self.get_corner_tiles()
        self.__put_top_left_corner(corner_tiles[0])
        self.__arrange_rest_tiles()

    def __put_top_left_corner(self, tile):
        while tile.has_edge_in_common(['top', 'left'], self.tiles):
            tile.turn_clockwise()
        self.__put_tile_at_pos(0, 0, tile)

    def __arrange_rest_tiles(self):
        for position in range(1, len(self.arrangement[0])):
            self.fill_position(0, position)
        for row in range(1, len(self.arrangement)):
            for column in range(len(self.arrangement[row])):
                self.fill_position(row, column)

    def fill_position(self, row, column):
        available_tiles = [
            t for t in self.tiles if t.num not in self.used_tiles]
        for tile in available_tiles:
            self.__try_all_constellations_for_pos(tile, row, column)
            if not self.arrangement[row][column] is None:
                return

    def __try_all_constellations_for_pos(self, tile, row, col):
        if self.__tile_fits_at_position(row, col, tile):
            self.__put_tile_at_pos(row, col, tile)
            return
        for _ in range(3):
            tile.turn_clockwise()
            if self.__tile_fits_at_position(row, col, tile):
                self.__put_tile_at_pos(row, col, tile)
                return
        tile.mirror_vertically()
        if self.__tile_fits_at_position(row, col, tile):
            self.__put_tile_at_pos(row, col, tile)
            return
        for _ in range(3):
            tile.turn_clockwise()
            if self.__tile_fits_at_position(row, col, tile):
                self.__put_tile_at_pos(row, col, tile)
                return

    def __put_tile_at_pos(self, row, column, tile):
        self.arrangement[row][column] = tile
        self.used_tiles.append(tile.num)

    def __tile_fits_at_position(self, row, column, tile):
        return (self.__tile_fits_to_side(tile, 'left', row, column + 1)
                and self.__tile_fits_to_side(tile, 'right', row, column - 1)
                and self.__tile_fits_to_side(tile, 'bottom', row - 1, column)
                and self.__tile_fits_to_side(tile, 'top', row+1, column))

    def __tile_fits_to_side(self, tile, side, side_row, side_column):
        if 0 <= side_row < len(self.arrangement):
            if 0 <= side_column < len(self.arrangement[0]):
                neighbor_tile = self.arrangement[side_row][side_column]
                if neighbor_tile:
                    return neighbor_tile.tile_fits_at_position(tile, side)
        return True

    def as_tile(self):
        contents = []
        for row in self.arrangement:
            new_lines = self.__fuse_tile_row(row)
            contents += new_lines
        return Tile(0, contents)

    def get_as_tile_without_tile_borders(self):
        tile_arrangement = [[tile.get_without_borders() for tile in row]
                            for row in self.arrangement]
        new_tiles = [tile.get_without_borders() for tile in self.tiles]
        arr = TileArrangement(self.width, self.length, new_tiles)
        arr.arrangement = tile_arrangement
        return arr.as_tile()

    def __fuse_tile_row(self, row):
        lines = []
        for i in range(len(row[0].contents)):
            line = ''.join([''.join(tile.contents[i]) for tile in row])
            lines.append(line)
        return lines

    def __str__(self):
        return str(self.as_tile())

    def __compute_all_possible_tile_neighbors(self):
        for i, tile1 in enumerate(self.tiles):
            for tile2 in self.tiles[i+1:]:
                if tile1.has_edges_in_common_with(tile2):
                    tile1.possible_neighbors.append(tile2)
                    tile2.possible_neighbors.append(tile1)

    def __find_tiles_with_neighbor_num(self, neighbor_num):
        res_tiles = []
        for tile in self.tiles:
            if len(tile.possible_neighbors) == neighbor_num:
                res_tiles.append(tile)
        return res_tiles

    def get_corner_tiles(self):
        return self.__find_tiles_with_neighbor_num(2)

    def get_edge_tiles(self):
        return self.__find_tiles_with_neighbor_num(3)


def part01(text):
    arrangement = parse_arrangement(text)
    corner_tiles = arrangement.get_corner_tiles()
    corner_tiles_numbers = [tile.num for tile in corner_tiles]
    res = prod(corner_tiles_numbers)
    print('Part 1:', res)


def parse_arrangement(text):
    tiles = parse_input(text)
    arrangement = build_square_tile_arrangement(tiles)
    return arrangement


def build_square_tile_arrangement(tiles):
    width = int(sqrt(len(tiles)))
    arrangement = TileArrangement(width, width, tiles)
    return arrangement


def parse_tile_data(tile_text):
    tile_lines = tile_text.split('\n')
    tile_num = int(tile_lines[0][5:9])
    tile_contents = tile_lines[1:]
    return Tile(tile_num, tile_contents)


def parse_input(text):
    all_tile_data = text.split('\n\n')
    tiles = []
    num_to_tile = {}
    for tile_data in all_tile_data:
        tile = parse_tile_data(tile_data)
        tiles.append(tile)
        num_to_tile[tile.num] = tile
    return tiles


def part02(text):
    arrangement = parse_arrangement(text)
    arrangement.arrange_tiles()
    big_tile_no_borders = arrangement.get_as_tile_without_tile_borders()
    seamonster_count = count_seamonsters_in_tile(big_tile_no_borders)
    hashtag_count = big_tile_no_borders.count_occurrences_of_pattern(
        HASHTAG_PATTERN)
    print('Part 2:', hashtag_count - seamonster_count*15)


def count_seamonsters_in_tile(tile):
    counts = []
    counts.append(tile.count_occurrences_of_pattern(SEAMONSTER_PATTERN))
    for _ in range(3):
        tile.turn_clockwise()
        counts.append(tile.count_occurrences_of_pattern(SEAMONSTER_PATTERN))
    tile.mirror_vertically()
    counts.append(tile.count_occurrences_of_pattern(SEAMONSTER_PATTERN))
    for _ in range(3):
        tile.turn_clockwise()
        counts.append(tile.count_occurrences_of_pattern(SEAMONSTER_PATTERN))
    seamonster_count = max(counts)
    return seamonster_count


if __name__ == '__main__':
    text = read_file_contents('day20.txt')
    part01(text)
    part02(text)
