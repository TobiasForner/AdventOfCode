from input_utils import get_input_file_lines_no_nl

ACTIVE = '#'


class Point:
    def __init__(self, coords):
        self.coords = coords
        self.dim = len(coords)

    def elevate(self, new_coord):
        return Point(self.coords + [new_coord])

    def get_surrounding_points(self):
        point_changes = set()
        partial_point_changes = {Point([0]), Point([-1]), Point([1])}
        for _ in range(self.dim-1):
            new_partials = set()
            for next_change in [-1, 0, 1]:
                for partial_point in partial_point_changes:
                    new_partials.add(partial_point.elevate(next_change))
            partial_point_changes = new_partials
        point_changes = partial_point_changes - set([Point([0] * self.dim)])
        return {self + p for p in point_changes}

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


def cube_is_active_after_iteration(active_cubes, point):
    if point in active_cubes:
        if len(active_cubes.intersection(point.get_surrounding_points())) in [2, 3]:
            return True
        else:
            return False
    else:
        if len(active_cubes.intersection(point.get_surrounding_points())) == 3:
            return True
        else:
            return False


def simulate_cube_iteration(active_cubes):
    new_active_cubes = set()
    potential_next_active = set()
    for active_cube in active_cubes:
        potential_next_active.add(active_cube)
        potential_next_active = potential_next_active.union(
            active_cube.get_surrounding_points())
    for cube in potential_next_active:
        if cube_is_active_after_iteration(active_cubes, cube):
            new_active_cubes.add(cube)
    return new_active_cubes


def simulate_cubes_v3(active_cubes, nr_iterations):
    current_active_cubes = active_cubes
    print(f'Initial active cubes:', len(active_cubes))
    for _ in range(nr_iterations):
        current_active_cubes = simulate_cube_iteration(current_active_cubes)
        print(f'active cubes:', len(current_active_cubes))
    return current_active_cubes


def part01_v3(lines):
    active_cubes = parse_active_points(lines, 3)
    active_cubes_end = simulate_cubes_v3(active_cubes, 6)
    print('Part 1:', len(active_cubes_end))


def part02_v3(lines):
    active_cubes = parse_active_points(lines, 4)
    active_cubes_end = simulate_cubes_v3(active_cubes, 6)
    print('Part 2:', len(active_cubes_end))


def parse_active_points(lines, dimensions=3):
    active_set = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ACTIVE:
                coords = [x, y] + [0] * (dimensions-2)
                point = Point(coords)
                active_set.add(point)
    return active_set


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day17.txt')
    part01_v3(lines)
    part02_v3(lines)
