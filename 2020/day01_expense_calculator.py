import os
from input_utils import get_input_file_lines

def get_target_numbers_and_result(numbers, start_number = 0, number_count=2, target_sum=2020, verbose = False):
    for i in range(len(numbers)):
        if verbose and i %10 == 0 and start_number == 0:
            print(i)
        if number_count > 1:
            res = get_target_numbers_and_result(numbers, i + 1, number_count-1, target_sum= target_sum-numbers[i])
            if res:
                return [numbers[i]] + res[0], res[1] * numbers[i]        
        elif numbers[i] == target_sum:
            return [numbers[i]], numbers[i]
        


if __name__ == '__main__':
    numbers = [int(i) for i in get_input_file_lines('day01_expense_report.txt')]
    res = get_target_numbers_and_result(numbers, number_count = 3)
    print(f'numbers:{res[0]}, product= {res[1]}')
    