from aoc2020.input_utils import get_input_file_lines_no_nl
import logging
from copy import deepcopy


class CYK():
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.convert_to_cnf()
        self.__cache = {}

    def __call__(self, word):
        if word in self.__cache:
            return self.__cache[word]
        for column in range(len(word)):
            for row in range(column, -1, -1):
                subword = word[row: column + 1]
                self.__compute_cache_entry(subword)
        return self.__cache[word]

    def __compute_cache_entry(self, subword):
        if subword in self.__cache:
            return
        if len(subword) == 1:
            self.__compute_diagonal_cache_entry(subword)
        else:
            self.__compute_non_diagonal_cache_entry(subword)

    def __compute_diagonal_cache_entry(self, subword):
        self.__cache[subword] = self.grammar.get_possible_lhs([subword])

    def __compute_non_diagonal_cache_entry(self, subword):
        cache_entry = set()
        for middle in range(len(subword)-1):
            first_part = subword[:middle+1]
            second_part = subword[middle+1:]
            for nt1 in self.__cache[first_part]:
                for nt2 in self.__cache[second_part]:
                    cache_entry = cache_entry.union(
                        self.grammar.get_possible_lhs([nt1, nt2]))
        self.__cache[subword] = cache_entry


class Grammar():
    def __init__(self, rules, starting_symbol, alphabet):
        self.rules = rules
        self.starting_symbol = starting_symbol
        self.alphabet = alphabet

    def convert_to_cnf(self):
        if self.__is_cnf():
            return
        self.__eliminate_start_symbol_from_rhs()
        self.__remove_single_nonterminal_right_hand_sides()
        self.__isolate_terminal_rules()
        self.__limit_all_rhs_to_length_two()
        if not self.__is_cnf():
            raise RuntimeError('Could not convert to CNF')

    def get_possible_lhs(self, rhs):
        possible_lhs = set()
        for lhs, rhs_list in self.rules.items():
            for rhs_rule in rhs_list:
                if rhs_rule == rhs:
                    possible_lhs.add(lhs)
        return possible_lhs

    def __is_cnf(self):
        if self.__start_symbol_is_in_any_rhs():
            return False
        if self.__contains_rule_with_single_non_terminal_rhs(self.rules):
            return False
        if self.__contains_rhs_larger_two():
            return False
        if self.__contains_wrong_terminal_rule(self.rules):
            return False
        return True

    def __eliminate_start_symbol_from_rhs(self):
        if not self.__start_symbol_is_in_any_rhs():
            return
        new_start_symbol = self.__get_new_nonterminal()
        self.rules[new_start_symbol] = [[self.starting_symbol]]
        self.starting_symbol = new_start_symbol

    def __get_new_nonterminal(self):
        max_lhs = max([int(lhs) for lhs in self.rules])
        return str(max_lhs + 1)

    def __start_symbol_is_in_any_rhs(self):
        for rhs_list in self.rules.values():
            for rhs in rhs_list:
                if self.starting_symbol in rhs:
                    return True
        return False

    def __isolate_terminal_rules(self):
        while self.__contains_wrong_terminal_rule(self.rules):
            self.__perform_terminal_isolation_iteration()

    def __perform_terminal_isolation_iteration(self):
        next_rules = {}
        for lhs, rhs_list in self.rules.items():
            next_rules[lhs] = self.__terminal_isolation_rhs_list(rhs_list)
        self.rules = next_rules

    def __terminal_isolation_rhs_list(self, rhs_list):
        new_rhs_list = []
        for rhs in rhs_list:
            new_rhs_list.append(self.__compute_rhs_without_terminals(rhs))
        return new_rhs_list

    def __compute_rhs_without_terminals(self, rhs):
        new_rhs = []
        for symbol in rhs:
            if symbol in self.alphabet:
                new_non_terminal = self.__get_new_nonterminal()
                self.rules[new_non_terminal] = [[symbol]]
                new_rhs.append(new_non_terminal)
            else:
                new_rhs.append(symbol)
        return new_rhs

    def __contains_rule_with_single_non_terminal_rhs(self, rules):
        for _, rhs_list in rules.items():
            for rhs in rhs_list:
                if self.__rhs_is_single_non_terminal(rhs):
                    return True
        return False

    def __contains_wrong_terminal_rule(self, rules):
        for rhs_list in rules.values():
            for rhs in rhs_list:
                if self.__is_terminal_rule_not_length_1(rhs):
                    return True
        return False

    def __is_terminal_rule_not_length_1(self, rhs):
        if any([terminal in rhs for terminal in self.alphabet]) and len(rhs) > 1:
            return True
        return False

    def __rhs_is_single_non_terminal(self, rhs):
        return len(rhs) == 1 and rhs[0] not in self.alphabet

    def __remove_single_nonterminal_right_hand_sides(self):
        new_rules = self.rules
        while self.__contains_rule_with_single_non_terminal_rhs(new_rules):
            for lhs, rhs_list in new_rules.items():
                new_rhs_list = []
                for rhs in rhs_list:
                    if self.__rhs_is_single_non_terminal(rhs):
                        logging.debug(f'Replacing single {rhs[0]} in rhs')
                        new_rhs_list += new_rules[rhs[0]]
                    else:
                        new_rhs_list.append(rhs)
                new_rules[lhs] = new_rhs_list
        self.rules = new_rules

    def __limit_all_rhs_to_length_two(self):
        while self.__contains_rhs_larger_two():
            old_rules = deepcopy(self.rules)
            for lhs in old_rules:
                self.__limit_rhs_list_length_two(lhs)

    def __limit_rhs_list_length_two(self, lhs):
        new_rhs_list = []
        for rhs in self.rules[lhs]:
            new_rhs_list.append(self.__compute_rhs_at_most_two(rhs))
        self.rules[lhs] = new_rhs_list

    def __compute_rhs_at_most_two(self, rhs):
        if len(rhs) <= 2:
            return rhs
        else:
            new_nonterminal = self.__get_new_nonterminal()
            new_rhs = [rhs[0], new_nonterminal]
            self.rules[new_nonterminal] = [rhs[1:]]
            return new_rhs

    def __contains_rhs_larger_two(self):
        for rhs_list in self.rules.values():
            for rhs in rhs_list:
                if len(rhs) > 2:
                    return True
        return False

    def __str__(self):
        ret = 'Grammar:\nalphabet: ' + ', '.join(self.alphabet)
        ret += '\n'
        ret += f'starting symbol: ' + self.starting_symbol
        ret += '\n'
        ret += self.__turn_rules_to_string()
        return ret

    def __turn_rules_to_string(self):
        rule_strings = []
        for lhs, rhs in self.rules.items():
            rule_str = lhs + ' -> '
            rule_str += ' | '.join([' '.join(r) for r in rhs])
            rule_strings.append(rule_str)
        return '\n'.join(rule_strings)


def parse_option_rhs(rhs):
    rhs_list = rhs.split(' | ')
    rule_rhs = [r.split(' ') for r in rhs_list]
    return rule_rhs


def parse_grammar(grammar_lines):
    rules = {}
    alphabet = []
    for rule in grammar_lines:
        lhs, rhs = rule.split(': ')
        if '\"' in rhs:
            terminal = rhs.replace('\"', '')
            rule_rhs = [[terminal]]
            if terminal not in alphabet:
                alphabet.append(terminal)
        elif '|' in rhs:
            rule_rhs = parse_option_rhs(rhs)
        else:
            rule_rhs = [rhs.split(' ')]
        rules[lhs] = rule_rhs
    return Grammar(rules, '0', alphabet)


def parse_input(lines):
    separation = lines.index('')
    grammar = parse_grammar(lines[:separation])
    words = lines[separation + 1:]
    return grammar, words


def compute_allowed_words(cnf_grammar, words, verbose=False):
    allowed_words = set()
    cyk = CYK(cnf_grammar)
    for index, word in enumerate(words):
        if verbose and index % 1 == 0:
            print(f'word {index}')
        if is_in_language(cnf_grammar, cyk, word):
            allowed_words.add(word)
    return allowed_words


def count_words_in_grammar(cnf_grammar, words, verbose=False):
    cyk = CYK(cnf_grammar)
    count = 0
    for index, word in enumerate(words):
        if verbose and index % 10 == 0:
            print(f'word {index}')
        if is_in_language(cnf_grammar, cyk, word):
            count += 1
    return count


def is_in_language(cnf_grammar, cyk, word):
    symbols = cyk(word)
    return cnf_grammar.starting_symbol in symbols


def part01(lines, verbose=False):
    grammar, words = parse_input(lines)
    grammar.convert_to_cnf()
    count = count_words_in_grammar(grammar, words, verbose)
    print('Part 1:', count)
    return count


def part02(lines, verbose=False):
    grammar, words = parse_input(lines)
    grammar.rules['8'] = [['42'], ['42', '8']]
    grammar.rules['11'] = [['42', '31'], ['42', '11', '31']]
    grammar.convert_to_cnf()
    count = count_words_in_grammar(grammar, words, verbose)
    print('Part 2:', count)
    return count


if __name__ == '__main__':
    logging.basicConfig(filename='day19.log',
                        encoding='utf-8', level=logging.DEBUG)
    lines = get_input_file_lines_no_nl('day19.txt')
    part01(lines, True)
    part02(lines, True)
