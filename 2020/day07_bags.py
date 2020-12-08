from input_utils import get_input_file_lines


def parse_contents(contents):
    def insert_contents(_cdict, s):
        num, bag = s.split(' ', maxsplit=1)
        if(bag[-1] == 's'):
            bag = bag[:-1]
        bag = bag[:-4]
        _cdict[bag] = int(num)
        return _cdict

    contents_dict = {}
    contents = contents.replace('.', '')  # remove . at the end
    if ', ' in contents:
        bags_with_num = contents.split(', ')
        for num_bag in bags_with_num:
            contents_dict = insert_contents(contents_dict, num_bag)
    else:
        if contents == 'no other bags':
            return {}
        contents_dict = insert_contents(contents_dict, contents)
    return contents_dict


def explore_bags(bags, target_bag, contains_target={}):
    def explore_deeper(bag, contents, visited=[]):
        visited.append(bag)
        if target_bag in contents:
            contains_target[bag] = True
            return True
        for b in contents.keys():
            if b in contains_target.keys():
                if contains_target[b]:
                    contains_target[bag] = True
                    return True
            elif b not in visited:
                ret = explore_deeper(b, bags[b], visited)
                if ret:
                    contains_target[bag] = True
                    return True
        contains_target[bag] = False
        return False
    v = []
    for bag, contents in bags.items():
        explore_deeper(bag, contents, v)
        v.append(bag)
    return contains_target


def init_bags(lines):
    bags = {}
    for line in lines:
        line = line.replace('\n', '')
        tmp = line.split(' bags contain ')
        bag, contents = tmp[0], tmp[1]  # line.split('s contain ')
        bags[bag] = parse_contents(contents)
    return bags


def count_inside_bag(bags, target):
    if len(bags[target]) == 0:
        return 0
    else:
        num_bags = 0
        for bag, num in bags[target].items():
            num_bags += num
            num_bags += num * count_inside_bag(bags, bag)
        return num_bags


def part01(bags, target_bag):
    explored_bags = explore_bags(bags, target_bag)
    print(f'part 01: bags containing {target_bag} bag (explore):', sum(
        [1 for x in explored_bags.values() if x]))


if __name__ == '__main__':
    part = 1
    target_bag = 'shiny gold'
    lines = get_input_file_lines('day07_bags.txt')
    initial_bags = init_bags(lines)
    part01(initial_bags, target_bag)
    print('part 02:', count_inside_bag(initial_bags, target_bag))
