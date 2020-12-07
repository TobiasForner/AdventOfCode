import os

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
    #fileDir = os.path.dirname(os.path.realpath('__file__'))
    #script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = os.path.join('2020', 'inputs', 'day01_expense_report.txt')
    my_path = os.getcwd()
    print('path:',my_path)
    path = os.path.join(my_path, rel_path)
    print('joined path:', path)
    with open(path) as file:
        numbers = [int(i) for i in file.readlines()]
        res = get_target_numbers_and_result(numbers, number_count = 3)
        print(f'numbers:{res[0]}, product= {res[1]}')
    