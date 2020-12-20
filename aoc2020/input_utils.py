import os


def get_input_file_lines(filename):
    rel_path = os.path.join('aoc2020', 'inputs', filename)
    my_path = os.getcwd()
    path = os.path.join(my_path, rel_path)
    with open(path) as file:
        return file.readlines()


def get_input_file_lines_no_nl(filename):
    return [x.replace('\n', '') for x in get_input_file_lines(filename)]
