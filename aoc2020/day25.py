from aoc2020.input_utils import get_input_file_lines_no_nl

CARD_PUBLIC_KEY = 15733400
DOOR_PUBLIC_KEY = 6408062


def transform_subject_number(subject_number, loop_size, init_value=1):
    value = init_value
    for _ in range(loop_size):
        value = value * subject_number
        value = value % 20201227
    return value


def figure_out_loop_size(public_key, subject_number):
    loop_size = 0
    value = 1
    while value != public_key:
        value = transform_subject_number(subject_number, 1, value)
        loop_size += 1
    return loop_size


def find_encryption_key(card_public_key, door_public_key):
    card_loop_size = figure_out_loop_size(card_public_key, 7)
    door_loop_size = figure_out_loop_size(door_public_key, 7)
    encryption_key = transform_subject_number(card_public_key, door_loop_size)
    print(
        f'card loop size: {card_loop_size}, door loop size: {door_loop_size}, encryption key: {encryption_key}')
    return encryption_key


def part01():
    find_encryption_key(CARD_PUBLIC_KEY, DOOR_PUBLIC_KEY)


if __name__ == '__main__':
    part01()
