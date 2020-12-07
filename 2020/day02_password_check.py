import os

def is_correct_ver1(entry):
        return entry['pattern']['min'] <= entry['pw'].count(entry['pattern']['char']) <= entry['pattern']['max']

def is_correct_ver2(entry):
        return (entry['pw'][entry['pattern']['min'] - 1] ==entry['pattern']['char']) ^ (entry['pw'][entry['pattern']['max'] - 1] ==entry['pattern']['char'])

def gen_patterns_passwords(lines):
    res = []
    for line in lines:
        pattern, pw = line.split(': ')
        min_count, rest = pattern.split('-')
        max_count, char = rest.split(' ')
        res.append({'pattern':{'min': int(min_count), 'max': int(max_count), 'char': char}, 'pw': pw})
    return res

def count_correct_pw(patterns_pw_dict, is_correct):    
    return sum([1 for x in patterns_pw_dict if is_correct(x)])

if __name__ == '__main__':
    part = 2
    correct_checkers = [is_correct_ver1, is_correct_ver2]
    rel_path = os.path.join('2020', 'inputs', 'day02_passwords.txt')
    my_path = os.getcwd()
    path = os.path.join(my_path, rel_path)
    with open(path) as file:
        patterns_passwords = gen_patterns_passwords(file.readlines())
        print('correct:', count_correct_pw(patterns_passwords, correct_checkers[part-1]))