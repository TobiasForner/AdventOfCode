from aoc2020.input_utils import get_input_file_lines_no_nl
import re


def parse_bounds(bounds_text):
    bounds = {}
    for line in bounds_text.split('\n'):
        m = re.search(r'([a-z\s]+): (\d+-\d+)(?: or (\d+-\d+))', line)
        var_name, *bound_pairs = m.groups()
        var_bounds = []
        for pair in bound_pairs:
            lower, upper = pair.split('-')
            var_bounds.append((int(lower), int(upper)))
        bounds[var_name] = var_bounds
    return bounds


def parse_nearby_tickets(tickets_text):
    nearby_ticket_nums = []
    for l in tickets_text.split('\n'):
        if not any([x.isnumeric() for x in l]):
            continue
        nearby_ticket_nums.append([int(x) for x in l.split(',')])
    return nearby_ticket_nums


def get_info(lines):
    bounds_text, rest = ('\n'.join(lines)).split('\n\nyour ticket:\n')
    own_nums, other_nums = rest.split('\n\nnearby tickets:\n')
    bounds = parse_bounds(bounds_text)

    own_ticket_nums = [int(x) for x in own_nums.split(',')]
    nearby_ticket_nums = parse_nearby_tickets(other_nums)
    return bounds, own_ticket_nums, nearby_ticket_nums


def fulfills_field_bounds(bounds, field, value):
    for (lower, upper) in bounds[field]:
        if lower <= value <= upper:
            return True
    return False


def is_within_bounds(value, bounds):
    for bound_list in bounds.values():
        for (lower, upper) in bound_list:
            if lower <= value <= upper:
                return True
    return False


def part01(lines, verbose=False):
    bounds, own_ticket_nums, nearby_ticket_nums = get_info(lines)
    error_sum = 0
    valid_tickets = []
    for ticket in nearby_ticket_nums:
        valid = True
        for num in ticket:
            if not is_within_bounds(num, bounds):
                if verbose:
                    print('out of bounds:', num)
                error_sum += num
                valid = False
        if valid:
            valid_tickets.append(ticket)

    print('part 1:', error_sum)
    return bounds, own_ticket_nums, valid_tickets


def part02(bounds, own_ticket_nums, valid_tickets, verbose=False):
    possible_fields_per_pos = [list(bounds.keys())
                               for _ in range(len(own_ticket_nums))]

    # elimination based on ranges
    for i in range(len(possible_fields_per_pos)):
        possible_fields_new = []
        for name in possible_fields_per_pos[i]:
            if all([fulfills_field_bounds(bounds, name, ticket[i]) for ticket in valid_tickets]):
                possible_fields_new.append(name)
        possible_fields_per_pos[i] = possible_fields_new

    # eliminate names that are already assigned to another field
    change = True
    while change:
        change = False
        for index, possible_names in enumerate(possible_fields_per_pos):
            if len(possible_names) == 1:
                for index2, possible_names2 in enumerate(possible_fields_per_pos):
                    if index2 == index:
                        continue
                    if possible_names[0] in possible_names2:
                        change = True
                        possible_fields_per_pos[index2] = [
                            name for name in possible_names2 if name != possible_names[0]]
    if verbose:
        print('possible names per position:', possible_fields_per_pos)
    result = 1
    for i, fields in enumerate(possible_fields_per_pos):
        if re.search(r'^departure', fields[0]):
            result *= own_ticket_nums[i]

    print('part 2:', result)


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day16.txt')
    bounds, own_ticket_nums, valid_tickets = part01(lines)
    part02(bounds, own_ticket_nums, valid_tickets)
