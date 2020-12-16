from input_utils import get_input_file_lines_no_nl
import re


def get_info(lines):
    own_line = 0
    bounds = {}
    for index, l in enumerate(lines):
        if l == 'your ticket:':
            own_line = index + 1
            break
        if not any([x.isalpha() for x in l]):
            continue
        m = re.search(r'([a-z\s]+): (\d+-\d+)(?: or (\d+-\d+))', l)
        var_name, *bounds = m.groups()
        var_bounds = []
        for b in bounds:
            lower, upper = b.split('-')
            var_bounds.append((int(lower), int(upper)))
        bounds[var_name] = var_bounds
    own_ticket_nums = [int(x) for x in lines[own_line].split(',')]
    nearby_ticket_nums = []
    for l in lines[own_line+1:]:
        if not any([x.isnumeric() for x in l]):
            continue
        nearby_ticket_nums.append([int(x) for x in l.split(',')])
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
    print(bounds)
    valid_tickets = []
    for ticket in nearby_ticket_nums:
        valid = True
        for num in ticket:
            if not is_within_bounds(num, bounds):
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
