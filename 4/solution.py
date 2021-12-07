from dataclasses import dataclass, field
from typing import Sequence, TypeAlias, Type

GRID_DIMENSIONS = 5
Board = list[list[int]]

test_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def read_input(path: str='4/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> tuple[list[int], list[Board]]:
    sequence, _, *lines = input.split('\n')
    sequence_numbers = [int(number) for number in sequence.split(',')]

    boards = []
    board: Board = []
    for row in lines:
        if not row:
            boards.append(board)
            board = []
        else:
            board.append([int(number) for number in row.split()])
    boards.append(board)

    return sequence_numbers, boards

def empty_field(dim: int=GRID_DIMENSIONS) -> list[list[bool]]:
    return [
        [False]*dim for _ in range(GRID_DIMENSIONS)
    ]

@dataclass
class BingoCard():
    numbers_field: list[list[int]]
    marked_field: list[list[bool]] = field(default_factory=empty_field)

    def __post_init__(self):
        numbers = set()

        for i in range(GRID_DIMENSIONS):
            for j in range(GRID_DIMENSIONS):
                numbers.add(self.numbers_field[i][j])

        self.numbers = numbers

    def add_number(self, number: int):
        if number in self.numbers:
            for i in range(GRID_DIMENSIONS):
                for j in range(GRID_DIMENSIONS):
                    if self.numbers_field[i][j] == number:
                        self.marked_field[i][j] = True
                        return

    def check_win(self) -> bool:
        for row_idx, row in enumerate(self.marked_field):
            if all(row):
                return True
            col = [
                self.marked_field[col_idx][row_idx]
                for col_idx in range(GRID_DIMENSIONS)
            ]
            if all(col):
                return True
        return False

    def sum_all_unmarked(self) -> int:
        unmarked_sum = 0
        for i in range(GRID_DIMENSIONS):
            for j in range(GRID_DIMENSIONS):
                if not self.marked_field[i][j]:
                    unmarked_sum += self.numbers_field[i][j]
        return unmarked_sum

def play(sequence: list[int], bingo_cards: list[BingoCard]) -> int:
    for number in sequence:
        for bingo_card in bingo_cards:
            bingo_card.add_number(number)
            if bingo_card.check_win():
                return bingo_card.sum_all_unmarked() * number
    raise RuntimeError('No winning card could be found!')

def play_v2(sequence: list[int], bingo_cards: list[BingoCard]) -> int:
    for number in sequence:
        bingo_cards_not_won = []
        for bingo_card in bingo_cards:
            bingo_card.add_number(number)
            if not bingo_card.check_win():
                bingo_cards_not_won.append(bingo_card)
        # all won, last one winning is current bingo_card
        if len(bingo_cards_not_won) == 0:
            return bingo_card.sum_all_unmarked() * number
        bingo_cards = bingo_cards_not_won
    raise RuntimeError('Not all cards won!')

if __name__=='__main__':
    test_sequence, test_boards = format_input(test_input)
    test_bingo_cards = [
        BingoCard(numbers_field=board) for board in test_boards
    ]
    sequence, boards = format_input(read_input())
    bingo_cards = [
        BingoCard(numbers_field=board) for board in boards
    ]

    # solution 1
    assert play(test_sequence, test_bingo_cards) == 4512
    print(play(sequence, bingo_cards))

    # solution 2
    assert play_v2(test_sequence, test_bingo_cards) == 1924
    print(play_v2(sequence, bingo_cards))
