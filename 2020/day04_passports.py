import os 
from string import ascii_lowercase
from input_utils import get_input_file_lines

def get_batches(lines, verbose = False):
    current_batch = ''
    batches = []
    def append_dict():
        pairs = current_batch.split(' ')
        if verbose:
            print(pairs)
        d={}
        for x in pairs:
            if x:
                a,b = x.split(':')
                d[a]=b
        batches.append(d)
            
    for line in lines:
        line = line.replace('\n', ' ')
        #print(f'line:|{line}|' )
        if not any([c.isalpha() for c in line]):
            append_dict()
            current_batch = '' 
        else:
            current_batch += line
    if current_batch:
        append_dict()
    return batches

def byr_correct(pp):
    byr = pp['byr']
    return byr.isnumeric() and 1920 <= int(byr) <= 2002

def iyr_correct(pp):
    iyr = pp['iyr']
    return iyr.isnumeric() and 2010 <= int(iyr) <= 2020

def eyr_correct(pp):
    eyr = pp['eyr']
    return eyr.isnumeric() and 2020 <= int(eyr) <= 2030

def hgt_correct(pp):
    hgt = pp['hgt']
    if(len(hgt)<3):
        return False
    measure = hgt[-2:]
    value = hgt[:-2]
    if measure not in ['cm', 'in'] or not value.isnumeric():
        return False
    bounds = {'cm': (150, 193), 'in': (59, 76)}
    return bounds[measure][0] <= int(value) <= bounds[measure][1] 

def hcl_correct(pp):
    hcl = pp['hcl']
    if len(hcl) != 7 or hcl[0]!='#':
        return False
    return all([c in '0123456789' + ascii_lowercase for c in hcl[1:]])

def ecl_correct(pp):
    ecl = pp['ecl']
    return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def pid_correct(pp):
    pid = pp['pid']
    return len(pid) == 9 and pid.isnumeric()

def pp_correct(pp):
    return all([byr_correct(pp), iyr_correct(pp), eyr_correct(pp), hgt_correct(pp), hcl_correct(pp), ecl_correct(pp), pid_correct(pp)])


def valid_count(batches, fields, optional={'cid'}):
    valid = 0
    for b in batches:
        key_set = set(b.keys())-set([''])
        if not (fields - key_set).issubset( optional):
            continue
        if pp_correct(b):
            valid += 1
    return valid, len(batches)


if __name__ == '__main__':
    part = 1
    fields = [set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])]
    batches = get_batches(get_input_file_lines('day04_passports.txt'))
    print('valid:', valid_count(batches, fields[part-1]))