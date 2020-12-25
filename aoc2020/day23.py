from copy import deepcopy
from math import prod
from time import perf_counter


class CircularListArray:
    def __init__(self, length):
        self.start = None
        self.end = None
        self.value_list = [None for _ in range(length)]

    def add_value(self, value):
        if self.end:
            self.value_list[self.end] = value
            self.value_list[value] = self.start
            self.end = value
        else:
            self.start = value
            self.end = value
            self.value_list[value] = value

    def extract_three_after_val(self, value):
        return self.extract_n_after_val(3, value)

    def extract_n_after_val(self, n, value):
        extracted = []
        current_value = value
        for _ in range(n):
            current_value = self.value_list[current_value]
            extracted.append(current_value)
        if self.end in extracted:
            self.end = value
        if self.start in extracted:
            self.start = self.value_list[extracted[-1]]
            self.value_list[self.end] = self.start
        self.value_list[value] = self.value_list[current_value]
        return extracted

    def value_right_of_val(self, val):
        return self.value_list[val]

    def insert_three_after_val(self, value, three):
        after_value = self.value_list[value]
        current_node = value
        for val in three:
            self.value_list[current_node] = val
            current_node = val
        self.value_list[current_node] = after_value
        if value == self.end:
            self.end = three[-1]

    def insert_three_after_val_unsafe(self, value, three):
        after_value = self.value_list[value]
        self.value_list[value] = three[0]
        self.value_list[three[-1]] = after_value

    def get_start_value(self):
        return self.start

    def __str__(self):
        as_list = [self.start]
        curr_val = self.start
        while curr_val != self.end:
            curr_val = self.value_list[curr_val]
            as_list.append(curr_val)
        return str(as_list)


class CupArrangement:
    def __init__(self, cups, min_cup, max_cup, verbose=False):
        self.cups = cups
        self.active_cup = cups.get_start_value()
        self.max_cup = max_cup
        self.min_cup = min_cup
        self.verbose = verbose

    def simulate(self, rounds=100):
        for i in range(rounds):
            if self.verbose and i % 100000 == 0:
                print('Iteration', i)
            self.__perform_round()

    def __perform_round(self):
        three_cups = self.__extract_three_right()
        dest_cup = self.__find_destination_cup(three_cups)
        self.cups.insert_three_after_val(dest_cup, three_cups)
        self.__select_new_active_cup()

    def __extract_three_right(self):
        return self.cups.extract_three_after_val(self.active_cup)

    def __find_destination_cup(self, three):
        cup = self.active_cup-1
        while cup in three or not (self.min_cup <= cup <= self.max_cup):
            if cup <= 1:
                cup = self.max_cup
            else:
                cup -= 1
        return cup

    def __select_new_active_cup(self):
        self.active_cup = self.cups.value_right_of_val(self.active_cup)


def arrange_circular_array(cups, start, end):
    length = len(cups) + end - start+1  # add one as zero is not a cup value
    circular = CircularListArray(length)
    for cup in cups:
        circular.add_value(cup)
    for cup in range(start, end):
        circular.add_value(cup)
    return circular


def part01(cups, nr_sim=100):
    circular = arrange_circular_array(cups, 0, 0)
    cup_arrangement = CupArrangement(circular, 1, 9)
    cup_arrangement.simulate(nr_sim)
    final_cups = cup_arrangement.cups
    after_one = final_cups.extract_n_after_val(8, 1)
    result = ''.join([str(x) for x in after_one])
    print('Part 1:', result)
    return result


def part02(cups):
    circular = arrange_circular_array(cups, 10, 1000001)
    cup_arrangement = CupArrangement(circular, 1, 1000000)
    start = perf_counter()
    cup_arrangement.simulate(10000000)
    final_cups = cup_arrangement.cups
    right_two = final_cups.extract_n_after_val(2, 1)
    result = prod(right_two)
    end = perf_counter()
    print('Part 2:', result, 'time:', end-start)


if __name__ == '__main__':
    cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    #cups = [int(x) for x in '364297581']
    part01(cups)
    part02(cups)
