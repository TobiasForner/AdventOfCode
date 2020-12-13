from input_utils import get_input_file_lines_no_nl
from math import lcm


def get_next_arrival(t, bus):
    arrival = (t//bus) * bus
    if arrival < t:
        arrival += bus
    return arrival


def part01(lines):
    start_time = int(lines[0])

    bus_ints = sorted([(int(t), get_next_arrival(start_time, int(t)))
                       for t in lines[1].split(',') if t != 'x'], key=lambda x: x[1])
    print('part 1:', bus_ints[0][0] *
          (bus_ints[0][1]-start_time), 'id:', bus_ints[0])


def part02(lines, verbose=False):
    bus_ids = lines[1].split(',')
    offsets = [(int(bus_ids[0]), 0)]
    for i, x in enumerate(bus_ids[1:]):
        if x == 'x':
            continue
        else:
            offsets.append((int(x), (i+1) % int(x)))
    offsets = [offsets[0]] + sorted(offsets[1:], key=lambda x: -x[0])
    step_width = offsets[0][0]
    start_pos = 0
    for i in range(1, len(offsets)):
        if verbose:
            print(f'outer iteration {i}: step_width',
                  step_width, ', start pos', start_pos)
        pos = start_pos
        bus, offset = offsets[i]
        while True:
            if get_next_arrival(pos, bus) == offset + pos:
                step_width = lcm(step_width, offsets[i][0])
                start_pos = pos
                break
            else:
                pos += step_width
    print('part 02:', pos)


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day13.txt')
    part01(lines)
    part02(lines)
