import random
from typing import Union


class WrongMoveException(Exception):
    ...


class NoMovesException(Exception):
    ...


class TicTacBoard:
    def __init__(
        self,
        board: list[list[str]] = None,
        free_space: str = '.',
        cross: str = 'X',
        zero: str = 'O',
    ) -> None:
        self.free_space = free_space
        self.cross = cross
        self.zero = zero
        if board is not None:
            self.board = board
        else:
            self.board = [[self.free_space for _ in range(3)] for _ in range(3)]
        self.empty_spaces = set(
            (i, j) for i in range(3) for j in range(3)
            if self.board[i][j] == self.free_space
        )

    @staticmethod
    def _process_move_input(
        move_pos: Union[tuple[int, int], str]
    ) -> tuple[int, int]:
        if len(move_pos) != 2:
            raise WrongMoveException("Move must be two numbers!")
        i, j = move_pos
        if type(i) == str:
            i, j = int(i), int(j)
        if 0 <= i <= 2 and 0 <= j <= 2:
            return i, j
        else:
            raise WrongMoveException("Move can't be outside the board!")

    def __getitem__(self, i: int) -> list[str]:
        return self.board[i]

    def is_correct_move(self, move_pos: Union[tuple[int, int], str]) -> bool:
        i, j = self._process_move_input(move_pos)
        return True if self.board[i][j] == self.free_space else False

    def has_place(self) -> bool:
        return True if len(self.empty_spaces) != 0 else False

    def place(
        self,
        move_pos: Union[tuple[int, int], str],
        first_player_turn: bool = True
    ) -> None:
        if not self.has_place():
            raise NoMovesException("Can't place any more moves!")
        i, j = self._process_move_input(move_pos)
        if not self.is_correct_move((i, j)):
            raise WrongMoveException("You can't place here!")
        self.board[i][j] = self.cross if first_player_turn else self.zero
        self.empty_spaces.remove((i, j))

    def place_random(self, first_player_turn: bool = False) -> None:
        if len(self.empty_spaces) == 0:
            raise NoMovesException("Can't place any more moves!")
        i, j = random.choice(list(self.empty_spaces))
        self.place((i, j), first_player_turn=first_player_turn)

    def has_win(self) -> bool:
        for row in range(3):
            if (
                self.board[row][0] ==
                self.board[row][1] ==
                self.board[row][2] !=
                self.free_space
            ):
                return True

        for col in range(3):
            if (
                self.board[0][col] ==
                self.board[1][col] ==
                self.board[2][col] !=
                self.free_space
            ):
                return True

        if (
            self.board[0][0] ==
            self.board[1][1] ==
            self.board[2][2] !=
            self.free_space
        ):
            return True
        if (
            self.board[0][2] ==
            self.board[1][1] ==
            self.board[2][0] !=
            self.free_space
        ):
            return True

        return False

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self.__eq__(other)
