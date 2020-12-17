from input_utils import get_input_file_lines_no_nl
from itertools import combinations_with_replacement, permutations
from copy import deepcopy

ACTIVE = '#'
INACTIVE = '.'


class Point:
    def __init__(self, coords):
        self.coords = coords
        self.dim = len(coords)

    def elevate(self, new_coord):
        return Point(self.coords + [new_coord])

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        if other.dim != self.dim:
            return False
        return other.coords == self.coords

    def __add__(self, other):
        if not isinstance(other, Point):
            raise ValueError('Object is not a point!')
        if other.dim != self.dim:
            raise ValueError('Dimensions are different!')
        else:
            new_coords = [self.coords[i] + other.coords[i]
                          for i in range(len(self.coords))]
            return Point(new_coords)

    def __str__(self):
        return str(tuple(self.coords))

    def __repr__(self):
        return 'Point' + str(tuple(self.coords))

    def __hash__(self):
        return str(self).__hash__()


class Cube:
    def __init__(self, active):
        self.active = active

    def at_point(self, point):
        if point.dim > 0:
            raise ValueError('Dimension zero expected.')
        else:
            return self

    def is_active_at_point(self, point):
        return self.at_point(point) == ACTIVE

    def is_active(self):
        return self.active

    def make_inactive_like(self):
        return Cube(False)

    def count_active(self):
        if self.active:
            return 1
        return 0

    def __str__(self):
        if self.active:
            return '#'
        return '.'


class CubeSpace:
    def __init__(self, space, dim):
        if space:
            self.space = self.turn_to_subspaces(space, dim)
        else:
            self.space = space
        self.dim = dim

    def at_point(self, point):
        if point.dim != self.dim:
            raise ValueError('Invalid dimension')
        if 0 <= point.coords[0] < len(self.space):
            return self.space[point.coords[0]].at_point(Point(point.coords[1:]))
        return None

    def is_active_at_point(self, point):
        cube = self.at_point(point)
        if cube:
            return cube.is_active()
        return False

    def count_active_around_point(self, point):
        surrounding_points = self.compute_surrounding_points(point)
        active_count = 0
        for p in surrounding_points:
            if self.is_active_at_point(p):
                active_count += 1
        return active_count

    def compute_surrounding_points(self, point):
        point_changes = set()
        partial_points = {Point([0]), Point([-1]), Point([1])}
        for _ in range(self.dim-1):
            new_partials = set()
            for next_change in [-1, 0, 1]:
                for partial_point in partial_points:
                    new_partials.add(partial_point.elevate(next_change))
            partial_points = new_partials
        point_changes = partial_points - set([Point([0] * point.dim)])
        return [point + p for p in point_changes]

    def make_inactive_like(self):
        if self.dim == 1:
            return CubeSpace([INACTIVE for _ in self.space], 1)
        tmp = CubeSpace([], self.dim)
        tmp.space = [subspace.make_inactive_like() for subspace in self.space]
        return tmp

    def turn_to_cube_space(self, cube_space_list, dim):
        tmp = CubeSpace([], dim)
        if dim == 1:
            tmp.space = [Cube(x == ACTIVE) for x in cube_space_list]
        else:
            tmp.space = [self.turn_to_cube_space(
                subspace, dim - 1) for subspace in cube_space_list]
        return tmp

    def turn_to_subspaces(self, cube_space_list, dim):
        if dim == 1:
            return [Cube(x == ACTIVE) for x in cube_space_list]
        else:
            return [self.turn_to_cube_space(subspace, dim - 1) for subspace in cube_space_list]

    def count_active(self):
        if self.dim == 1:
            return sum([1 for cube in self.space if cube.active])
        else:
            return sum([subspace.count_active() for subspace in self.space])

    def surround_by_inactive(self):
        tmp = CubeSpace([], self.dim)
        if self.dim == 1:
            new_subspace = [Cube(False)] + \
                [x for x in self.space] + [Cube(False)]
            tmp.space = new_subspace
        else:
            new_subspace = [subspace.surround_by_inactive()
                            for subspace in self.space]
            new_subspace = [new_subspace[0].make_inactive_like(
            )] + new_subspace + [new_subspace[0].make_inactive_like()]
            tmp.space = new_subspace
        return tmp

    def make_point_active(self, point):
        self.at_point(point).active = True

    def make_point_inactive(self, point):
        self.at_point(point).active = False

    def get_points(self, partial=[]):
        if partial:
            extended_partials = [p.elevate(i) for i in range(
                len(self.space)) for p in partial]
        else:
            extended_partials = [Point([i]) for i in range(
                len(self.space))]

        if self.dim == 1:
            return extended_partials
        else:
            ret = []
            for subspace in self.space:
                ret += subspace.get_points(extended_partials)
            return ret

    def __str__(self):
        if self.dim == 2:
            return '\n'.join([str(subspace) for subspace in self.space])
        elif self.dim == 1:
            return ''.join([str(cube) for cube in self.space])
        else:
            ret = ''
            for index, subspace in enumerate(self.space):
                ret += str(index)+':\n' + str(subspace) + '\n'
            return ret


def print_cube_space(cube_space):
    for z in range(len(cube_space)):
        plane = cube_space[z]
        plane_string = ''
        for line in plane:
            plane_string += ''.join(line) + '\n'
        print(f'z={z}:\n{plane_string}')


def surround_by_inactive(cube_space):
    new_space = []
    for plane in cube_space:
        new_space.append(surround_plane_by_inactive(plane))
    new_space = [make_inactive_plane_like(
        new_space[0])] + new_space + [make_inactive_plane_like(new_space[0])]
    return new_space


def make_inactive_plane_like(plane):
    result_plane = [[INACTIVE for x in line] for line in plane]
    return result_plane


def surround_plane_by_inactive(plane):
    new_plane = []
    for line in plane:
        new_plane.append(surround_line_by_inactive(line))
    y_len = len(new_plane[0])
    new_plane = [[INACTIVE] * y_len] + new_plane + [[INACTIVE] * y_len]
    return new_plane


def surround_line_by_inactive(line):
    return [INACTIVE] + line + [INACTIVE]


def get_surrounding_points(x, y, z):
    points = []
    for x_c in [-1, 0, 1]:
        for y_c in [-1, 0, 1]:
            for z_c in [-1, 0, 1]:
                new_point = (x + x_c, y + y_c, z + z_c)
                if not ((x_c, y_c, z_c) == (0, 0, 0)):
                    points.append(new_point)
    return points


def count_surrounding_active(x, y, z, cube_space):
    active_count = 0
    surrounding_points = get_surrounding_points(x, y, z)
    for x_c, y_c, z_c in surrounding_points:
        if cube_space_is_active_at(cube_space, x_c, y_c, z_c):
            # print(f'active around {(x,y,z)}:', (x_c, y_c, z_c))
            active_count += 1
    return active_count


def cube_space_is_active_at(cube_space, x, y, z):
    if z < len(cube_space) and y < len(cube_space[z]) and x < len(cube_space[z][y]):
        return cube_space[z][y][x] == ACTIVE
    return False


def simulate_cubes(cube_space, iterations=6):
    current_cube_space = cube_space
    # print('Initial cube space:--------------------------------')
    # print_cube_space(current_cube_space)
    for _ in range(iterations):
        current_cube_space = surround_by_inactive(current_cube_space)
        current_cube_space = simulate_iteration(current_cube_space)
        # print(f'after iteration {i+1}--------------------------------')
        # print_cube_space(current_cube_space)

    return current_cube_space


def compute_next_state_at(cube_space, x, y, z):
    surrounding_active_count = count_surrounding_active(x, y, z, cube_space)
    if cube_space[z][y][x] == ACTIVE:
        if surrounding_active_count in [2, 3]:
            return ACTIVE
    else:
        if surrounding_active_count == 3:
            return ACTIVE
    return INACTIVE


def simulate_iteration(cube_space):
    new_cube_space = []
    for z in range(len(cube_space)):
        new_plane = []
        for y in range(len(cube_space[z])):
            new_line = []
            for x in range(len(cube_space[z][y])):
                new_line.append(compute_next_state_at(cube_space, x, y, z))
            new_plane.append(new_line)
        new_cube_space.append(new_plane)
    return new_cube_space


def count_active_in_cube_space(cube_space):
    active_count = 0
    for plane in cube_space:
        for line in plane:
            for cube in line:
                if cube == ACTIVE:
                    active_count += 1
    return active_count


def simulate_cubes_general(cube_space, iterations=6):
    current_cube_space = cube_space
    #print('Initial cube space:--------------------------------')
    # print(current_cube_space)
    for i in range(iterations):
        print(f'Iteration {i}')
        current_cube_space = current_cube_space.surround_by_inactive()
        current_cube_space = simulate_iteration_general(current_cube_space)
        #print(f'after iteration {i+1}--------------------------------')
        # print(current_cube_space)

    return current_cube_space


def simulate_iteration_general(cube_space):
    active_points = []
    inactive_points = []
    for point in cube_space.get_points():
        if cube_space.is_active_at_point(point):
            if cube_space.count_active_around_point(point) in [2, 3]:
                active_points.append(point)
            else:
                inactive_points.append(point)
        else:
            if cube_space.count_active_around_point(point) == 3:
                active_points.append(point)
    for active in active_points:
        cube_space.make_point_active(active)
    for inactive in inactive_points:
        cube_space.make_point_inactive(inactive)
    return cube_space


def part01(lines):
    cube_space = parse_config(lines, 3)
    simulated_cube_space = simulate_cubes(cube_space, 6)
    active_count = count_active_in_cube_space(simulated_cube_space)
    print('part 1:', active_count)


def part01_general(lines):
    cube_space_list = parse_config(lines, 3)
    cube_space = CubeSpace(cube_space_list, 3)
    simulated_cube_space = simulate_cubes_general(cube_space, 6)
    print('part 1:', simulated_cube_space.count_active())


def part02(lines):
    cube_space_list = parse_config(lines, 4)
    cube_space = CubeSpace(cube_space_list, 4)
    simulated_cube_space = simulate_cubes_general(cube_space, 6)
    print('part 2:', simulated_cube_space.count_active())


def parse_config(lines, dims=3):
    layer = [[mark for mark in line] for line in lines]
    ret = layer
    for _ in range(dims-2):
        ret = [ret]
    return ret


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day17_test.txt')
    '''
    cube_space_list = parse_config(lines, 3)
    cube_space = CubeSpace(cube_space_list, 3)
    print(cube_space)
    print('active:', cube_space.count_active())
    cube_space = cube_space.surround_by_inactive()
    print('surrounded by inactive-----------------')
    print(cube_space)
    print(cube_space.count_active_around_point(Point([0, 4, 2])))
    print('active:', cube_space.count_active())'''

    # cube_space = surround_by_inactive(parse_config(lines))
    # print_cube_space(cube_space)
    # print(count_surrounding_active(2, 4, 0, cube_space))
    # part01_general(lines)
    part02(lines)
