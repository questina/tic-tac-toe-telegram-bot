from enum import Enum
from typing import Union

from game.board import TicTacBoard


class GameStatus(Enum):
    CROSS_WON = 0
    ZERO_WON = 1
    DRAW = 2
    CONTINUE_GAME = 3
    INCORRECT_MOVE = 4


class GameProcessor:
    def __init__(
        self,
        game_board: Union[TicTacBoard, list[list[str]]] = None,
        free_space: str = '.',
        cross: str = 'X',
        zero: str = 'O',
    ) -> None:
        if type(game_board) == TicTacBoard:
            self.game_board = game_board
        else:
            self.game_board = TicTacBoard(game_board, free_space, cross, zero)
        self.finished = False
        if self.game_board.has_win() or not self.game_board.has_place():
            self.finished = True

    def one_round(self, move_pos: Union[tuple[int, int], str]) -> GameStatus:
        if self.finished or not self.game_board.is_correct_move(move_pos):
            return GameStatus.INCORRECT_MOVE
        self.game_board.place(move_pos)
        if self.game_board.has_win():
            self.finished = True
            return GameStatus.CROSS_WON
        if not self.game_board.has_place():
            self.finished = True
            return GameStatus.DRAW
        self.game_board.place_random()
        if self.game_board.has_win():
            self.finished = True
            return GameStatus.ZERO_WON
        if not self.game_board.has_place():
            self.finished = True
            return GameStatus.DRAW
        return GameStatus.CONTINUE_GAME

    @property
    def board(self):
        return self.game_board.board

    def __eq__(self, other):
        return self.game_board == other.game_board

    def __ne__(self, other):
        return not self.__eq__(other)
