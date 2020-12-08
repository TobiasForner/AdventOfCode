from input_utils import get_input_file_lines


def parse_contents(contents):
    contents_dict = {}
    contents = contents[:-1]  # remove . at the end
    if ', ' in contents:
        bags_with_num = contents.split(', ')
        for num_bag in bags_with_num:
            s = num_bag.split(' ')
            num = s[0]
            bag = ' '.join(s[1:])
            if(bag[-1] == 's'):
                bag = bag[:-1]
            contents_dict[bag] = int(num)
    else:
        if contents == 'no other bags':
            return {}
        num, bag = contents.split(' ', maxsplit=1)
        if(bag[-1] == 's'):
            bag = bag[:-1]
        try:
            contents_dict[bag] = int(num)
        except:
            print(f'error: contents |{contents}|')

    return contents_dict


def init_bags(lines):
    bags = {}
    for line in lines:
        line = line.replace('\n', '')
        tmp = line.split('s contain ')
        bag, contents = tmp[0], tmp[1]  # line.split('s contain ')
        bags[bag] = parse_contents(contents)
        '''
        try:
            tmp = line.split('s contain ')
            bag, contents = tmp[0], tmp[1]  # line.split('s contain ')
            bags[bag] = parse_contents(contents)
        except:
            print(f'Error in line|{line}|, split: ', tmp)'''

    return bags


def merge_contents(c1, c2, num):
    merged = {}
    for bag in set(c1.keys()).union(set(c2.keys())):
        merged[bag] = num * c1.get(bag, 0) + c2.get(bag, 0)
    return merged


def expand_contents(contents, bags, target_bag):
    old_contents = []
    while len(old_contents) < len(contents.keys()):
        old_contents = contents.keys()
        for bag in contents:
            num = contents[bag]
            if not num or bag == target_bag:
                continue
            contents[bag] = 0
            contents = merge_contents(bags[bag], contents, num)
    return contents


def expand_bags(bags, target_bag):
    expanded_bags = {}
    for bag, contents in bags.items():
        expanded_bags[bag] = expand_contents(contents, bags, target_bag)
    return expanded_bags


def count_bags_containing(bags, bag):
    count = 0
    for b in bags:
        if bags[b].get(bag, 0) > 0:
            count += 1
    return count


def remove_zeros(bags):
    for bag, contents in bags.items():
        new_contents = {key: val for (key, val) in contents.items() if val > 0}
        bags[bag] = new_contents
    return bags


if __name__ == '__main__':
    part = 1
    target_bag = 'shiny gold bag'
    lines = get_input_file_lines('day07_bags.txt')
    initial_bags = init_bags(lines)
    # print(initial_bags)
    expanded_bags = expand_bags(initial_bags, target_bag)
    print('bags containing shiny gold bag',
          count_bags_containing(expanded_bags, target_bag))
    smaller_bags = remove_zeros(expanded_bags)
    # print(smaller_bags)
