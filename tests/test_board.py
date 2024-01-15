from copy import deepcopy

import pytest

from game.board import WrongMoveException, NoMovesException
from tests.constants import (
    EMPTY, ZERO, CROSS,
    BOARD, EMPTY_BOARD, DRAW_BOARD,
    HORIZONTAL_WIN_BOARD, VERTICAL_WIN_BOARD,
    LEFT_DIAGONAL_WIN_BOARD, RIGHT_DIAGONAL_WIN_BOARD
)


def test_board_init():
    assert BOARD.free_space == EMPTY
    assert BOARD.cross == CROSS
    assert BOARD.zero == ZERO

    assert BOARD.board == [
        [CROSS, EMPTY, CROSS],
        [ZERO, EMPTY, EMPTY],
        [EMPTY, ZERO, EMPTY]
    ]

    assert len(BOARD.empty_spaces) == 5
    assert BOARD.empty_spaces == {(0, 1), (1, 1), (1, 2), (2, 0), (2, 2)}

    assert len(EMPTY_BOARD.empty_spaces) == 9


def test_move_processing():
    assert BOARD._process_move_input('02') == (0, 2)
    assert BOARD._process_move_input((1, 0)) == (1, 0)
    with pytest.raises(WrongMoveException):
        BOARD._process_move_input('120')
    with pytest.raises(WrongMoveException):
        BOARD._process_move_input('05')


def test_get_item():
    assert BOARD[0][2] == CROSS
    assert BOARD[1] == [ZERO, EMPTY, EMPTY]


def test_is_correct_move():
    assert BOARD.is_correct_move('22')
    assert not BOARD.is_correct_move('00')


def test_has_place():
    assert BOARD.has_place()
    assert not DRAW_BOARD.has_place()


def test_place():
    with pytest.raises(WrongMoveException):
        BOARD.place('00')
    with pytest.raises(NoMovesException):
        DRAW_BOARD.place('10')
    BOARD.place('11')
    assert BOARD[1][1] == CROSS
    assert len(BOARD.empty_spaces) == 4
    BOARD.place('20', first_player_turn=False)
    assert BOARD[2][0] == ZERO
    assert len(BOARD.empty_spaces) == 3


def test_place_random():
    with pytest.raises(NoMovesException):
        DRAW_BOARD.place('00')
    BOARD.place_random()
    assert len(BOARD.empty_spaces) == 4
    BOARD.place_random(first_player_turn=True)
    assert len(BOARD.empty_spaces) == 3


def test_has_win():
    assert not BOARD.has_win()
    assert HORIZONTAL_WIN_BOARD.has_win()
    assert VERTICAL_WIN_BOARD.has_win()
    assert LEFT_DIAGONAL_WIN_BOARD.has_win()
    assert RIGHT_DIAGONAL_WIN_BOARD.has_win()
    assert not DRAW_BOARD.has_win()


def test_eq():
    assert BOARD != EMPTY_BOARD
    assert BOARD == deepcopy(BOARD)
