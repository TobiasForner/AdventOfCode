from functools import reduce

from input_utils import get_input_file_lines


def get_groups(lines):
    groups = []
    curr_group = ''
    for line in lines:
        if not any([c.isalpha() for c in line]):
            groups.append(curr_group)
            curr_group = ''
        else:
            if curr_group:
                curr_group += ','
            curr_group += line.replace('\n', '')
    if curr_group:
        groups.append(curr_group)
    return groups


def count_answers(groups):
    return sum([len(set([c for c in g if c != ','])) for g in groups])


def count_questions_all_yes(groups):
    def count_all_yes_per_group(group):
        group_sets = [set([c for c in x]) for x in group.split(',')]
        return len(reduce(lambda x, y: x.intersection(y), group_sets))
    return sum([count_all_yes_per_group(g) for g in groups])


if __name__ == '__main__':
    part = 2
    count_method = {1: count_answers, 2: count_questions_all_yes}
    lines = get_input_file_lines('day06_answers.txt')
    groups = get_groups(lines)
    answers = count_method[part](groups)
    print(f'{answers} answers')
