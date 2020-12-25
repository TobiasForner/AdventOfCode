from aoc2020.input_utils import read_file_contents
from functools import reduce


class Game:
    def __init__(self, stack1, stack2, game_num=1, verbose=False):
        self.stack1 = stack1
        self.stack2 = stack2
        self._verbose = verbose
        self.num = game_num
        self.winner = None

    def play(self):
        while not self.winner:
            self.__play_turn()
            self._check_winner()

    def __play_turn(self):
        if self._verbose:
            self._print_round()
        round_winner = self._determine_round_winner()
        self._modify_stacks(round_winner)

    def _modify_stacks(self, round_winner):
        if round_winner == 1:
            self._player1_wins_turn()
        elif round_winner == 2:
            self._player2_wins_turn()

    def _check_winner(self):
        if not self.stack1:
            self.winner = 2
        if not self.stack2:
            self.winner = 1

    def _print_round(self):
        print('------------------')
        print(self)
        print(f'Player 1 plays : {self.stack1[0]}')
        print(f'Player 2 plays : {self.stack2[0]}')

    def _player1_wins_turn(self):
        self.stack1 = self.stack1[1:] + [self.stack1[0], self.stack2[0]]
        self.stack2 = self.stack2[1:]

    def _player2_wins_turn(self):
        self.stack2 = self.stack2[1:] + [self.stack2[0], self.stack1[0]]
        self.stack1 = self.stack1[1:]

    def get_score(self):
        if self.winner == 1:
            return self.__calculate_score(self.stack1)
        elif self.winner == 2:
            return self.__calculate_score(self.stack2)
        else:
            raise RuntimeError('There is no winner yet')

    def get_winner(self):
        return self.winner

    def _determine_round_winner(self):
        if self.stack1[0] > self.stack2[0]:
            round_winner = 1
        elif self.stack1[0] < self.stack2[0]:
            round_winner = 2
        else:
            raise ValueError('Input resulted in a draw round!')
        return round_winner

    def __calculate_score(self, stack):
        score = 0
        for position, number in enumerate(stack):
            score += number * (len(stack) - position)
        return score

    def __str__(self):
        return f'Player 1: {self.stack1}\nPlayer 2: {self.stack2}'


class RecursiveCombat(Game):
    played_games_to_end = {}
    games_finished = 0

    def __init__(self, stack1, stack2, verbose=False):
        super().__init__(stack1, stack2, verbose)

        self.winner = None
        self.score = None
        self.rounds = set()
        self.round_count = 0

    def play(self):
        while not self.winner:
            self.__play_turn()
            self._check_winner()
            if str(self) in RecursiveCombat.played_games_to_end:
                self.winner = RecursiveCombat.played_games_to_end[str(self)]
        for round in self.rounds:
            RecursiveCombat.played_games_to_end[round] = self.winner
        RecursiveCombat.games_finished += 1
        if self._verbose and RecursiveCombat.games_finished % 100000 == 0:
            print(f'{RecursiveCombat.games_finished} games finished')

    def __play_turn(self):
        self.round_count += 1
        if self._verbose:
            self._print_round()
        if self.fulfills_infinite_prevention_rule():
            self.winner = 1
        else:
            self.rounds.add(str(self))
            round_winner = self.__determine_round_winner_rec()
            self._modify_stacks(round_winner)

    def __determine_round_winner_rec(self):
        if self.__can_recurse():
            round_winner = self.__recurse()
        else:
            round_winner = self._determine_round_winner()
        return round_winner

    def fulfills_infinite_prevention_rule(self):
        return str(self) in self.rounds

    def __can_recurse(self):
        return self.stack1[0] < len(self.stack1) and self.stack2[0] < len(self.stack2)

    def __recurse(self):
        substack1 = self.stack1[1:self.stack1[0]+1]
        substack2 = self.stack2[1:self.stack2[0]+1]
        subgame = RecursiveCombat(substack1, substack2)
        subgame.play()
        return subgame.winner

    def __str__(self):
        return f'Player 1: {self.stack1}\nPlayer 2: {self.stack2}'


def parse_stacks(text):
    text_no_player_info = text.replace(
        'Player 1:\n', '').replace('Player 2:\n', '')
    player_1_stack_text, player_2_stack_text = text_no_player_info.split(
        '\n\n')
    player1_stack = player_1_stack_text.split('\n')
    player2_stack = player_2_stack_text.split('\n')
    return [int(x) for x in player1_stack], [int(x) for x in player2_stack]


def part01(text):
    stacks = parse_stacks(text)
    game = Game(*stacks)
    game.play()
    print('Part 1:', game.get_score())
    return game.get_score()


def part02(text):
    stacks = parse_stacks(text)
    game = RecursiveCombat(*stacks)
    game.play()
    print('Part 2:', game.get_score())
    return game.get_score()


if __name__ == '__main__':
    lines = read_file_contents('day22.txt')
    part01(lines)
    part02(lines)
